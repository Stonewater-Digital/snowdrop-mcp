"""Estimate homeowners insurance premium based on home and contents value.

MCP Tool Name: homeowners_insurance_estimator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "homeowners_insurance_estimator",
    "description": "Estimate homeowners insurance annual premium based on home value, contents value, and deductible. Range: 0.3%-0.5% of home value adjusted by deductible.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "home_value": {"type": "number", "description": "Estimated home replacement value."},
            "contents_value": {"type": "number", "description": "Estimated contents/personal property value (default 0).", "default": 0},
            "deductible": {"type": "number", "description": "Policy deductible (default 1000).", "default": 1000},
        },
        "required": ["home_value"],
    },
}


def homeowners_insurance_estimator(
    home_value: float, contents_value: float = 0, deductible: float = 1000
) -> dict[str, Any]:
    """Estimate homeowners insurance premium."""
    try:
        if home_value <= 0:
            return {
                "status": "error",
                "data": {"error": "home_value must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # Higher deductible = lower premium
        if deductible >= 5000:
            rate = 0.003  # 0.3%
        elif deductible >= 2500:
            rate = 0.0035
        elif deductible >= 1000:
            rate = 0.004
        else:
            rate = 0.005  # 0.5%

        dwelling_premium = home_value * rate
        # Contents coverage typically 50-70% of dwelling rate
        contents_premium = contents_value * rate * 0.6
        total_premium = dwelling_premium + contents_premium
        monthly = total_premium / 12

        return {
            "status": "ok",
            "data": {
                "home_value": home_value,
                "contents_value": contents_value,
                "deductible": deductible,
                "rate_applied": round(rate * 100, 2),
                "dwelling_premium": round(dwelling_premium, 2),
                "contents_premium": round(contents_premium, 2),
                "estimated_annual_premium": round(total_premium, 2),
                "estimated_monthly_premium": round(monthly, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
