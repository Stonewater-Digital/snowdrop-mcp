"""Calculate DSCR for REIT portfolios."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "debt_service_coverage_reit",
    "description": "Computes DSCR using NOI less recurring capex versus debt service.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "net_operating_income": {"type": "number"},
            "recurring_capex": {"type": "number", "default": 0.0},
            "interest_expense": {"type": "number"},
            "principal_amortization": {"type": "number"},
        },
        "required": ["net_operating_income", "interest_expense", "principal_amortization"],
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def debt_service_coverage_reit(
    net_operating_income: float,
    interest_expense: float,
    principal_amortization: float,
    recurring_capex: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Return DSCR metrics for REIT balance sheets."""
    try:
        cash_available = net_operating_income - recurring_capex
        debt_service = interest_expense + principal_amortization
        dscr = cash_available / debt_service if debt_service else 0.0
        data = {
            "cash_available": round(cash_available, 2),
            "debt_service": round(debt_service, 2),
            "dscr": round(dscr, 3),
            "warning": dscr < 1.3,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("debt_service_coverage_reit", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
