"""Calculate debt service coverage for private credit loans."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "debt_service_coverage_calculator",
    "description": "Computes DSCR using EBITDA less capex relative to cash interest and amortization.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "ebitda": {"type": "number"},
            "interest_expense": {"type": "number"},
            "principal_amortization": {"type": "number"},
            "maintenance_capex": {"type": "number", "default": 0.0},
        },
        "required": ["ebitda", "interest_expense", "principal_amortization"],
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


def debt_service_coverage_calculator(
    ebitda: float,
    interest_expense: float,
    principal_amortization: float,
    maintenance_capex: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Return DSCR metrics and stress buffer."""
    try:
        operating_cash_flow = ebitda - maintenance_capex
        debt_service = interest_expense + principal_amortization
        dscr = operating_cash_flow / debt_service if debt_service else 0.0
        cushion_pct = (operating_cash_flow - debt_service) / debt_service * 100 if debt_service else 0.0
        warning = dscr < 1.2
        data = {
            "operating_cash_flow": round(operating_cash_flow, 2),
            "debt_service": round(debt_service, 2),
            "dscr": round(dscr, 3),
            "cash_cushion_pct": round(cushion_pct, 2),
            "breach_warning": warning,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("debt_service_coverage_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
