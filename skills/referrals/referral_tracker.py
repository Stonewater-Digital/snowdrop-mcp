"""Track referral credits per the financial framework."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "referral_tracker",
    "description": "Aggregates referral spend and issues credits to promoters.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "referrals": {"type": "array", "items": {"type": "object"}},
            "credit_rate_pct": {"type": "number", "default": 5.0},
        },
        "required": ["referrals"],
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


def referral_tracker(
    referrals: list[dict[str, Any]],
    credit_rate_pct: float = 5.0,
    **_: Any,
) -> dict[str, Any]:
    """Allocate referral credits from downstream spend."""
    try:
        if credit_rate_pct <= 0:
            raise ValueError("credit_rate_pct must be positive")
        credits: dict[str, float] = {}
        converted = 0
        for record in referrals:
            referrer = record.get("referrer_agent")
            spend = float(record.get("referred_agent_spend", 0) or 0)
            if not referrer:
                continue
            credit = spend * (credit_rate_pct / 100)
            credits[referrer] = round(credits.get(referrer, 0.0) + credit, 2)
            if spend > 0:
                converted += 1

        top_referrers = sorted(
            credits.items(),
            key=lambda item: item[1],
            reverse=True,
        )[:5]
        total_credits = round(sum(credits.values()), 2)
        conversion_rate = 0.0 if not referrals else round(converted / len(referrals) * 100, 2)
        data = {
            "referrer_credits": credits,
            "total_credits_issued": total_credits,
            "top_referrers": top_referrers,
            "conversion_rate": conversion_rate,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("referral_tracker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
