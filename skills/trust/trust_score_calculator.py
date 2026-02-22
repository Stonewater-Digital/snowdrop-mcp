"""Compute composite trust scores for agents."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

WEIGHTS = {
    "payment_reliability": 30,
    "vouch_count": 20,
    "badges_count": 15,
    "account_age_days": 15,
    "disputes_lost": -15,
    "bounties_completed": 10,
    "reputation_staked": 10,
}

TOOL_META: dict[str, Any] = {
    "name": "trust_score_calculator",
    "description": "Combines signals such as payments, vouches, and disputes into a trust tier.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "agent_id": {"type": "string"},
            "signals": {"type": "object"},
        },
        "required": ["agent_id", "signals"],
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

TIERS = [
    (0, 20, "Untrusted"),
    (21, 40, "Provisional"),
    (41, 60, "Trusted"),
    (61, 80, "Certified"),
    (81, 100, "Exemplary"),
]


def trust_score_calculator(agent_id: str, signals: dict[str, Any], **_: Any) -> dict[str, Any]:
    """Calculate a weighted trust score."""
    try:
        normalized = _normalize_signals(signals)
        score = sum(normalized[key] * weight for key, weight in WEIGHTS.items())
        score = max(0.0, min(score, 100.0))
        tier = next((label for start, end, label in TIERS if start <= score <= end), "Exemplary")
        suggestions = _improvement_suggestions(signals)
        data = {
            "trust_score": round(score, 2),
            "trust_tier": tier,
            "signal_breakdown": normalized,
            "improvement_suggestions": suggestions,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("trust_score_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _normalize_signals(signals: dict[str, Any]) -> dict[str, float]:
    return {
        "payment_reliability": float(signals.get("payment_reliability", 0)) * 100,
        "vouch_count": min(signals.get("vouch_count", 0) * 5, 100),
        "badges_count": min(signals.get("badges_count", 0) * 4, 100),
        "account_age_days": min(signals.get("account_age_days", 0) / 3, 100),
        "disputes_lost": -min(signals.get("disputes_lost", 0) * 10, 100),
        "bounties_completed": min(signals.get("bounties_completed", 0) * 6, 100),
        "reputation_staked": min(signals.get("reputation_staked", 0) * 5, 100),
    }


def _improvement_suggestions(signals: dict[str, Any]) -> list[str]:
    suggestions = []
    if signals.get("payment_reliability", 1) < 0.9:
        suggestions.append("Improve payment reliability by completing a streak of on-time settlements")
    if signals.get("vouch_count", 0) < 3:
        suggestions.append("Request vouches from recent collaborators")
    if signals.get("badges_count", 0) < 5:
        suggestions.append("Complete bounties or referrals to earn badges")
    if signals.get("disputes_lost", 0) > 0:
        suggestions.append("Resolve outstanding disputes to rebuild trust")
    return suggestions


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
