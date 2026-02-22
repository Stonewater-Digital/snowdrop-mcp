"""Produce a Markdown listing for skill marketplace registration."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "skill_marketplace_listing",
    "description": "Turns the skill registry into a Moltbook/Fragment-friendly markdown listing.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "skill_registry": {
                "type": "object",
                "description": "Mapping of skill names to descriptions.",
            }
        },
        "required": ["skill_registry"],
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


def skill_marketplace_listing(skill_registry: dict[str, str], **_: Any) -> dict[str, Any]:
    """Return a markdown doc with categorized pricing tiers.

    Args:
        skill_registry: Mapping of skill names to short descriptions.

    Returns:
        Envelope containing markdown text for the Moltbook/Fragment listing.
    """

    try:
        categories: dict[str, list[str]] = {}
        for name, description in skill_registry.items():
            category = name.split("_")[0].title()
            tier = _price_tier(name)
            entry = f"- **{name}** ({tier}) — {description}"
            categories.setdefault(category, []).append(entry)

        lines = ["# Snowdrop Skill Marketplace", "Generated: " + datetime.now(timezone.utc).isoformat()]
        for category, entries in sorted(categories.items()):
            lines.append(f"\n## {category}")
            lines.extend(entries)

        markdown = "\n".join(lines) + "\n"
        return {
            "status": "success",
            "data": {"skill_markdown": markdown},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("skill_marketplace_listing", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _price_tier(name: str) -> str:
    lower = name.lower()
    if any(keyword in lower for keyword in ("nav", "agent", "opus", "railway")):
        return "premium"
    if any(keyword in lower for keyword in ("report", "budget", "audit")):
        return "standard"
    return "exploratory"


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
