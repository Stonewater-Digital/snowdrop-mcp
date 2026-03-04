"""Estimate disability insurance benefit needs and coverage gap.

MCP Tool Name: disability_insurance_estimator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "disability_insurance_estimator",
    "description": "Estimate disability insurance monthly benefit needs (typically 60% of income) and calculate any coverage gap.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "monthly_income": {"type": "number", "description": "Gross monthly income."},
            "coverage_pct": {"type": "number", "description": "Desired coverage as decimal (default 0.60 for 60%).", "default": 0.60},
            "existing_coverage": {"type": "number", "description": "Existing monthly disability benefit (default 0).", "default": 0},
        },
        "required": ["monthly_income"],
    },
}


def disability_insurance_estimator(
    monthly_income: float, coverage_pct: float = 0.60, existing_coverage: float = 0
) -> dict[str, Any]:
    """Estimate disability insurance needs and gap."""
    try:
        if monthly_income <= 0:
            return {
                "status": "error",
                "data": {"error": "monthly_income must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        needed_benefit = monthly_income * coverage_pct
        gap = max(needed_benefit - existing_coverage, 0)

        return {
            "status": "ok",
            "data": {
                "monthly_income": monthly_income,
                "coverage_pct": round(coverage_pct * 100, 1),
                "needed_monthly_benefit": round(needed_benefit, 2),
                "existing_coverage": existing_coverage,
                "monthly_coverage_gap": round(gap, 2),
                "annual_benefit_needed": round(needed_benefit * 12, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
