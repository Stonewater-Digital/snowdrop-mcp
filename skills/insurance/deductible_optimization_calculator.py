"""Optimize insurance deductible choice by comparing premium savings vs expected claims cost.

MCP Tool Name: deductible_optimization_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "deductible_optimization_calculator",
    "description": "Compare low vs high deductible plans: premium savings, breakeven claims needed, and expected value analysis.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "low_deductible": {"type": "number", "description": "Low deductible amount."},
            "low_premium": {"type": "number", "description": "Monthly premium for low-deductible plan."},
            "high_deductible": {"type": "number", "description": "High deductible amount."},
            "high_premium": {"type": "number", "description": "Monthly premium for high-deductible plan."},
            "expected_claims_per_year": {"type": "number", "description": "Expected number of claims per year (default 0.5).", "default": 0.5},
        },
        "required": ["low_deductible", "low_premium", "high_deductible", "high_premium"],
    },
}


def deductible_optimization_calculator(
    low_deductible: float,
    low_premium: float,
    high_deductible: float,
    high_premium: float,
    expected_claims_per_year: float = 0.5,
) -> dict[str, Any]:
    """Optimize deductible choice."""
    try:
        annual_premium_savings = (low_premium - high_premium) * 12
        deductible_increase = high_deductible - low_deductible

        # Breakeven: how many claims to make premium savings worthwhile
        if deductible_increase > 0:
            breakeven_claims = annual_premium_savings / deductible_increase
        else:
            breakeven_claims = 0

        # Expected value comparison
        low_ev = low_premium * 12 + expected_claims_per_year * low_deductible
        high_ev = high_premium * 12 + expected_claims_per_year * high_deductible

        better = "high deductible" if high_ev < low_ev else "low deductible"

        return {
            "status": "ok",
            "data": {
                "low_deductible": low_deductible,
                "low_monthly_premium": low_premium,
                "low_annual_premium": round(low_premium * 12, 2),
                "high_deductible": high_deductible,
                "high_monthly_premium": high_premium,
                "high_annual_premium": round(high_premium * 12, 2),
                "annual_premium_savings": round(annual_premium_savings, 2),
                "deductible_increase": round(deductible_increase, 2),
                "breakeven_claims_per_year": round(breakeven_claims, 2),
                "expected_claims_per_year": expected_claims_per_year,
                "low_deductible_expected_annual_cost": round(low_ev, 2),
                "high_deductible_expected_annual_cost": round(high_ev, 2),
                "better_option": better,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
