"""Calculate whether current savings will grow to target by retirement (Coast FIRE).

MCP Tool Name: coast_fire_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "coast_fire_calculator",
    "description": "Determines if current savings will compound to the target retirement amount without additional contributions (Coast FIRE).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "current_savings": {
                "type": "number",
                "description": "Current total invested savings in dollars.",
            },
            "target_amount": {
                "type": "number",
                "description": "Target retirement portfolio amount in dollars.",
            },
            "years_to_retire": {
                "type": "number",
                "description": "Number of years until planned retirement.",
            },
            "expected_return": {
                "type": "number",
                "description": "Expected annual real investment return as a decimal (default: 0.07).",
            },
        },
        "required": ["current_savings", "target_amount", "years_to_retire"],
    },
}


def coast_fire_calculator(
    current_savings: float,
    target_amount: float,
    years_to_retire: float,
    expected_return: float = 0.07,
) -> dict[str, Any]:
    """Determines if current savings will coast to the retirement target."""
    try:
        if years_to_retire <= 0:
            return {
                "status": "error",
                "data": {"error": "Years to retire must be a positive number."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if target_amount <= 0:
            return {
                "status": "error",
                "data": {"error": "Target amount must be a positive number."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        future_value = round(current_savings * (1 + expected_return) ** years_to_retire, 2)
        is_coast = future_value >= target_amount

        # Calculate the minimum savings needed today to coast
        coast_number = round(target_amount / (1 + expected_return) ** years_to_retire, 2)
        gap = round(coast_number - current_savings, 2)

        return {
            "status": "ok",
            "data": {
                "current_savings": current_savings,
                "target_amount": target_amount,
                "years_to_retire": years_to_retire,
                "expected_return_pct": round(expected_return * 100, 2),
                "projected_future_value": future_value,
                "coast_fire_number": coast_number,
                "is_coast_fire": is_coast,
                "gap_to_coast": max(0, gap),
                "surplus_above_coast": max(0, round(-gap, 2)),
                "explanation": (
                    f"With ${current_savings:,.2f} growing at {expected_return*100:.1f}% for {years_to_retire:.0f} years, "
                    f"your portfolio will reach ${future_value:,.2f}. "
                    + (
                        f"You have reached Coast FIRE — you could stop saving and still reach your ${target_amount:,.2f} target."
                        if is_coast
                        else f"You need ${gap:,.2f} more to reach your Coast FIRE number of ${coast_number:,.2f}."
                    )
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
