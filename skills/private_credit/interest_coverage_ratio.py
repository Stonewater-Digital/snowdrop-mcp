"""Measure EBITDA to interest coverage strength."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "interest_coverage_ratio",
    "description": "Calculates interest and fixed charge coverage ratios.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "ebitda": {"type": "number"},
            "interest_expense": {"type": "number"},
            "fixed_charges": {"type": "number", "default": 0.0},
            "stress_decline_pct": {"type": "number", "default": 15.0},
        },
        "required": ["ebitda", "interest_expense"],
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


def interest_coverage_ratio(
    ebitda: float,
    interest_expense: float,
    fixed_charges: float = 0.0,
    stress_decline_pct: float = 15.0,
    **_: Any,
) -> dict[str, Any]:
    """Return coverage metrics with stress scenario."""
    try:
        interest_cov = ebitda / interest_expense if interest_expense else 0.0
        fixed_charge_cov = ebitda / (interest_expense + fixed_charges) if (interest_expense + fixed_charges) else 0.0
        stressed_ebitda = ebitda * (1 - stress_decline_pct / 100)
        stressed_cov = stressed_ebitda / interest_expense if interest_expense else 0.0
        warning = stressed_cov < 1.0
        data = {
            "interest_coverage": round(interest_cov, 3),
            "fixed_charge_coverage": round(fixed_charge_cov, 3),
            "stressed_interest_coverage": round(stressed_cov, 3),
            "stress_decline_pct": stress_decline_pct,
            "breach_warning": warning,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("interest_coverage_ratio", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
