"""Model tax increment financing districts."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "tif_district_calculator",
    "description": "Projects increment revenue and coverage for TIF districts over the term.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "base_assessed_value": {"type": "number"},
            "projected_assessed_value": {"type": "number"},
            "tax_rate_per_100": {"type": "number"},
            "tif_term_years": {"type": "integer"},
            "project_cost": {"type": "number"},
            "annual_growth_rate": {"type": "number", "default": 0.03},
        },
        "required": [
            "base_assessed_value",
            "projected_assessed_value",
            "tax_rate_per_100",
            "tif_term_years",
            "project_cost",
        ],
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


def tif_district_calculator(
    base_assessed_value: float,
    projected_assessed_value: float,
    tax_rate_per_100: float,
    tif_term_years: int,
    project_cost: float,
    annual_growth_rate: float = 0.03,
    **_: Any,
) -> dict[str, Any]:
    """Return annual increments, coverage ratios, and payback timing."""
    try:
        annual_increment = []
        base_tax = base_assessed_value / 100 * tax_rate_per_100
        increment_total = 0.0
        payback_year = None
        for year in range(1, tif_term_years + 1):
            growth_factor = (1 + annual_growth_rate) ** (year - 1)
            value = min(projected_assessed_value * growth_factor, projected_assessed_value)
            taxes = value / 100 * tax_rate_per_100
            increment = max(taxes - base_tax, 0)
            increment_total += increment
            if payback_year is None and increment_total >= project_cost:
                payback_year = year
            annual_increment.append({"year": year, "increment": round(increment, 2)})
        coverage = increment_total / max(project_cost, 1e-6) * 100
        data = {
            "annual_increment": annual_increment,
            "cumulative_increment": round(increment_total, 2),
            "project_coverage_pct": round(coverage, 2),
            "payback_year": payback_year,
            "total_taxes_diverted": round(increment_total, 2),
            "impact_on_taxing_bodies": round(base_tax * tif_term_years - increment_total, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("tif_district_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
