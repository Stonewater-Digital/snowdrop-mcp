"""Track trade lifecycle milestones and aging."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "trade_lifecycle_tracker",
    "description": "Summarizes trade lifecycle stages with elapsed times and bottlenecks.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "trades": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "trade_id": {"type": "string"},
                        "execution_ts": {"type": "string"},
                        "allocation_ts": {"type": "string"},
                        "confirmation_ts": {"type": "string"},
                        "settlement_ts": {"type": "string"},
                    },
                    "required": ["trade_id", "execution_ts"],
                },
            }
        },
        "required": ["trades"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def trade_lifecycle_tracker(trades: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return lifecycle durations and outstanding steps."""
    try:
        summaries = []
        for trade in trades:
            execution = _parse_time(trade.get("execution_ts"))
            allocation = _parse_time(trade.get("allocation_ts"))
            confirmation = _parse_time(trade.get("confirmation_ts"))
            settlement = _parse_time(trade.get("settlement_ts"))
            now = datetime.now(timezone.utc)
            cycle_time = ((settlement or now) - execution).total_seconds() / 3600 if execution else 0.0
            outstanding_stage = "settled" if settlement else "confirmation" if confirmation else "allocation" if allocation else "execution"
            summaries.append(
                {
                    "trade_id": trade.get("trade_id"),
                    "cycle_hours": round(cycle_time, 2),
                    "outstanding_stage": outstanding_stage,
                }
            )
        data = {"trades": summaries}
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("trade_lifecycle_tracker", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        cleaned = value.replace("Z", "+00:00")
        return datetime.fromisoformat(cleaned)
    except ValueError:
        return None


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
