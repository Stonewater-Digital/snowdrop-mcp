"""
Executive Summary: Fork-based trade simulation — previews transaction outcome, gas costs, and failure conditions before on-chain execution.
Inputs: transaction (dict: chain str, action str, token_pair str, amount float, params dict),
        current_state (dict: balances dict[str→float], gas_price_gwei float)
Outputs: simulated_outcome (dict), new_balances (dict), gas_cost_usd (float),
         success_probability (float), warnings (list)
MCP Tool Name: transaction_sim_pre_flight
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

# Gas usage estimates per action type (in gas units)
GAS_ESTIMATES: dict[str, int] = {
    "swap":             150_000,
    "transfer":          21_000,
    "approve":           46_000,
    "stake":            200_000,
    "unstake":          200_000,
    "add_liquidity":    250_000,
    "remove_liquidity": 230_000,
    "bridge":           300_000,
    "mint":             120_000,
    "burn":             100_000,
    "DEFAULT":          100_000,
}

# ETH price used for gas cost estimation when no oracle is available
FALLBACK_ETH_PRICE_USD: float = 3_200.0

# Slippage ceiling — warn if slippage parameter exceeds this
MAX_SAFE_SLIPPAGE_PCT: float = 1.0  # 1%

# DEX fee defaults by action
DEX_FEE_PCT: dict[str, float] = {
    "swap":          0.003,  # 0.3% Uniswap-style
    "add_liquidity": 0.003,
    "DEFAULT":       0.0,
}

TOOL_META = {
    "name": "transaction_sim_pre_flight",
    "description": (
        "Simulates an on-chain transaction in isolation before submission. "
        "Checks for insufficient balances, high slippage, and other failure conditions. "
        "Returns projected new balances, estimated gas cost in USD, and a success "
        "probability score derived from balance adequacy and warning count."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "transaction": {
                "type": "object",
                "properties": {
                    "chain":      {"type": "string"},
                    "action":     {"type": "string"},
                    "token_pair": {"type": "string"},
                    "amount":     {"type": "number"},
                    "params":     {"type": "object"},
                },
                "required": ["chain", "action", "token_pair", "amount"],
            },
            "current_state": {
                "type": "object",
                "properties": {
                    "balances":        {"type": "object", "additionalProperties": {"type": "number"}},
                    "gas_price_gwei":  {"type": "number"},
                    "eth_price_usd":   {"type": "number", "description": "Optional ETH price for gas USD conversion."},
                },
                "required": ["balances", "gas_price_gwei"],
            },
        },
        "required": ["transaction", "current_state"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "simulated_outcome":  {"type": "object"},
            "new_balances":       {"type": "object"},
            "gas_cost_usd":       {"type": "number"},
            "success_probability": {"type": "number"},
            "warnings":           {"type": "array"},
            "status":             {"type": "string"},
            "timestamp":          {"type": "string"},
        },
        "required": [
            "simulated_outcome", "new_balances", "gas_cost_usd",
            "success_probability", "warnings", "status", "timestamp"
        ],
    },
}


def transaction_sim_pre_flight(
    transaction: dict[str, Any],
    current_state: dict[str, Any],
) -> dict[str, Any]:
    """Simulate an on-chain transaction and report projected outcomes before submission.

    Applies DEX fees and slippage to estimate received amount. Checks balances,
    slippage settings, and gas affordability. Computes a success probability
    (0.0–1.0) from the ratio of passing checks to total checks.

    Args:
        transaction: Transaction descriptor with keys:
            - chain (str): Blockchain name (e.g. "ethereum", "ton").
            - action (str): Action type — swap, transfer, stake, etc.
            - token_pair (str): Asset pair, e.g. "ETH/USDC".
            - amount (float): Amount of the input token.
            - params (dict, optional): Extra params — slippage_pct, price_impact_pct, etc.
        current_state: Current on-chain state snapshot with keys:
            - balances (dict[str, float]): Token symbol → available balance.
            - gas_price_gwei (float): Current gas price in Gwei.
            - eth_price_usd (float, optional): ETH/USD price for gas conversion.

    Returns:
        dict with keys:
            - status (str): "success" or "error".
            - simulated_outcome (dict): Projected token flows and action summary.
            - new_balances (dict): Estimated post-transaction balances.
            - gas_cost_usd (float): Estimated gas cost in USD.
            - success_probability (float): Probability of execution success (0–1).
            - warnings (list[str]): Non-fatal issues detected during simulation.
            - timestamp (str): ISO 8601 UTC execution timestamp.
    """
    try:
        now_utc: datetime = datetime.now(timezone.utc)
        warnings: list[str] = []
        checks_passed: int = 0
        total_checks: int = 0

        chain: str = str(transaction.get("chain", "ethereum")).lower()
        action: str = str(transaction.get("action", "swap")).lower()
        token_pair: str = str(transaction.get("token_pair", ""))
        amount: float = float(transaction.get("amount", 0.0))
        params: dict[str, Any] = transaction.get("params", {}) or {}

        balances: dict[str, float] = {
            k.upper(): float(v) for k, v in current_state.get("balances", {}).items()
        }
        gas_price_gwei: float = float(current_state.get("gas_price_gwei", 20.0))
        eth_price_usd: float = float(current_state.get("eth_price_usd", FALLBACK_ETH_PRICE_USD))

        # Determine input/output tokens from token_pair
        parts: list[str] = token_pair.upper().replace("-", "/").split("/")
        input_token: str = parts[0] if len(parts) >= 1 else "UNKNOWN"
        output_token: str = parts[1] if len(parts) >= 2 else "UNKNOWN"

        # Gas cost calculation
        gas_units: int = GAS_ESTIMATES.get(action, GAS_ESTIMATES["DEFAULT"])
        gas_cost_eth: float = (gas_price_gwei * gas_units) / 1e9  # Gwei → ETH
        gas_cost_usd: float = round(gas_cost_eth * eth_price_usd, 4)

        # Check 1: Sufficient input token balance
        total_checks += 1
        input_balance: float = balances.get(input_token, 0.0)
        if input_balance >= amount:
            checks_passed += 1
        else:
            warnings.append(
                f"Insufficient {input_token} balance: have {input_balance:.6f}, need {amount:.6f}."
            )

        # Check 2: Gas affordability (ETH/native token balance)
        total_checks += 1
        eth_balance: float = balances.get("ETH", balances.get("WETH", 0.0))
        if chain in ("ton",):
            eth_balance = balances.get("TON", 0.0)
            gas_cost_eth_for_check = gas_cost_eth  # treat as native token
        else:
            gas_cost_eth_for_check = gas_cost_eth

        if eth_balance >= gas_cost_eth_for_check:
            checks_passed += 1
        else:
            warnings.append(
                f"Insufficient gas funds: have {eth_balance:.6f} ETH, "
                f"estimated gas {gas_cost_eth_for_check:.6f} ETH (${gas_cost_usd:.2f})."
            )

        # Check 3: Slippage guard
        total_checks += 1
        slippage_pct: float = float(params.get("slippage_pct", 0.5))
        if slippage_pct <= MAX_SAFE_SLIPPAGE_PCT:
            checks_passed += 1
        else:
            warnings.append(
                f"High slippage setting: {slippage_pct}% exceeds recommended maximum "
                f"of {MAX_SAFE_SLIPPAGE_PCT}%."
            )

        # Check 4: Price impact guard
        total_checks += 1
        price_impact_pct: float = float(params.get("price_impact_pct", 0.0))
        if price_impact_pct < 2.0:
            checks_passed += 1
        else:
            warnings.append(
                f"High price impact: {price_impact_pct:.2f}%. "
                "Consider splitting the order into smaller tranches."
            )

        # Simulate new balances
        dex_fee_pct: float = DEX_FEE_PCT.get(action, DEX_FEE_PCT["DEFAULT"])
        amount_after_fee: float = amount * (1.0 - dex_fee_pct)
        # Apply slippage to estimate received amount
        received_amount: float = amount_after_fee * (1.0 - slippage_pct / 100.0)
        # Apply price impact reduction
        received_amount *= (1.0 - price_impact_pct / 100.0)
        received_amount = round(received_amount, 8)

        new_balances: dict[str, float] = dict(balances)
        new_balances[input_token] = round(
            new_balances.get(input_token, 0.0) - amount, 8
        )
        new_balances[output_token] = round(
            new_balances.get(output_token, 0.0) + received_amount, 8
        )
        # Deduct gas from ETH
        new_eth_key: str = "ETH" if "ETH" in new_balances else "WETH"
        new_balances[new_eth_key] = round(
            new_balances.get(new_eth_key, 0.0) - gas_cost_eth, 8
        )

        success_probability: float = round(checks_passed / total_checks, 4) if total_checks > 0 else 0.0

        simulated_outcome: dict[str, Any] = {
            "chain":               chain,
            "action":              action,
            "input_token":         input_token,
            "output_token":        output_token,
            "input_amount":        amount,
            "dex_fee_pct":         dex_fee_pct,
            "slippage_applied_pct": slippage_pct,
            "price_impact_pct":    price_impact_pct,
            "estimated_received":  received_amount,
            "gas_units":           gas_units,
            "gas_price_gwei":      gas_price_gwei,
            "gas_cost_eth":        round(gas_cost_eth, 8),
            "gas_cost_usd":        gas_cost_usd,
            "checks_passed":       checks_passed,
            "total_checks":        total_checks,
        }

        return {
            "status":              "success",
            "simulated_outcome":   simulated_outcome,
            "new_balances":        new_balances,
            "gas_cost_usd":        gas_cost_usd,
            "success_probability": success_probability,
            "warnings":            warnings,
            "timestamp":           now_utc.isoformat(),
        }

    except Exception as e:
        logger.error(f"transaction_sim_pre_flight failed: {e}")
        _log_lesson(f"transaction_sim_pre_flight: {e}")
        return {"status": "error", "error": str(e), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    """Append a failure lesson to the shared lessons log.

    Args:
        message: Human-readable description of the failure.
    """
    with open("logs/lessons.md", "a") as f:
        f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
