"""Calculate GDP growth rate between two periods.

MCP Tool Name: gdp_growth_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "gdp_growth_calculator",
    "description": "Calculate GDP growth rate between two periods. Returns percentage growth and context on real vs nominal GDP.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "gdp_current": {
                "type": "number",
                "description": "Current period GDP value (in any consistent unit).",
            },
            "gdp_previous": {
                "type": "number",
                "description": "Previous period GDP value (in same unit as current).",
            },
        },
        "required": ["gdp_current", "gdp_previous"],
    },
}


def gdp_growth_calculator(
    gdp_current: float,
    gdp_previous: float,
) -> dict[str, Any]:
    """Calculate GDP growth rate between two periods."""
    try:
        if gdp_previous == 0:
            return {
                "status": "error",
                "data": {"error": "Previous GDP cannot be zero (division by zero)."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        growth_rate = (gdp_current - gdp_previous) / gdp_previous * 100
        absolute_change = gdp_current - gdp_previous

        if growth_rate > 3:
            assessment = "Strong expansion"
        elif growth_rate > 1:
            assessment = "Moderate growth"
        elif growth_rate > 0:
            assessment = "Slow growth"
        elif growth_rate == 0:
            assessment = "Stagnation"
        elif growth_rate > -1:
            assessment = "Mild contraction"
        else:
            assessment = "Significant contraction (recession territory)"

        return {
            "status": "ok",
            "data": {
                "gdp_current": gdp_current,
                "gdp_previous": gdp_previous,
                "growth_rate_pct": round(growth_rate, 4),
                "absolute_change": round(absolute_change, 2),
                "assessment": assessment,
                "note": "This calculates nominal growth. For real GDP growth, ensure both values are inflation-adjusted (constant dollars). Real GDP growth removes the effect of price changes.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
