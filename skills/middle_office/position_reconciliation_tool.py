"""Reconcile internal versus broker positions."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "position_reconciliation_tool",
    "description": "Compares internal books with prime broker files and flags breaks.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "internal_positions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {"symbol": {"type": "string"}, "quantity": {"type": "number"}},
                    "required": ["symbol", "quantity"],
                },
            },
            "broker_positions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {"symbol": {"type": "string"}, "quantity": {"type": "number"}},
                    "required": ["symbol", "quantity"],
                },
            },
        },
        "required": ["internal_positions", "broker_positions"],
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def position_reconciliation_tool(
    internal_positions: list[dict[str, Any]],
    broker_positions: list[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    """Return position breaks."""
    try:
        internal_map = {pos["symbol"]: pos.get("quantity", 0.0) for pos in internal_positions}
        broker_map = {pos["symbol"]: pos.get("quantity", 0.0) for pos in broker_positions}
        symbols = set(internal_map) | set(broker_map)
        breaks = []
        for symbol in sorted(symbols):
            internal_qty = internal_map.get(symbol, 0.0)
            broker_qty = broker_map.get(symbol, 0.0)
            diff = internal_qty - broker_qty
            if abs(diff) > 1e-6:
                breaks.append({"symbol": symbol, "internal": internal_qty, "broker": broker_qty, "difference": round(diff, 2)})
        data = {
            "breaks": breaks,
            "break_rate_pct": round(len(breaks) / len(symbols) * 100, 2) if symbols else 0.0,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("position_reconciliation_tool", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
