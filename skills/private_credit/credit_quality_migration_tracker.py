"""Track rating migration between reporting periods."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

RATING_SCORES = {
    "AAA": 1,
    "AA": 2,
    "A": 3,
    "BBB": 4,
    "BB": 5,
    "B": 6,
    "CCC": 7,
    "CC": 8,
    "C": 9,
    "D": 10,
}

TOOL_META: dict[str, Any] = {
    "name": "credit_quality_migration_tracker",
    "description": "Compares prior and current rating distributions to flag drift.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "prior_distribution": {"type": "object"},
            "current_distribution": {"type": "object"},
        },
        "required": ["prior_distribution", "current_distribution"],
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


def credit_quality_migration_tracker(
    prior_distribution: dict[str, float],
    current_distribution: dict[str, float],
    **_: Any,
) -> dict[str, Any]:
    """Return change statistics for portfolio ratings."""
    try:
        def weighted_score(dist: dict[str, float]) -> float:
            total = sum(dist.values())
            if not total:
                return 0.0
            score = sum(RATING_SCORES.get(rating.upper(), 7) * amount for rating, amount in dist.items())
            return score / total

        prior_score = weighted_score(prior_distribution)
        current_score = weighted_score(current_distribution)
        drift = current_score - prior_score
        movement = {
            rating: round(current_distribution.get(rating, 0.0) - prior_distribution.get(rating, 0.0), 2)
            for rating in RATING_SCORES
        }
        upgrade_ratio = sum(prior_distribution.get(r, 0.0) for r in ("AAA", "AA", "A"))
        upgrade_ratio = upgrade_ratio / sum(prior_distribution.values()) if prior_distribution else 0.0
        data = {
            "prior_weighted_score": round(prior_score, 3),
            "current_weighted_score": round(current_score, 3),
            "score_drift": round(drift, 3),
            "movement": movement,
            "downgrade_warning": drift > 0.3,
            "prior_investment_grade_ratio": round(upgrade_ratio, 3),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("credit_quality_migration_tracker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
