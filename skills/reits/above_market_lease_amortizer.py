"""Amortize above/below market lease intangibles."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "above_market_lease_amortizer",
    "description": "Calculates periodic amortization expense for lease intangibles.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "intangible_value": {"type": "number"},
            "remaining_term_years": {"type": "number"},
            "discount_rate_pct": {"type": "number", "default": 0.0},
        },
        "required": ["intangible_value", "remaining_term_years"],
    },
    "outputSchema": {"type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def above_market_lease_amortizer(
    intangible_value: float,
    remaining_term_years: float,
    discount_rate_pct: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Return level amortization schedule info."""
    try:
        months = int(remaining_term_years * 12)
        if months <= 0:
            raise ValueError("remaining_term_years must be positive")
        monthly_rate = discount_rate_pct / 100 / 12
        if monthly_rate:
            annuity_factor = (1 - (1 + monthly_rate) ** -months) / monthly_rate
            monthly_expense = intangible_value / annuity_factor
        else:
            monthly_expense = intangible_value / months
        annual_expense = monthly_expense * 12
        data = {
            "monthly_amortization": round(monthly_expense, 2),
            "annual_amortization": round(annual_expense, 2),
            "remaining_months": months,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("above_market_lease_amortizer", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
