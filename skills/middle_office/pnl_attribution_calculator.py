"""Decompose P&L into drivers."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "pnl_attribution_calculator",
    "description": "Breaks daily P&L into price, carry, FX, and fee components.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "price_pnl": {"type": "number"},
            "carry_pnl": {"type": "number"},
            "fx_pnl": {"type": "number"},
            "fee_pnl": {"type": "number"},
        },
        "required": ["price_pnl", "carry_pnl", "fx_pnl", "fee_pnl"],
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def pnl_attribution_calculator(
    price_pnl: float,
    carry_pnl: float,
    fx_pnl: float,
    fee_pnl: float,
    **_: Any,
) -> dict[str, Any]:
    """Return P&L contributions."""
    try:
        total = price_pnl + carry_pnl + fx_pnl + fee_pnl
        contributions = {
            "price": price_pnl,
            "carry": carry_pnl,
            "fx": fx_pnl,
            "fees": fee_pnl,
        }
        pct = {key: round(value / total * 100, 2) if total else 0.0 for key, value in contributions.items()}
        data = {
            "total_pnl": round(total, 2),
            "contribution_pct": pct,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("pnl_attribution_calculator", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
