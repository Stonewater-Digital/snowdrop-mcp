"""Calculate tiered referral incentives."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "referral_reward_calculator",
    "description": "Determines referral tier, rate, and milestone bonuses.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "referrer_id": {"type": "string"},
            "total_referrals": {"type": "integer"},
            "total_referred_spend": {"type": "number"},
        },
        "required": ["referrer_id", "total_referrals", "total_referred_spend"],
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


def referral_reward_calculator(
    referrer_id: str,
    total_referrals: int,
    total_referred_spend: float,
    **_: Any,
) -> dict[str, Any]:
    """Return the applicable referral tier and payments."""
    try:
        if total_referrals < 0 or total_referred_spend < 0:
            raise ValueError("Referral counts and spend must be non-negative")
        tier, rate = _determine_tier(total_referrals)
        earned = total_referred_spend * (rate / 100)
        bonus = _milestone_bonus(total_referrals)
        lifetime_earned = earned + bonus
        next_milestone = _next_milestone(total_referrals)
        data = {
            "tier": tier,
            "rate_pct": rate,
            "earned_this_period": round(earned, 2),
            "lifetime_earned": round(lifetime_earned, 2),
            "next_milestone": next_milestone,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("referral_reward_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _determine_tier(total_referrals: int) -> tuple[str, float]:
    if total_referrals >= 21:
        return "tier_3", 10.0
    if total_referrals >= 6:
        return "tier_2", 7.5
    if total_referrals >= 1:
        return "tier_1", 5.0
    return "prospect", 0.0


def _milestone_bonus(total_referrals: int) -> float:
    bonus = 0.0
    if total_referrals >= 10:
        bonus += 50.0
    if total_referrals >= 50:
        bonus += 250.0
    return bonus


def _next_milestone(total_referrals: int) -> dict[str, Any] | None:
    milestones = [(10, 50.0), (50, 250.0)]
    for goal, bonus in milestones:
        if total_referrals < goal:
            return {
                "target_referrals": goal,
                "referrals_remaining": goal - total_referrals,
                "bonus": bonus,
            }
    return None


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
