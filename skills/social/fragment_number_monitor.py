"""Monitor Fragment.com +888 listings."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "fragment_number_monitor",
    "description": "Filters Fragment number listings by prefix and budget.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "target_prefix": {"type": "string"},
            "max_price_ton": {"type": "number"},
            "listings": {
                "type": "array",
                "items": {"type": "object"},
                "description": "Optional cached listings to scan.",
            },
        },
        "required": ["target_prefix", "max_price_ton"],
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


def fragment_number_monitor(
    target_prefix: str,
    max_price_ton: float,
    listings: list[dict[str, Any]] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Return listings that match prefix/budget criteria.

    Args:
        target_prefix: Desired number prefix (e.g., "+888").
        max_price_ton: Maximum TON price willing to monitor.
        listings: Optional cached listing payload to evaluate.

    Returns:
        Envelope summarizing matching listings with read-only status.
    """

    try:
        filtered = []
        for listing in listings or []:
            number = str(listing.get("number") or listing.get("id") or "")
            price = float(listing.get("price_ton", 0) or 0)
            if number.startswith(target_prefix) and price <= max_price_ton:
                filtered.append({
                    "number": number,
                    "price_ton": price,
                    "available": listing.get("available", True),
                })

        data = {
            "target_prefix": target_prefix,
            "max_price_ton": max_price_ton,
            "matches": filtered,
            "search_status": "read_only",
        }

        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("fragment_number_monitor", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
