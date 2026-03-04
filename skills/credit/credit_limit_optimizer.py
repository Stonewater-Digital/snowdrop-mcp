"""Optimize total credit limit to achieve a target utilization ratio.

MCP Tool Name: credit_limit_optimizer
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "credit_limit_optimizer",
    "description": "Calculate the ideal total credit limit to achieve a target utilization ratio based on income and existing limits.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "income": {"type": "number", "description": "Annual gross income."},
            "existing_limits": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of current credit limits.",
            },
            "utilization_target": {
                "type": "number",
                "description": "Target utilization ratio as decimal (default 0.30).",
                "default": 0.30,
            },
        },
        "required": ["income", "existing_limits"],
    },
}


def credit_limit_optimizer(
    income: float,
    existing_limits: list[float],
    utilization_target: float = 0.30,
) -> dict[str, Any]:
    """Calculate ideal credit limit for target utilization."""
    try:
        if income <= 0:
            return {
                "status": "error",
                "data": {"error": "income must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if utilization_target <= 0 or utilization_target >= 1:
            return {
                "status": "error",
                "data": {"error": "utilization_target must be between 0 and 1 exclusive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        current_total = sum(existing_limits)
        # Estimate typical monthly spending as ~30% of monthly income
        estimated_monthly_spend = (income / 12) * 0.30
        ideal_total = estimated_monthly_spend / utilization_target
        additional_needed = max(ideal_total - current_total, 0)

        current_utilization = (estimated_monthly_spend / current_total * 100) if current_total > 0 else 100.0

        return {
            "status": "ok",
            "data": {
                "annual_income": income,
                "estimated_monthly_spend": round(estimated_monthly_spend, 2),
                "current_total_limit": round(current_total, 2),
                "current_utilization_pct": round(current_utilization, 2),
                "target_utilization_pct": round(utilization_target * 100, 2),
                "ideal_total_limit": round(ideal_total, 2),
                "additional_limit_needed": round(additional_needed, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
