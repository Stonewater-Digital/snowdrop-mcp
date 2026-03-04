"""Derive nominal and effective APY for incentive farming programs.
Includes optional compounding sensitivity for variable block schedules."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import logging
import math

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "yield_farming_apy_calculator",
    "description": "Translates per-block reward rates into APR and APY estimates for yield farmers.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "reward_rate_per_block": {"type": "number", "description": "Tokens paid per block"},
            "blocks_per_day": {"type": "number", "description": "Expected blocks per day"},
            "reward_token_price_usd": {"type": "number", "description": "USD price of reward token"},
            "staked_value_usd": {"type": "number", "description": "USD value of stake"},
            "compound_frequency_days": {
                "type": "number",
                "description": "Days between reinvestment cycles",
                "default": 1,
            },
        },
        "required": ["reward_rate_per_block", "blocks_per_day", "reward_token_price_usd", "staked_value_usd"],
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


def yield_farming_apy_calculator(
    reward_rate_per_block: float,
    blocks_per_day: float,
    reward_token_price_usd: float,
    staked_value_usd: float,
    compound_frequency_days: float = 1.0,
    **_: Any,
) -> dict[str, Any]:
    """Convert incentive schedules to APR and APY values.

    Args:
        reward_rate_per_block: Tokens paid out per block for the strategy.
        blocks_per_day: Average block production rate.
        reward_token_price_usd: Fiat value of the incentive token.
        staked_value_usd: Total TVL provided by the farmer.
        compound_frequency_days: Interval for compounding reinvestments.

    Returns:
        Payload with nominal APR and effective APY metrics.
    """
    try:
        if staked_value_usd <= 0:
            raise ValueError("staked_value_usd must be positive")
        daily_rewards = reward_rate_per_block * blocks_per_day
        daily_reward_value = daily_rewards * reward_token_price_usd
        apr_pct = daily_reward_value * 365 / staked_value_usd * 100
        periods_per_year = max(int(365 / max(compound_frequency_days, 1e-6)), 1)
        apy_pct = (math.pow(1 + apr_pct / 100 / periods_per_year, periods_per_year) - 1) * 100
        data = {
            "daily_rewards_tokens": round(daily_rewards, 4),
            "daily_rewards_usd": round(daily_reward_value, 2),
            "apr_pct": round(apr_pct, 2),
            "apy_pct": round(apy_pct, 2),
            "periods_per_year": periods_per_year,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("yield_farming_apy_calculator failure: %s", exc)
        log_lesson(f"yield_farming_apy_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
