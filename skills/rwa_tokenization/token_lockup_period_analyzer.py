"""Analyze investor lockup periods for tokenized offerings.
Reports remaining lockup, penalty tiers, and liquidity classification."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Sequence
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "token_lockup_period_analyzer",
    "description": "Summarizes lockup mechanics with current remaining term and unlock schedule.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "total_lockup_months": {"type": "integer", "description": "Total lockup duration"},
            "months_elapsed": {"type": "number", "description": "Months passed since issuance"},
            "penalty_schedule": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "threshold_month": {"type": "number"},
                        "penalty_pct": {"type": "number"},
                    },
                    "required": ["threshold_month", "penalty_pct"],
                },
                "description": "Penalty tiers for early exits",
            },
        },
        "required": ["total_lockup_months", "months_elapsed", "penalty_schedule"],
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


def token_lockup_period_analyzer(
    total_lockup_months: int,
    months_elapsed: float,
    penalty_schedule: Sequence[dict[str, float]],
    **_: Any,
) -> dict[str, Any]:
    """Evaluate lockup progress and penalty tiers.

    Args:
        total_lockup_months: Total lockup duration.
        months_elapsed: Months since issuance.
        penalty_schedule: Penalty tiers for early exit.

    Returns:
        Dict with remaining lockup and current penalty tier.
    """
    try:
        remaining = max(total_lockup_months - months_elapsed, 0)
        penalty_schedule_sorted = sorted(penalty_schedule, key=lambda tier: tier.get("threshold_month", 0))
        current_penalty = 0.0
        for tier in penalty_schedule_sorted:
            if months_elapsed < tier.get("threshold_month", 0):
                current_penalty = float(tier.get("penalty_pct", 0))
                break
        else:
            current_penalty = 0.0
        liquidity_tier = "locked" if remaining > 6 else "semi-liquid" if remaining > 0 else "open"
        data = {
            "months_remaining": round(remaining, 2),
            "current_penalty_pct": round(current_penalty, 2),
            "liquidity_tier": liquidity_tier,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("token_lockup_period_analyzer failure: %s", exc)
        log_lesson(f"token_lockup_period_analyzer: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
