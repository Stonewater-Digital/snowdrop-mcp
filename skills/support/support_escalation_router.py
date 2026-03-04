"""Route support tickets based on complexity and tier."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "support_escalation_router",
    "description": "Determines routing paths for support tickets based on category, tier, and urgency.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "ticket": {"type": "object"},
        },
        "required": ["ticket"],
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


ROUTES = {
    "billing": "billing_auto_queue",
    "technical": "engineering_triage",
    "access": "accounts_team",
    "feature": "product_backlog",
    "other": "general_support",
}


def support_escalation_router(ticket: dict[str, Any], **_: Any) -> dict[str, Any]:
    """Return the routing decision for a ticket."""
    try:
        category = ticket.get("category", "other")
        priority = ticket.get("priority", "medium")
        agent_tier = ticket.get("agent_tier", "community")
        auto_resolve_attempted = ticket.get("auto_resolve_attempted", False)
        routed_to = ROUTES.get(category, "general_support")
        auto_resolved = False
        auto_response = None
        if category == "billing" and ticket.get("description", "").lower().startswith("how do i pay"):
            auto_resolved = True
            auto_response = "Sent billing FAQ article"
            routed_to = "auto_resolve"
        elif priority == "urgent":
            routed_to = "thunder_alert"
        elif category == "technical" and agent_tier in {"premium", "ambassador"}:
            routed_to = "priority_engineering"
        elif category == "feature":
            routed_to = "product_backlog"
        estimated_response = _estimate_response_time(priority, routed_to)
        data = {
            "routed_to": routed_to,
            "auto_resolved": auto_resolved,
            "auto_response": auto_response,
            "estimated_response_time": estimated_response,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("support_escalation_router", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _estimate_response_time(priority: str, routed_to: str) -> str:
    if routed_to == "thunder_alert":
        return "15m"
    mapping = {
        "urgent": "1h",
        "high": "4h",
        "medium": "24h",
        "low": "72h",
    }
    return mapping.get(priority, "48h")


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
