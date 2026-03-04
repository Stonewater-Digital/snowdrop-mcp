"""Authorize agents for skill execution based on tier."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "access_control_checker",
    "description": "Validates tier permissions across Snowdrop skills.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "agent_id": {"type": "string"},
            "requested_skill": {"type": "string"},
            "agent_tier": {
                "type": "string",
                "enum": ["free", "premium", "franchise"],
            },
        },
        "required": ["agent_id", "requested_skill", "agent_tier"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "authorized": {"type": "boolean"},
                    "reason": {"type": "string"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}

GOODWILL_PREFIXES = ("goodwill", "community", "info_")
FINANCIAL_PREFIXES = ("fund_", "capital_", "ghost_", "mercury", "billing_", "payment")


def access_control_checker(
    agent_id: str,
    requested_skill: str,
    agent_tier: str,
    **_: Any,
) -> dict[str, Any]:
    """Determine whether the agent may run the requested skill."""

    try:
        skill = requested_skill.lower()
        tier = agent_tier.lower()
        if tier not in {"free", "premium", "franchise"}:
            raise ValueError("agent_tier must be free, premium, or franchise")

        if tier == "franchise":
            authorized = True
            reason = "Franchise operators have full access."
        elif tier == "premium":
            authorized = not skill.startswith(FINANCIAL_PREFIXES)
            reason = (
                "Premium tier cannot execute core financial controls"
                if not authorized
                else "Skill cleared for premium tier."
            )
        else:
            authorized = skill.startswith(GOODWILL_PREFIXES)
            reason = (
                "Free tier restricted to Goodwill Cask"
                if authorized
                else "Free tier lacks permission for this skill"
            )

        return {
            "status": "success",
            "data": {"authorized": authorized, "reason": reason},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("access_control_checker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    """Append a Ralph Wiggum lesson entry."""

    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
