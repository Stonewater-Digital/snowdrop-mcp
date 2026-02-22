"""Validate partner onboarding readiness."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "partner_onboarding_validator",
    "description": "Ensures partner submissions meet baseline technical and compliance requirements.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "partner": {"type": "object"},
        },
        "required": ["partner"],
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


REQUIRED_FIELDS = ["name", "type", "technical_contact", "integration_type"]


def partner_onboarding_validator(partner: dict[str, Any], **_: Any) -> dict[str, Any]:
    """Return approval decision with onboarding steps."""
    try:
        missing = [field for field in REQUIRED_FIELDS if field not in partner]
        blockers: list[str] = []
        if missing:
            blockers.append(f"Missing fields: {', '.join(missing)}")
        tier = partner.get("type")
        integration_type = partner.get("integration_type")
        if tier in {"integration", "strategic"} and not partner.get("security_audit_passed"):
            blockers.append("Security audit required for technical partners")
        if integration_type not in {"mcp", "a2a", "webhook"}:
            blockers.append("Unsupported integration_type")
        approved = len(blockers) == 0
        onboarding_steps = [
            "Sign data processing addendum",
            "Provision sandbox keys",
            "Run joint QA",
        ]
        partner_id = str(uuid.uuid4()) if approved else None
        data = {
            "approved": approved,
            "partner_id": partner_id,
            "onboarding_steps": onboarding_steps,
            "blockers": blockers,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("partner_onboarding_validator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
