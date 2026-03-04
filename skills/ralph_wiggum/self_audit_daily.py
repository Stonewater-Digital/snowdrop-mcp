"""Daily self-audit skill per ethics mandate."""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "self_audit_daily",
    "description": "Compares planned vs executed actions, logs discrepancies, and triggers freezes if needed.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "planned_actions": {"type": "array", "items": {"type": "object"}},
            "executed_actions": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["planned_actions", "executed_actions"],
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

_AUDIT_LOG = "logs/daily_audit.jsonl"


def self_audit_daily(
    planned_actions: list[dict[str, Any]],
    executed_actions: list[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    """Return audit metrics and append to audit log."""
    try:
        if not planned_actions:
            raise ValueError("planned_actions cannot be empty")

        expected_value = sum(float(action.get("expected_value", 0.0)) for action in planned_actions)
        actual_value = sum(float(action.get("actual_value", 0.0)) for action in executed_actions)
        completed = sum(1 for action in executed_actions if action.get("status") == "completed")
        completion_rate = completed / len(planned_actions)
        discrepancy = 0.0 if expected_value == 0 else (actual_value - expected_value) / expected_value
        alerts = {
            "freeze_wallets": abs(discrepancy) > 0.01,
            "alert_thunder": abs(discrepancy) > 0.01,
        }
        audit_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "planned_actions": planned_actions,
            "executed_actions": executed_actions,
            "completion_rate": completion_rate,
            "value_discrepancy_pct": discrepancy * 100,
            "alerts": alerts,
        }
        _append_audit_record(audit_record)
        data = {
            "completion_rate": round(completion_rate * 100, 2),
            "value_discrepancy_pct": round(discrepancy * 100, 2),
            **alerts,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": audit_record["timestamp"],
        }
    except Exception as exc:
        _log_lesson("self_audit_daily", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _append_audit_record(record: dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(_AUDIT_LOG), exist_ok=True)
    with open(_AUDIT_LOG, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(record) + "\n")


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
