"""Shock EBITDA and rates to recompute credit metrics."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "credit_portfolio_stress_tester",
    "description": "Applies EBITDA declines and rate shocks to measure coverage and leverage impact.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "base_ebitda": {"type": "number"},
            "base_interest_expense": {"type": "number"},
            "total_debt": {"type": "number"},
            "rate_shock_bps": {"type": "number", "default": 200},
            "ebitda_decline_pct": {"type": "number", "default": 15.0},
        },
        "required": ["base_ebitda", "base_interest_expense", "total_debt"],
    },
    "outputSchema": {"type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def credit_portfolio_stress_tester(
    base_ebitda: float,
    base_interest_expense: float,
    total_debt: float,
    rate_shock_bps: float = 200,
    ebitda_decline_pct: float = 15.0,
    **_: Any,
) -> dict[str, Any]:
    """Return stressed coverage and leverage statistics."""
    try:
        stressed_interest = base_interest_expense + total_debt * (rate_shock_bps / 10000)
        stressed_ebitda = base_ebitda * (1 - ebitda_decline_pct / 100)
        stressed_coverage = stressed_ebitda / stressed_interest if stressed_interest else 0.0
        stressed_leverage = total_debt / stressed_ebitda if stressed_ebitda else 0.0
        data = {
            "stressed_interest_expense": round(stressed_interest, 2),
            "stressed_ebitda": round(stressed_ebitda, 2),
            "stressed_interest_coverage": round(stressed_coverage, 3),
            "stressed_gross_leverage": round(stressed_leverage, 2),
            "breach_warning": stressed_coverage < 1.0 or stressed_leverage > 6.0,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("credit_portfolio_stress_tester", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
