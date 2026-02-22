"""Route incidents to appropriate responders and auto-actions."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "incident_escalation_router",
    "description": "Determines escalation targets and automatic guardrails based on severity.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "incident": {
                "type": "object",
                "description": "Incident payload including severity, affected systems, and domain.",
            },
            "escalation_policy": {
                "type": "object",
                "description": "Optional override for severity routing rules.",
            },
        },
        "required": ["incident"],
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


_DEFAULT_POLICY = {
    "sev1": ["Thunder"],
    "sev2": ["Thunder", "Telnyx"],
    "sev3": ["Telegram"],
    "sev4": ["log_only"],
}
_DOMAIN_ACTIONS = {
    "financial": ["transaction_freeze"],
    "security": ["rotate_api_keys", "initiate_forensics"],
    "infrastructure": ["scale_backup_region"],
    "data": ["snapshot_warehouse"],
}
_CHANNEL_MAP = {
    "financial": "pagerduty",
    "security": "signal",
    "infrastructure": "ops_chat",
    "data": "data_eng",
}


def incident_escalation_router(
    incident: dict[str, Any],
    escalation_policy: dict[str, Any] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Determine escalation recipients and actions for an incident."""
    try:
        severity = str(incident.get("severity", "sev3")).lower()
        domain = str(incident.get("domain", "general")).lower()
        systems = incident.get("affected_systems", []) or []
        policy = {**_DEFAULT_POLICY, **(escalation_policy or {})}
        notify_targets = policy.get(severity, ["log_only"])

        notify_payload = [
            {
                "channel": _CHANNEL_MAP.get(domain, "ops_center"),
                "recipient": target,
                "systems": systems,
            }
            for target in notify_targets
        ]

        severity_levels = {"sev1": 4, "sev2": 3, "sev3": 2, "sev4": 1}
        escalation_level = severity_levels.get(severity, 2)
        auto_actions = list(_DOMAIN_ACTIONS.get(domain, []))
        if severity == "sev1" and "financial" in domain:
            auto_actions.append("notify_regulators")
        if severity in {"sev1", "sev2"}:
            auto_actions.append("open_war_room")

        data = {
            "notify": notify_payload,
            "escalation_level": escalation_level,
            "auto_actions": auto_actions,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("incident_escalation_router", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
