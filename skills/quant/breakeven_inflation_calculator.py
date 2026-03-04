"""Compute breakeven inflation versus TIPS."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "breakeven_inflation_calculator",
    "description": "Calculates breakeven inflation and adjusts for risk premium assumptions.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "nominal_yield_pct": {"type": "number"},
            "tips_yield_pct": {"type": "number"},
            "inflation_risk_premium_bps": {"type": "number", "default": 20.0},
        },
        "required": ["nominal_yield_pct", "tips_yield_pct"],
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


def breakeven_inflation_calculator(
    nominal_yield_pct: float,
    tips_yield_pct: float,
    inflation_risk_premium_bps: float = 20.0,
    **_: Any,
) -> dict[str, Any]:
    """Return raw and adjusted breakeven inflation."""
    try:
        breakeven = nominal_yield_pct - tips_yield_pct
        adjusted = breakeven - inflation_risk_premium_bps / 100
        data = {
            "breakeven_inflation_pct": round(breakeven, 3),
            "adjusted_breakeven_pct": round(adjusted, 3),
            "risk_premium_bps": inflation_risk_premium_bps,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        _log_lesson(f"breakeven_inflation_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
