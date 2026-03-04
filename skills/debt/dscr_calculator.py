"""Debt Service Coverage Ratio calculator."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "dscr_calculator",
    "description": "Computes DSCR, assessment tier, excess cash, and headroom for new debt.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "net_operating_income": {"type": "number"},
            "total_debt_service": {"type": "number"},
        },
        "required": ["net_operating_income", "total_debt_service"],
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


def dscr_calculator(
    net_operating_income: float,
    total_debt_service: float,
    **_: Any,
) -> dict[str, Any]:
    """Return DSCR metrics and assessment."""
    try:
        if total_debt_service <= 0:
            raise ValueError("total_debt_service must be positive")
        dscr = net_operating_income / total_debt_service
        assessment = _assessment(dscr)
        excess_cash_flow = net_operating_income - total_debt_service
        max_additional_debt = max(0.0, net_operating_income / 1.25 - total_debt_service)
        data = {
            "dscr": round(dscr, 3),
            "assessment": assessment,
            "excess_cash_flow": round(excess_cash_flow, 2),
            "maximum_additional_debt": round(max_additional_debt, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("dscr_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _assessment(dscr: float) -> str:
    if dscr > 1.5:
        return "strong"
    if dscr >= 1.25:
        return "adequate"
    if dscr >= 1.0:
        return "marginal"
    return "distressed"


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
