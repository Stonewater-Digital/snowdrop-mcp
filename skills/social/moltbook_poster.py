"""Generate Moltbook marketplace listings."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "moltbook_poster",
    "description": "Formats Snowdrop skills for the Moltbook agent marketplace.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "skill_name": {"type": "string"},
            "description": {"type": "string"},
            "price_usd": {"type": "number"},
            "category": {"type": "string"},
        },
        "required": ["skill_name", "description", "price_usd", "category"],
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


def moltbook_poster(
    skill_name: str,
    description: str,
    price_usd: float,
    category: str,
    **_: Any,
) -> dict[str, Any]:
    """Return a listing payload ready for submission.

    Args:
        skill_name: Name of the skill being marketed.
        description: Marketing copy or summary.
        price_usd: Asking price in USD for the skill.
        category: Moltbook category tag.

    Returns:
        Envelope containing the listing payload.
    """

    try:
        payload = {
            "skill": skill_name,
            "category": category,
            "description": description,
            "pricing": {
                "amount": round(price_usd, 2),
                "currency": "USD",
                "status": "pending_thunder_approval",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        return {
            "status": "success",
            "data": {"listing": payload},
            "timestamp": payload["timestamp"],
        }
    except Exception as exc:
        _log_lesson("moltbook_poster", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
