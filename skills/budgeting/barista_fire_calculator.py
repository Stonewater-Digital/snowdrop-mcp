"""Calculate Barista FIRE number (semi-retirement with part-time income).

MCP Tool Name: barista_fire_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "barista_fire_calculator",
    "description": "Calculates Barista FIRE number: the portfolio needed to cover the gap between expenses and part-time income.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "annual_expenses": {
                "type": "number",
                "description": "Total annual living expenses in dollars.",
            },
            "part_time_income": {
                "type": "number",
                "description": "Expected annual income from part-time or flexible work in dollars.",
            },
            "current_savings": {
                "type": "number",
                "description": "Current total invested savings in dollars.",
            },
            "expected_return": {
                "type": "number",
                "description": "Expected annual real investment return as a decimal (default: 0.07).",
            },
        },
        "required": ["annual_expenses", "part_time_income", "current_savings"],
    },
}


def barista_fire_calculator(
    annual_expenses: float,
    part_time_income: float,
    current_savings: float,
    expected_return: float = 0.07,
) -> dict[str, Any]:
    """Calculates Barista FIRE number and status."""
    try:
        if annual_expenses <= 0:
            return {
                "status": "error",
                "data": {"error": "Annual expenses must be a positive number."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        gap = round(annual_expenses - part_time_income, 2)
        if gap <= 0:
            return {
                "status": "ok",
                "data": {
                    "annual_expenses": annual_expenses,
                    "part_time_income": part_time_income,
                    "gap": 0,
                    "barista_fire_number": 0,
                    "status": "Part-time income covers all expenses. No portfolio needed for Barista FIRE.",
                    "surplus": round(abs(gap), 2),
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        barista_fire_number = round(gap * 25, 2)
        regular_fire_number = round(annual_expenses * 25, 2)
        savings_reduction = round(regular_fire_number - barista_fire_number, 2)

        is_barista_fire = current_savings >= barista_fire_number
        is_regular_fire = current_savings >= regular_fire_number

        safe_withdrawal = round(current_savings * 0.04, 2)
        annual_income_at_fire = round(safe_withdrawal + part_time_income, 2)

        progress = round((current_savings / barista_fire_number) * 100, 2) if barista_fire_number > 0 else 100

        return {
            "status": "ok",
            "data": {
                "annual_expenses": annual_expenses,
                "part_time_income": part_time_income,
                "annual_gap": gap,
                "monthly_gap": round(gap / 12, 2),
                "barista_fire_number": barista_fire_number,
                "regular_fire_number": regular_fire_number,
                "savings_vs_regular_fire": savings_reduction,
                "current_savings": current_savings,
                "progress_pct": progress,
                "is_barista_fire": is_barista_fire,
                "gap_to_barista_fire": round(max(0, barista_fire_number - current_savings), 2),
                "current_portfolio_withdrawal": safe_withdrawal,
                "total_annual_income_today": annual_income_at_fire,
                "coverage_pct": round((annual_income_at_fire / annual_expenses) * 100, 2),
                "note": (
                    "Barista FIRE means your portfolio covers the gap between living expenses and part-time income. "
                    f"You need 25x the annual gap (${gap:,.2f}) = ${barista_fire_number:,.2f}, "
                    f"which is ${savings_reduction:,.2f} less than full FIRE (${regular_fire_number:,.2f})."
                ),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
