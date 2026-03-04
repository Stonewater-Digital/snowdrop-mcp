"""
Executive Summary: Ranks API credentials by rotation age and outputs actionable rotation tasks with escalation hooks.

Inputs: credentials (list[dict]), notify_thunder (bool, optional)
Outputs: status (str), data (tasks/summary), timestamp (str)
MCP Tool Name: api_credential_rotator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from skills.utils import (
    SkillTelemetryEmitter,
    get_iso_timestamp,
    logger,
    log_lesson as _shared_log_lesson,
)

TOOL_META: dict[str, Any] = {
    "name": "api_credential_rotator",
    "description": "Generates rotation tasks for API keys/secrets using age vs. policy frequency.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "credentials": {
                "type": "array",
                "items": {"type": "object"},
                "description": "Credential entries with name, owner, last_rotated_at, rotation_frequency_days, criticality.",
            },
            "notify_thunder": {
                "type": "boolean",
                "default": False,
                "description": "Send Thunder alert when overdue credentials are found.",
            },
        },
        "required": ["credentials"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["ok", "error"]},
            "data": {
                "type": "object",
                "properties": {
                    "tasks": {"type": "array", "items": {"type": "object"}},
                    "summary": {"type": "object"},
                },
            },
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def api_credential_rotator(
    credentials: list[dict[str, Any]],
    notify_thunder: bool = False,
) -> dict[str, Any]:
    """Prepare rotation tasks for API credentials."""
    emitter = SkillTelemetryEmitter(
        "api_credential_rotator",
        {"credentials": len(credentials or [])},
    )
    try:
        if not credentials:
            raise ValueError("credentials cannot be empty")

        tasks: list[dict[str, Any]] = []
        overdue = 0
        now = datetime.now(timezone.utc)

        for cred in credentials:
            name = str(cred.get("name") or "unknown")
            owner = cred.get("owner") or "ops"
            last_rotated = _parse_timestamp(cred.get("last_rotated_at"))
            frequency = int(cred.get("rotation_frequency_days") or 90)
            criticality = str(cred.get("criticality") or "standard").lower()

            days_since = (now - last_rotated).days if last_rotated else frequency + 1
            overdue_days = days_since - frequency
            status = "overdue" if overdue_days > 0 else "due" if days_since > frequency * 0.8 else "ok"
            if status == "overdue":
                overdue += 1

            tasks.append(
                {
                    "credential": name,
                    "owner": owner,
                    "days_since_rotation": days_since,
                    "rotation_frequency_days": frequency,
                    "status": status,
                    "criticality": criticality,
                    "recommended_action": "rotate_immediately" if status == "overdue" else "schedule",
                }
            )

        summary = {
            "total_credentials": len(credentials),
            "overdue": overdue,
        }
        emitter.record("ok", summary)

        if notify_thunder and overdue:
            _notify_thunder(f"{overdue} API credentials overdue for rotation.", severity="WARNING")

        return {"status": "ok", "data": {"tasks": tasks, "summary": summary}, "timestamp": get_iso_timestamp()}
    except Exception as exc:  # noqa: BLE001
        logger.error(f"api_credential_rotator failed: {exc}")
        _log_lesson("api_credential_rotator", str(exc))
        emitter.record("error", {"error": str(exc)})
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": get_iso_timestamp()}


def _parse_timestamp(raw: Any) -> datetime:
    """Parse timestamp or return epoch fallback."""
    if not raw:
        return datetime.fromtimestamp(0, tz=timezone.utc)
    value = str(raw).replace("Z", "+00:00")
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def _notify_thunder(message: str, *, severity: str) -> None:
    """Send Thunder alert with fallback logging."""
    try:
        from skills.thunder_signal import thunder_signal

        thunder_signal(severity=severity, message=message)
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"api_credential_rotator alert failed: {exc}")


def _log_lesson(skill_name: str, error: str) -> None:
    """Proxy shared lesson logger."""
    _shared_log_lesson(skill_name, error)
