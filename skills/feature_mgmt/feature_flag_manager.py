"""Manage Snowdrop feature flags with tier/date evaluations."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "feature_flag_manager",
    "description": "Gets, sets, lists, or evaluates feature flags stored in config/feature_flags.json.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["get", "set", "list", "evaluate"],
            },
            "flag_name": {"type": "string"},
            "value": {"type": "boolean"},
            "context": {"type": "object"},
        },
        "required": ["operation"],
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


_FLAG_PATH = Path("config/feature_flags.json")


def feature_flag_manager(
    operation: str,
    flag_name: str | None = None,
    value: bool | None = None,
    context: dict[str, Any] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Perform CRUD-like operations on feature flags."""
    try:
        flags = _load_flags()
        operation = operation.lower()
        data: dict[str, Any]

        if operation == "list":
            data = flags
        elif operation == "get":
            if not flag_name:
                raise ValueError("flag_name required for get operation")
            data = {flag_name: flags.get(flag_name)}
        elif operation == "set":
            if not flag_name:
                raise ValueError("flag_name required for set operation")
            flag_entry = flags.get(flag_name, {})
            if value is not None:
                flag_entry["enabled"] = value
            flags[flag_name] = flag_entry
            _write_flags(flags)
            data = {flag_name: flag_entry}
        elif operation == "evaluate":
            if not flag_name:
                raise ValueError("flag_name required for evaluate operation")
            flag_entry = flags.get(flag_name, {})
            evaluation = _evaluate_flag(flag_entry, context or {})
            data = {"flag_name": flag_name, **evaluation}
        else:
            raise ValueError("operation must be get, set, list, or evaluate")

        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("feature_flag_manager", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _load_flags() -> dict[str, Any]:
    if not _FLAG_PATH.exists():
        return {}
    content = _FLAG_PATH.read_text(encoding="utf-8")
    return json.loads(content) if content else {}


def _write_flags(flags: dict[str, Any]) -> None:
    _FLAG_PATH.parent.mkdir(parents=True, exist_ok=True)
    _FLAG_PATH.write_text(json.dumps(flags, indent=2), encoding="utf-8")


def _evaluate_flag(flag_entry: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    enabled = bool(flag_entry.get("enabled", False))
    tiers = flag_entry.get("tiers") or []
    activate_after = flag_entry.get("activate_after")
    agent_tier = str(context.get("agent_tier", ""))
    now = context.get("date")
    current_time = _parse_time(now) if now else datetime.now(timezone.utc)

    if tiers and agent_tier and agent_tier not in tiers:
        enabled = False
    if activate_after:
        activate_dt = _parse_time(activate_after)
        if current_time < activate_dt:
            enabled = False

    return {
        "enabled": enabled,
        "flag": flag_entry,
        "context": context,
    }


def _parse_time(value: str | datetime) -> datetime:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:  # noqa: B904
        raise ValueError(f"Invalid datetime: {value}") from exc
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
