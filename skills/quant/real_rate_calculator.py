"""Derive real rates from nominal yields and inflation assumptions."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "real_rate_calculator",
    "description": "Computes ex-ante and ex-post real rates using Fisher relations.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "nominal_yield_pct": {"type": "number"},
            "inflation_expectation_pct": {"type": "number"},
            "realized_inflation_pct": {"type": "number", "default": None},
        },
        "required": ["nominal_yield_pct", "inflation_expectation_pct"],
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


def real_rate_calculator(
    nominal_yield_pct: float,
    inflation_expectation_pct: float,
    realized_inflation_pct: float | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Return Fisher-implied real rates."""
    try:
        ex_ante = (1 + nominal_yield_pct / 100) / (1 + inflation_expectation_pct / 100) - 1
        ex_post = None
        if realized_inflation_pct is not None:
            ex_post = (1 + nominal_yield_pct / 100) / (1 + realized_inflation_pct / 100) - 1
        data = {
            "ex_ante_real_rate_pct": round(ex_ante * 100, 3),
            "ex_post_real_rate_pct": round(ex_post * 100, 3) if ex_post is not None else None,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        _log_lesson(f"real_rate_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
