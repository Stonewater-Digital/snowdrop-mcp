"""Validate external agent onboarding requirements."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "agent_onboarding_validator",
    "description": "Checks VC freshness, capability alignment, and bad-actor lists before onboarding.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "agent_id": {"type": "string"},
            "declared_capabilities": {"type": "array", "items": {"type": "string"}},
            "verifiable_credential": {"type": ["object", "null"]},
            "requested_tier": {"type": "string"},
        },
        "required": ["agent_id", "declared_capabilities"],
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

_BAD_ACTORS = {"darkpool_alpha", "rugpull_bot"}
_KNOWN_CAPABILITIES = {
    "fund_accounting",
    "treasury_ops",
    "tax_planning",
    "fx",
    "memory_ops",
    "swarm_coordination",
}


def agent_onboarding_validator(
    agent_id: str,
    declared_capabilities: list[str],
    verifiable_credential: dict[str, Any] | None = None,
    requested_tier: str | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Apply onboarding policy checks and return approval conditions."""
    try:
        if agent_id.lower() in _BAD_ACTORS:
            raise ValueError("Agent on prohibited list — auto reject")

        conditions: list[str] = []
        approved = True
        assigned_tier = requested_tier or _tier_from_capabilities(declared_capabilities)

        if verifiable_credential is None:
            approved = False
            conditions.append("Provide verifiable credential (A2A compliant)")
        else:
            expires_at = verifiable_credential.get("expires_at")
            if not expires_at:
                approved = False
                conditions.append("Credential missing expires_at")
            else:
                expiry = datetime.fromisoformat(str(expires_at)).replace(tzinfo=timezone.utc)
                if expiry <= datetime.now(timezone.utc):
                    approved = False
                    conditions.append("Credential expired")

        invalid_caps = [cap for cap in declared_capabilities if cap not in _KNOWN_CAPABILITIES]
        if invalid_caps:
            approved = False
            conditions.append(f"Unknown capabilities: {', '.join(invalid_caps)}")

        data = {
            "approved": approved,
            "assigned_tier": assigned_tier,
            "conditions": conditions,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("agent_onboarding_validator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _tier_from_capabilities(capabilities: list[str]) -> str:
    count = len(set(capabilities))
    if count >= 5:
        return "alpha"
    if count >= 3:
        return "beta"
    return "gamma"


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
