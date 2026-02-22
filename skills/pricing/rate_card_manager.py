"""Manage Watering Hole tier pricing."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "rate_card_manager",
    "description": "Retrieves or updates tier pricing for Watering Hole skills.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["get", "set", "calculate"],
            },
            "tier": {
                "type": "string",
                "enum": ["free", "standard", "premium", "franchise"],
            },
            "skill_name": {"type": "string"},
            "price_per_call": {"type": "number"},
        },
        "required": ["operation", "tier"],
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


_RATE_CARD: dict[str, dict[str, Any]] = {
    "free": {"range": (0.0, 0.0), "skills": {"goodwill_cask": 0.0}},
    "standard": {"range": (0.01, 0.05), "skills": {}},
    "premium": {"range": (0.05, 0.25), "skills": {}},
    "franchise": {"range": (0.25, 1.0), "skills": {}},
}


def rate_card_manager(
    operation: str,
    tier: str,
    skill_name: str | None = None,
    price_per_call: float | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Handle tier pricing get/set/calculate operations."""
    try:
        tier = tier.lower()
        if tier not in _RATE_CARD:
            raise ValueError("Unsupported tier")
        operation = operation.lower()
        tier_data = _RATE_CARD[tier]

        if operation == "get":
            data = {"tier": tier, **tier_data}
        elif operation == "set":
            if not skill_name:
                raise ValueError("skill_name required for set operation")
            if price_per_call is None:
                raise ValueError("price_per_call required for set operation")
            tier_data["skills"][skill_name] = round(price_per_call, 4)
            data = {"tier": tier, "skill_name": skill_name, "price_per_call": tier_data["skills"][skill_name]}
        elif operation == "calculate":
            if not skill_name:
                raise ValueError("skill_name required for calculate operation")
            price = tier_data["skills"].get(skill_name)
            if price is None:
                low, high = tier_data["range"]
                price = round((low + high) / 2, 4)
            data = {"tier": tier, "skill_name": skill_name, "price_per_call": price}
        else:
            raise ValueError("operation must be get, set, or calculate")

        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("rate_card_manager", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
