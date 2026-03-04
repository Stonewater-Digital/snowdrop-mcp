"""Calculate GAAP straight-line rent adjustments."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "straight_line_rent_calculator",
    "description": "Computes straight-line rent adjustment over the remaining lease term.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "cash_rent": {"type": "number"},
            "gaap_rent": {"type": "number"},
            "remaining_term_years": {"type": "number"},
        },
        "required": ["cash_rent", "gaap_rent", "remaining_term_years"],
    },
    "outputSchema": {"type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def straight_line_rent_calculator(
    cash_rent: float,
    gaap_rent: float,
    remaining_term_years: float,
    **_: Any,
) -> dict[str, Any]:
    """Return straight-line rent add-back or deduction."""
    try:
        difference = gaap_rent - cash_rent
        annual_adj = difference / remaining_term_years if remaining_term_years else 0.0
        data = {
            "gaap_rent": round(gaap_rent, 2),
            "cash_rent": round(cash_rent, 2),
            "straight_line_adjustment": round(annual_adj, 2),
            "is_non_cash_income": annual_adj > 0,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("straight_line_rent_calculator", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
