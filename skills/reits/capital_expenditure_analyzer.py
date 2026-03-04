"""Split REIT capital expenditures by type."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "capital_expenditure_analyzer",
    "description": "Breaks capex into maintenance vs growth and measures NOI burden.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "maintenance_capex": {"type": "number"},
            "growth_capex": {"type": "number"},
            "net_operating_income": {"type": "number"},
        },
        "required": ["maintenance_capex", "growth_capex", "net_operating_income"],
    },
    "outputSchema": {"type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def capital_expenditure_analyzer(
    maintenance_capex: float,
    growth_capex: float,
    net_operating_income: float,
    **_: Any,
) -> dict[str, Any]:
    """Return capex intensity metrics."""
    try:
        total_capex = maintenance_capex + growth_capex
        maintenance_ratio = maintenance_capex / total_capex * 100 if total_capex else 0.0
        noi_burden = total_capex / net_operating_income * 100 if net_operating_income else 0.0
        data = {
            "total_capex": round(total_capex, 2),
            "maintenance_pct": round(maintenance_ratio, 2),
            "noi_burden_pct": round(noi_burden, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("capital_expenditure_analyzer", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
