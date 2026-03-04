"""Compute staking yields for Proof-of-Stake validators or delegators.
Transforms reward schedules into APR and payout per validator."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "staking_yield_calculator",
    "description": "Analyzes staking rewards to derive APR, payout cadence, and token emissions.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "total_staked_tokens": {"type": "number", "description": "Total tokens staked in the network"},
            "annual_inflation_tokens": {"type": "number", "description": "Tokens emitted to stakers annually"},
            "commission_pct": {"type": "number", "description": "Validator/delegation commission percent", "default": 0},
            "token_price_usd": {"type": "number", "description": "Token USD price", "default": 0},
        },
        "required": ["total_staked_tokens", "annual_inflation_tokens"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"},
            "error": {"type": "string"},
        },
    },
}


def staking_yield_calculator(
    total_staked_tokens: float,
    annual_inflation_tokens: float,
    commission_pct: float = 0.0,
    token_price_usd: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Translate inflation schedules to staking returns.

    Args:
        total_staked_tokens: Network stake at measurement time.
        annual_inflation_tokens: Rewards available to stakers.
        commission_pct: Portion withheld by validators.
        token_price_usd: Fiat value for optional cash yield view.

    Returns:
        Response containing net APR and annualized payouts.
    """
    try:
        if total_staked_tokens <= 0:
            raise ValueError("total_staked_tokens must be positive")
        gross_yield = annual_inflation_tokens / total_staked_tokens * 100
        net_yield = gross_yield * (1 - commission_pct / 100)
        annual_reward_value = annual_inflation_tokens * token_price_usd
        data = {
            "gross_apr_pct": round(gross_yield, 2),
            "net_apr_pct": round(net_yield, 2),
            "annual_reward_tokens": round(annual_inflation_tokens, 2),
            "annual_reward_usd": round(annual_reward_value, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("staking_yield_calculator failure: %s", exc)
        log_lesson(f"staking_yield_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
