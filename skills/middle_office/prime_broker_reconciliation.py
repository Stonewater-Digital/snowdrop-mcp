"""Prime broker reconciliation tool."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "prime_broker_reconciliation",
    "description": "Reconciles positions and cash between internal books and the prime broker.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "internal_positions": {"type": "array", "items": {"type": "object"}},
            "pb_positions": {"type": "array", "items": {"type": "object"}},
            "internal_cash": {"type": "number"},
            "pb_cash": {"type": "number"},
        },
        "required": ["internal_positions", "pb_positions", "internal_cash", "pb_cash"],
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


def _positions_to_dict(positions: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    mapping: dict[str, dict[str, float]] = {}
    for row in positions or []:
        sid = str(row.get("security_id"))
        mapping[sid] = {
            "quantity": float(row.get("quantity", 0.0)),
            "market_value": float(row.get("market_value", 0.0)),
        }
    return mapping


def prime_broker_reconciliation(
    internal_positions: list[dict[str, Any]],
    pb_positions: list[dict[str, Any]],
    internal_cash: float,
    pb_cash: float,
    **_: Any,
) -> dict[str, Any]:
    """Return breaks and reconciliation summary."""
    try:
        internal = _positions_to_dict(internal_positions)
        broker = _positions_to_dict(pb_positions)
        securities = set(internal) | set(broker)
        breaks: list[dict[str, Any]] = []
        total_break_mv = 0.0
        for sec in sorted(securities):
            internal_row = internal.get(sec, {"quantity": 0.0, "market_value": 0.0})
            broker_row = broker.get(sec, {"quantity": 0.0, "market_value": 0.0})
            quantity_diff = internal_row["quantity"] - broker_row["quantity"]
            value_diff = internal_row["market_value"] - broker_row["market_value"]
            if quantity_diff or value_diff:
                breaks.append(
                    {
                        "security_id": sec,
                        "quantity_diff": round(quantity_diff, 6),
                        "market_value_diff": round(value_diff, 2),
                    }
                )
                total_break_mv += abs(value_diff)
        cash_break = internal_cash - pb_cash
        status = "balanced"
        if breaks or cash_break:
            status = "breaks_found"
        data = {
            "position_breaks": breaks,
            "cash_break": round(cash_break, 2),
            "total_break_count": len(breaks) + (1 if cash_break else 0),
            "total_break_market_value": round(total_break_mv, 2),
            "reconciliation_status": status,
        }
        return {"status": "ok", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        try:
            with open("logs/lessons.md", "a") as _f:
                _f.write(f"- [{datetime.now(timezone.utc).isoformat()}] prime_broker_reconciliation: {exc}\n")
        except OSError:
            pass
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
