"""Calculate overtime pay based on hourly rate and hours worked.

MCP Tool Name: overtime_pay_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "overtime_pay_calculator",
    "description": "Calculate overtime pay using hourly rate, regular hours, and overtime hours with configurable overtime multiplier (default 1.5x).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "hourly_rate": {
                "type": "number",
                "description": "Regular hourly pay rate.",
            },
            "regular_hours": {
                "type": "number",
                "description": "Number of regular (non-overtime) hours worked.",
                "default": 40,
            },
            "overtime_hours": {
                "type": "number",
                "description": "Number of overtime hours worked.",
                "default": 0,
            },
            "overtime_multiplier": {
                "type": "number",
                "description": "Overtime pay multiplier (1.5 = time and a half, 2.0 = double time).",
                "default": 1.5,
            },
        },
        "required": ["hourly_rate"],
    },
}


def overtime_pay_calculator(
    hourly_rate: float,
    regular_hours: float = 40,
    overtime_hours: float = 0,
    overtime_multiplier: float = 1.5,
) -> dict[str, Any]:
    """Calculate overtime pay."""
    try:
        if hourly_rate < 0:
            return {
                "status": "error",
                "data": {"error": "Hourly rate cannot be negative."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        regular_pay = hourly_rate * regular_hours
        overtime_rate = hourly_rate * overtime_multiplier
        overtime_pay = overtime_rate * overtime_hours
        total_pay = regular_pay + overtime_pay
        total_hours = regular_hours + overtime_hours
        effective_hourly = total_pay / total_hours if total_hours > 0 else 0

        # Weekly/annual projections
        weekly_total = total_pay
        annual_projection = weekly_total * 52

        return {
            "status": "ok",
            "data": {
                "hourly_rate": hourly_rate,
                "regular_hours": regular_hours,
                "regular_pay": round(regular_pay, 2),
                "overtime_hours": overtime_hours,
                "overtime_rate": round(overtime_rate, 2),
                "overtime_multiplier": overtime_multiplier,
                "overtime_pay": round(overtime_pay, 2),
                "total_hours": total_hours,
                "total_pay": round(total_pay, 2),
                "effective_hourly_rate": round(effective_hourly, 2),
                "annual_projection_at_this_pace": round(annual_projection, 2),
                "overtime_premium": round(overtime_pay - (hourly_rate * overtime_hours), 2),
                "note": "Under FLSA, non-exempt employees must receive at least 1.5x regular rate for hours over 40/week. "
                "Some states (e.g., California) also require overtime for hours over 8/day or 12/day (double time).",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
