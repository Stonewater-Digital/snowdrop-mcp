"""Analyze municipal bond tax-equivalent yields."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "muni_bond_analyzer",
    "description": "Computes tax-equivalent yield, breakeven rates, and annual savings for muni bonds.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "muni_yield": {"type": "number"},
            "taxable_yield": {"type": "number"},
            "federal_tax_rate": {"type": "number"},
            "state_tax_rate": {"type": "number", "default": 0},
            "in_state": {"type": "boolean", "default": True},
            "amt_subject": {"type": "boolean", "default": False},
        },
        "required": ["muni_yield", "taxable_yield", "federal_tax_rate"],
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


def muni_bond_analyzer(
    muni_yield: float,
    taxable_yield: float,
    federal_tax_rate: float,
    state_tax_rate: float = 0.0,
    in_state: bool = True,
    amt_subject: bool = False,
    **_: Any,
) -> dict[str, Any]:
    """Return muni vs taxable comparison metrics."""
    try:
        combined_rate = federal_tax_rate / 100
        if in_state:
            combined_rate += state_tax_rate / 100
        if amt_subject:
            combined_rate = min(combined_rate, 0.28)
        tax_equivalent = muni_yield / max(1 - combined_rate, 1e-6)
        tax_advantage = tax_equivalent - taxable_yield
        breakeven = 1 - (muni_yield / taxable_yield) if taxable_yield else 0
        better = "muni" if tax_equivalent > taxable_yield else "taxable"
        annual_savings = (tax_equivalent - taxable_yield) / 100 * 100000
        data = {
            "tax_equivalent_yield": round(tax_equivalent, 3),
            "tax_advantage_bps": round(tax_advantage * 100, 2),
            "breakeven_tax_rate": round(breakeven * 100, 2),
            "better_choice": better,
            "annual_tax_savings_per_100k": round(annual_savings, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("muni_bond_analyzer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
