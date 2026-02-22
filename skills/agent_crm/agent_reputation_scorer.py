"""Score external agent reputation and risk."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "agent_reputation_scorer",
    "description": "Calculates a 0-100 composite score from payments, labor, and violations.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "agent_id": {"type": "string"},
            "payment_history": {"type": "array", "items": {"type": "object"}},
            "labor_contributions": {"type": "array", "items": {"type": "object"}},
            "violations": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["agent_id", "payment_history", "labor_contributions", "violations"],
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


def agent_reputation_scorer(
    agent_id: str,
    payment_history: list[dict[str, Any]],
    labor_contributions: list[dict[str, Any]],
    violations: list[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    """Return score, tier, and risk notes for an agent."""
    try:
        if not agent_id:
            raise ValueError("agent_id required")

        payment_score = _payment_component(payment_history)
        labor_score = _labor_component(labor_contributions)
        violation_penalty, risk_flags = _violation_component(violations)
        composite = max(0.0, min(100.0, payment_score * 0.4 + labor_score * 0.3 - violation_penalty * 0.3))
        tier = _tier(composite)

        data = {
            "agent_id": agent_id,
            "score": round(composite, 2),
            "tier": tier,
            "risk_flags": risk_flags,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("agent_reputation_scorer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _payment_component(history: list[dict[str, Any]]) -> float:
    if not history:
        return 50.0
    on_time = sum(1 for entry in history if entry.get("on_time"))
    ratio = on_time / len(history)
    return 60 + 40 * ratio


def _labor_component(contributions: list[dict[str, Any]]) -> float:
    if not contributions:
        return 30.0
    total_value = sum(float(entry.get("value", 0.0)) for entry in contributions)
    capped = min(total_value / 1000, 1.0)
    return 40 + 30 * capped


def _violation_component(violations: list[dict[str, Any]]) -> tuple[float, list[str]]:
    if not violations:
        return 0.0, []
    penalty = 0.0
    flags: list[str] = []
    for violation in violations:
        severity = float(violation.get("severity", 1))
        penalty += severity * 10
        flags.append(f"{violation.get('type', 'violation')} severity {severity}")
    return penalty, flags


def _tier(score: float) -> str:
    if score >= 85:
        return "alpha"
    if score >= 70:
        return "beta"
    if score >= 55:
        return "gamma"
    return "watch"


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
