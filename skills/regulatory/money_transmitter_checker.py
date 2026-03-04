"""Heuristic Money Transmitter License evaluator."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "money_transmitter_checker",
    "description": "Flags actions that might require MTL coverage and provides guidance.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "action_type": {
                "type": "string",
                "enum": ["transfer", "exchange", "custody"],
            },
            "amount": {"type": "number"},
            "sender_type": {
                "type": "string",
                "enum": ["self", "agent", "third_party"],
            },
            "receiver_type": {
                "type": "string",
                "enum": ["self", "agent", "third_party"],
            },
            "jurisdiction": {"type": "string"},
        },
        "required": [
            "action_type",
            "amount",
            "sender_type",
            "receiver_type",
            "jurisdiction",
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

THRESHOLDS = {
    "federal": 1000,
    "NY": 0,
    "CA": 1000,
}


def money_transmitter_checker(
    action_type: str,
    amount: float,
    sender_type: str,
    receiver_type: str,
    jurisdiction: str,
    **_: Any,
) -> dict[str, Any]:
    """Return MTL trigger assessment."""

    try:
        if amount <= 0:
            raise ValueError("amount must be positive")
        threshold = THRESHOLDS.get(jurisdiction.upper(), THRESHOLDS["federal"])
        third_party_flow = sender_type != receiver_type or sender_type == "third_party"
        triggers = amount >= threshold and third_party_flow
        risk = "low"
        if triggers and amount > threshold * 5:
            risk = "high"
        elif triggers:
            risk = "medium"
        exemptions = []
        if not third_party_flow:
            exemptions.append("Self-directed transfer")
        if action_type == "custody" and amount < 100:
            exemptions.append("Custodial balance < $100")
        recommendation = (
            "Consult MTL counsel and hold until Thunder clears"
            if triggers
            else "No immediate MTL filing, monitor"
        )
        data = {
            "triggers_mtl": triggers,
            "exemptions_applicable": exemptions,
            "risk_level": risk,
            "recommendation": recommendation,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("money_transmitter_checker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
