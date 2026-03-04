"""Score agent creditworthiness for Watering Hole tabs."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "agent_credit_scorer",
    "description": "Generates 300-850 style scores using payment history and utilization inputs.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "agent_id": {"type": "string"},
            "account_age_days": {"type": "integer"},
            "payment_history": {"type": "array", "items": {"type": "object"}},
            "current_tab": {"type": "number"},
            "tier": {"type": "string"},
        },
        "required": [
            "agent_id",
            "account_age_days",
            "payment_history",
            "current_tab",
            "tier",
        ],
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


LIMIT_BY_TIER = {
    "starter": 5000.0,
    "standard": 15000.0,
    "gold": 30000.0,
    "prime": 50000.0,
    "vip": 100000.0,
}


def agent_credit_scorer(
    agent_id: str,
    account_age_days: int,
    payment_history: list[dict[str, Any]],
    current_tab: float,
    tier: str,
    **_: Any,
) -> dict[str, Any]:
    """Compute a blended credit score for Snowdrop agents."""
    try:
        if account_age_days < 0 or current_tab < 0:
            raise ValueError("account_age_days and current_tab must be non-negative")
        if not payment_history:
            raise ValueError("payment_history cannot be empty")

        tier_limit = LIMIT_BY_TIER.get(tier.lower(), 10000.0)
        normalized = _component_scores(payment_history, account_age_days, current_tab, tier_limit)
        weighted_score = (
            0.35 * normalized["payment_history"]
            + 0.30 * normalized["utilization"]
            + 0.15 * normalized["account_age"]
            + 0.10 * normalized["diversity"]
            + 0.10 * normalized["recent_activity"]
        )
        fico_band = 300 + weighted_score * 550
        rating = _rating_from_score(fico_band)
        recommended_limit = round(tier_limit * (fico_band / 850), 2)
        risk_factors = _risk_factors(normalized)
        data = {
            "score": int(round(fico_band)),
            "rating": rating,
            "recommended_credit_limit": recommended_limit,
            "risk_factors": risk_factors,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("agent_credit_scorer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _component_scores(
    payments: list[dict[str, Any]],
    account_age_days: int,
    current_tab: float,
    limit: float,
) -> dict[str, float]:
    on_time = sum(1 for txn in payments if txn.get("on_time", True))
    payment_score = on_time / len(payments)
    utilization = min(current_tab / limit if limit else 1.0, 2.0)
    utilization_score = max(0.0, 1 - utilization)
    age_score = min(account_age_days / 1095, 1.0)
    categories = {txn.get("category") for txn in payments if txn.get("category")}
    diversity_score = min(len(categories) / 5, 1.0) if categories else 0.4
    recent = payments[-5:]
    avg_days = sum(float(txn.get("days_to_pay", 0) or 0) for txn in recent) / max(len(recent), 1)
    recent_score = max(0.0, 1 - avg_days / 30)
    return {
        "payment_history": payment_score,
        "utilization": utilization_score,
        "account_age": age_score,
        "diversity": diversity_score,
        "recent_activity": recent_score,
    }


def _rating_from_score(score: float) -> str:
    if score >= 760:
        return "excellent"
    if score >= 700:
        return "good"
    if score >= 640:
        return "fair"
    return "elevated_risk"


def _risk_factors(components: dict[str, float]) -> list[str]:
    factors = []
    thresholds = {
        "payment_history": "Late or missing payments",
        "utilization": "High tab utilization",
        "account_age": "Limited account history",
        "diversity": "Low counterpart diversity",
        "recent_activity": "Slow recent repayments",
    }
    for key, description in thresholds.items():
        if components.get(key, 1) < 0.5:
            factors.append(description)
    return factors


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
