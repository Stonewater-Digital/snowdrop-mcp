"""Model token vesting schedules with cliffs and linear releases.
Useful for tracking unlock cadence relative to circulating supply."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "token_vesting_schedule_calculator",
    "description": "Converts vesting plans with cliffs into cumulative unlock curves and outstanding balances.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "total_tokens": {"type": "number", "description": "Total grant size"},
            "cliff_months": {"type": "integer", "description": "Months before first unlock"},
            "vesting_months": {"type": "integer", "description": "Total vesting duration after cliff"},
            "months_elapsed": {"type": "number", "description": "Months passed since start"},
        },
        "required": ["total_tokens", "cliff_months", "vesting_months", "months_elapsed"],
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


def token_vesting_schedule_calculator(
    total_tokens: float,
    cliff_months: int,
    vesting_months: int,
    months_elapsed: float,
    **_: Any,
) -> dict[str, Any]:
    """Compute unlocked and remaining balances for vesting grants.

    Args:
        total_tokens: Size of the award.
        cliff_months: Months before first unlock.
        vesting_months: Total linear vesting duration.
        months_elapsed: Months passed since grant inception.

    Returns:
        Dict including unlocked tokens, percent vested, and schedule metadata.
    """
    try:
        if vesting_months <= 0:
            raise ValueError("vesting_months must be positive")
        if months_elapsed < cliff_months:
            unlocked = 0.0
        else:
            vested_months = min(months_elapsed - cliff_months, vesting_months)
            unlocked = (vested_months / vesting_months) * total_tokens
        unlocked = min(max(unlocked, 0.0), total_tokens)
        remaining = total_tokens - unlocked
        vested_pct = unlocked / total_tokens * 100 if total_tokens else 0.0
        data = {
            "unlocked_tokens": round(unlocked, 2),
            "remaining_tokens": round(remaining, 2),
            "vested_pct": round(vested_pct, 2),
            "months_until_fully_vested": max(cliff_months + vesting_months - months_elapsed, 0),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("token_vesting_schedule_calculator failure: %s", exc)
        log_lesson(f"token_vesting_schedule_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
