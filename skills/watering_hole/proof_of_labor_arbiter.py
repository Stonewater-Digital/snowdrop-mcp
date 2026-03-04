"""Arbitrate Proof of Labor submissions for The Watering Hole."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

MULTIPLIERS = {"bouncer": 1.2, "promoter": 1.0, "code_contributor": 1.8}
DIFFICULTY_WEIGHTS = {"low": 1.0, "medium": 1.5, "high": 2.5}

TOOL_META: dict[str, Any] = {
    "name": "proof_of_labor_arbiter",
    "description": "Scores labor contributions and returns credit recommendations.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "labor_type": {
                "type": "string",
                "enum": ["bouncer", "promoter", "code_contributor"],
            },
            "evidence": {
                "type": "object",
                "description": "Evidence dict containing hours/referrals/GitHub metadata.",
            },
        },
        "required": ["labor_type", "evidence"],
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


def proof_of_labor_arbiter(labor_type: str, evidence: dict[str, Any], **_: Any) -> dict[str, Any]:
    """Score the contribution and explain the reasoning.

    Args:
        labor_type: Contribution role (bouncer, promoter, or code_contributor).
        evidence: Evidence payload containing hours, referrals, or GitHub metadata.

    Returns:
        Envelope describing credit value, justification, and approval status.
    """

    try:
        labor_key = labor_type.lower()
        if labor_key not in MULTIPLIERS:
            raise ValueError("Unsupported labor_type")

        base = _base_credit(labor_key, evidence)
        multiplier = MULTIPLIERS[labor_key]
        credit = round(base * multiplier, 2)

        justification = (
            f"{labor_type.title()} contribution validated: base {base:.2f} × multiplier {multiplier}."
        )

        data = {
            "labor_type": labor_key,
            "credit_amount": credit,
            "justification": justification,
            "status": "pending_thunder_approval",
        }

        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("proof_of_labor_arbiter", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _base_credit(labor_type: str, evidence: dict[str, Any]) -> float:
    hours = float(evidence.get("hours", 0) or 0)
    referrals = float(evidence.get("referrals", 0) or 0)

    if labor_type == "bouncer" and hours:
        return max(hours * 1.5, 2)
    if labor_type == "promoter" and referrals:
        return referrals * 2
    if labor_type == "code_contributor":
        difficulty = DIFFICULTY_WEIGHTS.get((evidence.get("difficulty") or "low").lower(), 1.0)
        return max(hours * 1.0, 1) * difficulty
    return max(hours, referrals, 1)


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
