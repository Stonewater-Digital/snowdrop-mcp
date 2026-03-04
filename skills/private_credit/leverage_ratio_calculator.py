"""Compute leverage ratios for private credit borrowers."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "leverage_ratio_calculator",
    "description": "Calculates gross, net, and senior leverage metrics versus targets.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "total_debt": {"type": "number"},
            "senior_debt": {"type": "number"},
            "cash_balance": {"type": "number"},
            "ebitda": {"type": "number"},
            "target_total_leverage": {"type": "number", "default": 5.0},
            "target_senior_leverage": {"type": "number", "default": 3.0},
        },
        "required": ["total_debt", "senior_debt", "cash_balance", "ebitda"],
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


def leverage_ratio_calculator(
    total_debt: float,
    senior_debt: float,
    cash_balance: float,
    ebitda: float,
    target_total_leverage: float = 5.0,
    target_senior_leverage: float = 3.0,
    **_: Any,
) -> dict[str, Any]:
    """Return leverage and covenant headroom metrics."""
    try:
        gross_leverage = total_debt / ebitda if ebitda else 0.0
        senior_leverage = senior_debt / ebitda if ebitda else 0.0
        net_leverage = (total_debt - cash_balance) / ebitda if ebitda else 0.0
        total_headroom = target_total_leverage - gross_leverage
        senior_headroom = target_senior_leverage - senior_leverage
        data = {
            "gross_leverage": round(gross_leverage, 2),
            "senior_leverage": round(senior_leverage, 2),
            "net_leverage": round(net_leverage, 2),
            "total_headroom": round(total_headroom, 2),
            "senior_headroom": round(senior_headroom, 2),
            "covenant_warning": total_headroom < 0 or senior_headroom < 0,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("leverage_ratio_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
