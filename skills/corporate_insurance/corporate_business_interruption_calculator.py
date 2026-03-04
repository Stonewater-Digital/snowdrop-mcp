"""Business interruption loss estimator.
Calculates net income replacement and waiting period coverage.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "corporate_business_interruption_calculator",
    "description": "Estimates business interruption exposure from revenue, expense, and standby time.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "annual_revenue": {"type": "number"},
            "variable_expense_ratio_pct": {"type": "number"},
            "restoration_period_days": {"type": "number"},
            "waiting_period_days": {"type": "number", "default": 3},
        },
        "required": ["annual_revenue", "variable_expense_ratio_pct", "restoration_period_days"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def corporate_business_interruption_calculator(
    annual_revenue: float,
    variable_expense_ratio_pct: float,
    restoration_period_days: int,
    waiting_period_days: int = 3,
    **_: Any,
) -> dict[str, Any]:
    """Return gross earnings exposure and uncovered waiting period."""
    try:
        daily_revenue = annual_revenue / 365
        contribution_margin = 1 - variable_expense_ratio_pct / 100
        covered_days = max(restoration_period_days - waiting_period_days, 0)
        loss = daily_revenue * contribution_margin * covered_days
        waiting_loss = daily_revenue * contribution_margin * waiting_period_days
        data = {
            "covered_bi_loss": round(loss, 2),
            "waiting_period_loss": round(waiting_loss, 2),
            "contribution_margin_pct": round(contribution_margin * 100, 2),
            "coverage_days": covered_days,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("corporate_business_interruption_calculator failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
