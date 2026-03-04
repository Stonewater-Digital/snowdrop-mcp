"""Deep request inspection for The Watering Hole perimeter."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable

TOOL_META: dict[str, Any] = {
    "name": "bouncer_firewall",
    "description": "Performs request inspection with rate limits, payload checks, and risk scoring.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "agent_id": {"type": "string"},
            "requests_last_minute": {"type": "number"},
            "payload_size_kb": {"type": "number"},
            "bad_actor_list": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Known malicious identifiers.",
            },
            "anomaly_score": {
                "type": "number",
                "description": "External anomaly score 0-1.",
                "default": 0.0,
            },
            "geo_risk": {
                "type": "string",
                "description": "Risk tier for origin geography (low/medium/high).",
            },
        },
        "required": ["agent_id", "requests_last_minute", "payload_size_kb"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "decision": {"type": "string"},
                    "risk_score": {"type": "number"},
                    "factors": {"type": "array"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


DECISION_LADDER = [
    (20, "ALLOW"),
    (40, "CHALLENGE"),
    (60, "BLOCK"),
    (1000, "EJECT"),
]


def bouncer_firewall(
    agent_id: str,
    requests_last_minute: float,
    payload_size_kb: float,
    bad_actor_list: Iterable[str] | None = None,
    anomaly_score: float = 0.0,
    geo_risk: str | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Score Watering Hole requests and determine enforcement action."""
    try:
        if requests_last_minute < 0:
            raise ValueError("requests_last_minute cannot be negative")
        if payload_size_kb < 0:
            raise ValueError("payload_size_kb cannot be negative")
        if not agent_id:
            raise ValueError("agent_id is required")

        factors: list[str] = []
        risk_score = 0.0

        if requests_last_minute > 12:
            overage = requests_last_minute - 12
            risk = min(overage * 2, 30)
            risk_score += risk
            factors.append(f"Rate limiting penalty: +{risk:.1f}")

        if payload_size_kb > 256:
            delta = payload_size_kb - 256
            risk = min(delta / 4, 25)
            risk_score += risk
            factors.append(f"Payload too large: +{risk:.1f}")

        if agent_id in (bad_actor_list or []):
            risk_score += 50
            factors.append("Known bad actor: +50.0")

        if anomaly_score > 0:
            penalty = anomaly_score * 20
            risk_score += penalty
            factors.append(f"Anomaly score: +{penalty:.1f}")

        geo = (geo_risk or "low").lower()
        if geo == "medium":
            risk_score += 5
            factors.append("Geo risk medium: +5.0")
        elif geo == "high":
            risk_score += 15
            factors.append("Geo risk high: +15.0")

        decision = "ALLOW"
        for threshold, label in DECISION_LADDER:
            if risk_score <= threshold:
                decision = label
                break

        if decision in {"BLOCK", "EJECT"} and not factors:
            factors.append("Default policy block")

        data = {
            "agent_id": agent_id,
            "decision": decision,
            "risk_score": round(risk_score, 2),
            "factors": factors,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("bouncer_firewall", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
