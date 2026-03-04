"""Track failed settlements and associated costs."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "settlement_fail_tracker",
    "description": "Ages failed trades and estimates fail penalties.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "fails": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "trade_id": {"type": "string"},
                        "expected_settle": {"type": "string"},
                        "notional": {"type": "number"},
                        "fail_rate_bps": {"type": "number"},
                    },
                    "required": ["trade_id", "expected_settle", "notional", "fail_rate_bps"],
                },
            }
        },
        "required": ["fails"],
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def settlement_fail_tracker(fails: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return fail aging and penalty estimates."""
    try:
        today = datetime.now(timezone.utc)
        results = []
        total_penalty = 0.0
        for fail in fails:
            settle_date = _parse_date(fail.get("expected_settle"))
            days = (today - settle_date).days if settle_date else 0
            penalty = fail.get("notional", 0.0) * (fail.get("fail_rate_bps", 0.0) / 10000) * days / 360
            total_penalty += penalty
            results.append(
                {
                    "trade_id": fail.get("trade_id"),
                    "days_outstanding": days,
                    "penalty": round(penalty, 2),
                }
            )
        data = {
            "fails": results,
            "total_penalty": round(total_penalty, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("settlement_fail_tracker", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _parse_date(value: str | None) -> datetime:
    reference = datetime.now(timezone.utc)
    if not value:
        return reference
    cleaned = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(cleaned)
    except ValueError:
        return reference


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
