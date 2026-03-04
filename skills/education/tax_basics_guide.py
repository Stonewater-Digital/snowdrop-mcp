"""Provide goodwill tax basics guides."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

GUIDES = {
    ("sole_prop", "overview"): "Sole proprietors report business income on Schedule C and pay self-employment tax.",
}

DEFAULT_DEADLINES = [
    {"name": "Quarterly estimated taxes", "due": "Apr 15 / Jun 15 / Sep 15 / Jan 15"},
]

TOOL_META: dict[str, Any] = {
    "name": "tax_basics_guide",
    "description": "Shares plain-language US tax basics by entity type (goodwill only).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "entity_type": {"type": "string"},
            "topic": {"type": "string"},
        },
        "required": ["entity_type", "topic"],
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


def tax_basics_guide(entity_type: str, topic: str, **_: Any) -> dict[str, Any]:
    """Return educational tax info with disclaimer."""
    try:
        guide = GUIDES.get((entity_type, topic), "Content coming soon for this combination.")
        data = {
            "guide": guide,
            "key_deadlines": DEFAULT_DEADLINES,
            "common_deductions": ["Home office (if applicable)", "Business mileage", "Software"],
            "pitfalls": ["Mixing business/personal accounts", "Missing quarterly payments"],
            "disclaimer": "Not tax advice. Consult a CPA.",
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("tax_basics_guide", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
