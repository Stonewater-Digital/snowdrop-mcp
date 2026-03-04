"""Create weighted borrower credit score."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "borrower_credit_scorecard",
    "description": "Generates weighted scorecard covering leverage, coverage, liquidity, and management.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "net_leverage": {"type": "number"},
            "interest_coverage": {"type": "number"},
            "liquidity_ratio": {"type": "number"},
            "management_score": {"type": "number"},
            "industry_outlook_score": {"type": "number", "default": 0.5},
        },
        "required": ["net_leverage", "interest_coverage", "liquidity_ratio", "management_score"],
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


def borrower_credit_scorecard(
    net_leverage: float,
    interest_coverage: float,
    liquidity_ratio: float,
    management_score: float,
    industry_outlook_score: float = 0.5,
    **_: Any,
) -> dict[str, Any]:
    """Return normalized borrower scores."""
    try:
        leverage_score = max(0.0, 1 - net_leverage / 6)
        coverage_score = min(interest_coverage / 4, 1)
        liquidity_score = min(liquidity_ratio / 1.5, 1)
        weights = {
            "leverage": 0.3,
            "coverage": 0.25,
            "liquidity": 0.2,
            "management": 0.15,
            "industry": 0.1,
        }
        composite = (
            leverage_score * weights["leverage"]
            + coverage_score * weights["coverage"]
            + liquidity_score * weights["liquidity"]
            + management_score * weights["management"]
            + industry_outlook_score * weights["industry"]
        )
        risk_label = "strong" if composite >= 0.7 else "watch" if composite >= 0.5 else "weak"
        data = {
            "leverage_score": round(leverage_score, 3),
            "coverage_score": round(coverage_score, 3),
            "liquidity_score": round(liquidity_score, 3),
            "management_score": round(management_score, 3),
            "industry_outlook_score": round(industry_outlook_score, 3),
            "composite_score": round(composite, 3),
            "risk_label": risk_label,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("borrower_credit_scorecard", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
