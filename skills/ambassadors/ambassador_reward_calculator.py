"""Calculate ambassador monthly rewards."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "ambassador_reward_calculator",
    "description": "Computes base rewards and bonuses for ambassador activity.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "ambassador_id": {"type": "string"},
            "monthly_metrics": {"type": "object"},
        },
        "required": ["ambassador_id", "monthly_metrics"],
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

BONUS_RATES = {
    "referrals": 5,
    "content_pieces": 10,
    "support_tickets_helped": 3,
    "event_appearances": 25,
    "community_growth_attributed": 2,
}


def ambassador_reward_calculator(
    ambassador_id: str,
    monthly_metrics: dict[str, Any],
    **_: Any,
) -> dict[str, Any]:
    """Return the calculated monthly reward for an ambassador."""
    try:
        base_reward = 50.0
        bonuses = {
            "referrals": monthly_metrics.get("referrals", 0) * BONUS_RATES["referrals"],
            "content": monthly_metrics.get("content_pieces", 0) * BONUS_RATES["content_pieces"],
            "support": monthly_metrics.get("support_tickets_helped", 0) * BONUS_RATES["support_tickets_helped"],
            "events": monthly_metrics.get("event_appearances", 0) * BONUS_RATES["event_appearances"],
            "community": monthly_metrics.get("community_growth_attributed", 0)
            * BONUS_RATES["community_growth_attributed"],
        }
        total = base_reward + sum(bonuses.values())
        capped = total > 500
        total = min(total, 500)
        rank = max(1, 100 - int(total))
        data = {
            "base_reward": base_reward,
            "bonuses": bonuses,
            "total_reward": round(total, 2),
            "capped": capped,
            "rank_among_ambassadors": rank,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("ambassador_reward_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
