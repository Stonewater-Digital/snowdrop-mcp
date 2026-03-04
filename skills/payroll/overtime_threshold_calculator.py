"""Calculate regular and overtime pay.

MCP Tool Name: overtime_threshold_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "overtime_threshold_calculator",
    "description": "Calculate regular and overtime pay given hourly rate, hours worked, overtime multiplier, and threshold (default 40 hours).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "hourly_rate": {
                "type": "number",
                "description": "Regular hourly rate in USD.",
            },
            "hours_worked": {
                "type": "number",
                "description": "Total hours worked in the period.",
            },
            "overtime_multiplier": {
                "type": "number",
                "description": "Overtime pay multiplier (e.g. 1.5 for time-and-a-half).",
                "default": 1.5,
            },
            "threshold": {
                "type": "number",
                "description": "Hours threshold before overtime kicks in.",
                "default": 40,
            },
        },
        "required": ["hourly_rate", "hours_worked"],
    },
}


def overtime_threshold_calculator(
    hourly_rate: float,
    hours_worked: float,
    overtime_multiplier: float = 1.5,
    threshold: float = 40,
) -> dict[str, Any]:
    """Calculate regular and overtime pay."""
    try:
        if hourly_rate < 0:
            return {
                "status": "error",
                "data": {"error": "hourly_rate must be non-negative."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if hours_worked < 0:
            return {
                "status": "error",
                "data": {"error": "hours_worked must be non-negative."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        regular_hours = min(hours_worked, threshold)
        overtime_hours = max(hours_worked - threshold, 0)

        regular_pay = regular_hours * hourly_rate
        overtime_rate = hourly_rate * overtime_multiplier
        overtime_pay = overtime_hours * overtime_rate
        total_pay = regular_pay + overtime_pay

        effective_rate = total_pay / hours_worked if hours_worked > 0 else 0

        return {
            "status": "ok",
            "data": {
                "hourly_rate": round(hourly_rate, 2),
                "hours_worked": round(hours_worked, 2),
                "overtime_threshold": threshold,
                "regular_hours": round(regular_hours, 2),
                "overtime_hours": round(overtime_hours, 2),
                "regular_pay": round(regular_pay, 2),
                "overtime_rate": round(overtime_rate, 2),
                "overtime_multiplier": overtime_multiplier,
                "overtime_pay": round(overtime_pay, 2),
                "total_gross_pay": round(total_pay, 2),
                "effective_hourly_rate": round(effective_rate, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
