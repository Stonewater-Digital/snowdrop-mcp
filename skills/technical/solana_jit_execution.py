"""
Executive Summary: Calculate Just-in-Time liquidity provisioning plans for Solana AMM pools with slippage and risk scoring.
Inputs: pool_address (str), token_pair (str), amount_usd (float), slippage_tolerance_bps (int)
Outputs: execution_plan (dict), estimated_yield_bps (float), risk_score (float 0-1), position_details (dict)
MCP Tool Name: solana_jit_execution
"""
import os
import math
import hashlib
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "solana_jit_execution",
    "description": "Calculate Just-in-Time liquidity provisioning plan for a Solana AMM pool with yield estimation and risk scoring.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "pool_address": {
                "type": "string",
                "description": "The Solana AMM pool public key address."
            },
            "token_pair": {
                "type": "string",
                "description": "Token pair string, e.g. 'SOL/USDC'."
            },
            "amount_usd": {
                "type": "number",
                "description": "USD value of the JIT liquidity position to provide."
            },
            "slippage_tolerance_bps": {
                "type": "integer",
                "description": "Maximum acceptable slippage in basis points (e.g. 50 = 0.5%)."
            }
        },
        "required": ["pool_address", "token_pair", "amount_usd", "slippage_tolerance_bps"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "execution_plan": {"type": "object"},
            "estimated_yield_bps": {"type": "number"},
            "risk_score": {"type": "number"},
            "position_details": {"type": "object"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"}
        },
        "required": ["execution_plan", "estimated_yield_bps", "risk_score", "position_details", "status", "timestamp"]
    }
}

# JIT LP constants derived from Solana AMM research
_BASE_YIELD_BPS = 12.0        # baseline yield per JIT event in bps
_CONCENTRATION_MULTIPLIER = 3.5   # tick-concentrated positions earn more
_LARGE_POSITION_THRESHOLD_USD = 50_000.0
_HIGH_SLIPPAGE_THRESHOLD_BPS = 200


def solana_jit_execution(
    pool_address: str,
    token_pair: str,
    amount_usd: float,
    slippage_tolerance_bps: int,
) -> dict:
    """Build a JIT liquidity provisioning execution plan for a Solana AMM pool.

    Just-in-Time liquidity involves adding concentrated LP positions immediately
    before a large swap and removing them immediately after, capturing fees with
    minimal impermanent loss exposure.

    Args:
        pool_address: The Solana AMM pool public key address.
        token_pair: Token pair string, e.g. 'SOL/USDC'.
        amount_usd: USD value of the JIT liquidity position to provide.
        slippage_tolerance_bps: Maximum acceptable slippage in basis points.

    Returns:
        A dict with keys:
            - execution_plan (dict): Step-by-step JIT LP strategy.
            - estimated_yield_bps (float): Estimated yield from this JIT event.
            - risk_score (float): Risk score from 0 (safe) to 1 (high risk).
            - position_details (dict): Position size and tick range details.
            - status (str): "success" or "error".
            - timestamp (str): ISO 8601 UTC timestamp.
    """
    try:
        sol_wallet = os.getenv("SOL_WALLET_ADDRESS", "")
        if not sol_wallet:
            raise ValueError("SOL_WALLET_ADDRESS environment variable is not set.")
        if amount_usd <= 0:
            raise ValueError(f"amount_usd must be positive, got {amount_usd}.")
        if slippage_tolerance_bps < 0:
            raise ValueError("slippage_tolerance_bps cannot be negative.")
        if not pool_address:
            raise ValueError("pool_address cannot be empty.")

        tokens = token_pair.upper().split("/")
        if len(tokens) != 2:
            raise ValueError(f"token_pair must be 'TOKEN_A/TOKEN_B' format, got '{token_pair}'.")

        token_a, token_b = tokens

        # Derive a deterministic pool fingerprint for idempotency tracking
        pool_fingerprint = hashlib.sha256(pool_address.encode()).hexdigest()[:12]

        # --- Tick range calculation ---
        # JIT positions use a tight tick range around current price.
        # We approximate a ±slippage_tolerance range for the concentrated position.
        tick_width_bps = max(slippage_tolerance_bps, 10)
        lower_tick_offset = -tick_width_bps
        upper_tick_offset = tick_width_bps

        # --- Yield estimation ---
        # JIT yield = base_yield * concentration_multiplier * size_factor
        # Larger positions relative to pool depth tend to capture more fee value
        # but also bear more price impact risk.
        size_factor = math.log1p(amount_usd / 1_000.0) / math.log1p(10.0)  # normalized
        estimated_yield_bps = round(
            _BASE_YIELD_BPS * _CONCENTRATION_MULTIPLIER * size_factor, 4
        )

        # --- Risk scoring ---
        # Risks: slippage tolerance too wide, large position, exotic pairs
        risk_components: list[float] = []

        # Slippage risk: higher tolerance = more risk of adverse fill
        slippage_risk = min(slippage_tolerance_bps / _HIGH_SLIPPAGE_THRESHOLD_BPS, 1.0)
        risk_components.append(slippage_risk * 0.35)

        # Size risk: large USD positions face more impermanent loss variance
        size_risk = min(amount_usd / _LARGE_POSITION_THRESHOLD_USD, 1.0)
        risk_components.append(size_risk * 0.30)

        # Pair risk: non-stable pairs carry more IL risk
        stablecoins = {"USDC", "USDT", "BUSD", "DAI", "PYUSD"}
        pair_has_stable = bool(stablecoins & {token_a, token_b})
        pair_risk = 0.1 if pair_has_stable else 0.6
        risk_components.append(pair_risk * 0.35)

        risk_score = round(min(sum(risk_components), 1.0), 4)

        # --- Execution plan ---
        execution_plan = {
            "strategy": "JIT_LP_CONCENTRATED",
            "pool_address": pool_address,
            "pool_fingerprint": pool_fingerprint,
            "wallet": sol_wallet,
            "steps": [
                {
                    "step": 1,
                    "action": "detect_pending_swap",
                    "description": "Monitor mempool for large swap transactions targeting this pool.",
                    "trigger_min_swap_usd": round(amount_usd * 0.5, 2),
                },
                {
                    "step": 2,
                    "action": "add_concentrated_liquidity",
                    "description": f"Add {amount_usd} USD of concentrated LP in tick range [{lower_tick_offset}, +{upper_tick_offset}] bps.",
                    "amount_usd": amount_usd,
                    "tick_lower_offset_bps": lower_tick_offset,
                    "tick_upper_offset_bps": upper_tick_offset,
                    "token_a": token_a,
                    "token_b": token_b,
                },
                {
                    "step": 3,
                    "action": "wait_for_swap_confirmation",
                    "description": "Wait for the target swap to settle on-chain (typically 1 block ~400ms on Solana).",
                    "max_wait_ms": 2000,
                },
                {
                    "step": 4,
                    "action": "remove_liquidity",
                    "description": "Remove LP position immediately after swap to lock in fee revenue.",
                    "slippage_tolerance_bps": slippage_tolerance_bps,
                },
                {
                    "step": 5,
                    "action": "collect_fees",
                    "description": "Collect accrued swap fees from the position.",
                    "estimated_fee_bps": estimated_yield_bps,
                },
            ],
            "abort_conditions": [
                "Slippage would exceed tolerance before swap lands",
                "Pool TVL drops >20% between detect and execute",
                "Gas fee spike makes JIT uneconomical",
            ],
        }

        position_details = {
            "token_a": token_a,
            "token_b": token_b,
            "position_usd": amount_usd,
            "tick_lower_offset_bps": lower_tick_offset,
            "tick_upper_offset_bps": upper_tick_offset,
            "concentration_multiplier": _CONCENTRATION_MULTIPLIER,
            "slippage_tolerance_bps": slippage_tolerance_bps,
            "wallet_address": sol_wallet,
        }

        return {
            "status": "success",
            "execution_plan": execution_plan,
            "estimated_yield_bps": estimated_yield_bps,
            "risk_score": risk_score,
            "position_details": position_details,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"solana_jit_execution failed: {e}")
        _log_lesson(f"solana_jit_execution: {e}")
        return {
            "status": "error",
            "error": str(e),
            "execution_plan": {},
            "estimated_yield_bps": 0.0,
            "risk_score": 1.0,
            "position_details": {},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    """Append an error lesson to the lessons log file.

    Args:
        message: The lesson message to record.
    """
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        logger.warning("Could not write to logs/lessons.md")
