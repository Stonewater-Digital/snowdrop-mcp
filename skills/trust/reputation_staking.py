"""Allow agents to stake reputation on community claims."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "reputation_staking",
    "description": "Locks reputation points against delivery, quality, or fairness claims.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "agent_id": {"type": "string"},
            "claim": {"type": "string"},
            "stake_amount": {"type": "integer"},
            "claim_type": {
                "type": "string",
                "enum": ["skill_quality", "delivery_promise", "price_fairness"],
            },
            "current_reputation": {"type": "integer"},
        },
        "required": ["agent_id", "claim", "stake_amount", "claim_type", "current_reputation"],
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


def reputation_staking(
    agent_id: str,
    claim: str,
    stake_amount: int,
    claim_type: str,
    current_reputation: int,
    **_: Any,
) -> dict[str, Any]:
    """Reserve reputation points for a claim."""
    try:
        if stake_amount <= 0:
            raise ValueError("stake_amount must be positive")
        if stake_amount > current_reputation:
            raise ValueError("Insufficient reputation to stake")
        remaining = current_reputation - stake_amount
        potential_gain = stake_amount * 2
        data = {
            "staked": True,
            "stake_amount": stake_amount,
            "remaining_reputation": remaining,
            "potential_gain": potential_gain,
            "potential_loss": stake_amount,
            "resolution": "pending",
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("reputation_staking", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
