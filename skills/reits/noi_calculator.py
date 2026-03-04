"""Compute REIT net operating income."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "noi_calculator",
    "description": "Calculates NOI and margin from rental revenue and operating expenses.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "rental_revenue": {"type": "number"},
            "other_income": {"type": "number", "default": 0.0},
            "operating_expenses": {"type": "number"},
            "property_taxes": {"type": "number", "default": 0.0},
            "bad_debt": {"type": "number", "default": 0.0},
        },
        "required": ["rental_revenue", "operating_expenses"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
    },
}


def noi_calculator(
    rental_revenue: float,
    operating_expenses: float,
    other_income: float = 0.0,
    property_taxes: float = 0.0,
    bad_debt: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Return NOI and related metrics."""
    try:
        gross_income = rental_revenue + other_income
        total_expenses = operating_expenses + property_taxes + bad_debt
        noi = gross_income - total_expenses
        margin = noi / gross_income * 100 if gross_income else 0.0
        data = {
            "gross_income": round(gross_income, 2),
            "total_expenses": round(total_expenses, 2),
            "noi": round(noi, 2),
            "noi_margin_pct": round(margin, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("noi_calculator", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
