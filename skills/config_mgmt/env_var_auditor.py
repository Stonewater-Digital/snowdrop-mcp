"""Audit environment variables against template requirements."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "env_var_auditor",
    "description": "Finds missing, empty, and extra environment variables relative to .env.template.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "template_vars": {"type": "array", "items": {"type": "string"}},
            "set_vars": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["template_vars", "set_vars"],
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


def env_var_auditor(
    template_vars: list[str],
    set_vars: list[Any],
    **_: Any,
) -> dict[str, Any]:
    """Return readiness summary for environment variables."""
    try:
        template_set = {var for var in template_vars}
        normalized: dict[str, bool] = {}
        for entry in set_vars:
            if isinstance(entry, dict):
                name = str(entry.get("name"))
                value = entry.get("value")
                normalized[name] = bool(value)
            else:
                normalized[str(entry)] = True
        missing = sorted(template_set - normalized.keys())
        extra = sorted(name for name in normalized.keys() if name not in template_set)
        empty = sorted(name for name, has_value in normalized.items() if not has_value)
        satisfied = len(template_set) - len(missing) - len(empty)
        completion_pct = satisfied / len(template_set) if template_set else 1.0
        ready = completion_pct == 1.0 and not empty
        data = {
            "ready": ready,
            "missing": missing,
            "empty": empty,
            "extra": extra,
            "completion_pct": round(completion_pct * 100, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("env_var_auditor", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
