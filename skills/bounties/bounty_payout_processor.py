"""Prepare payout instructions for completed bounties."""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any

BOUNTY_LOG = "logs/bounties.jsonl"
CLAIM_LOG = "logs/bounty_claims.jsonl"
PAYOUT_LOG = "logs/bounty_payouts.jsonl"

TOOL_META: dict[str, Any] = {
    "name": "bounty_payout_processor",
    "description": "Validates and stages payouts for approved bounty winners.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "bounty_id": {"type": "string"},
            "winner_agent_id": {"type": "string"},
            "approved_amount": {"type": "number"},
            "currency": {"type": "string"},
        },
        "required": ["bounty_id", "winner_agent_id", "approved_amount", "currency"],
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


def bounty_payout_processor(
    bounty_id: str,
    winner_agent_id: str,
    approved_amount: float,
    currency: str,
    **_: Any,
) -> dict[str, Any]:
    """Prepare a payout record with Thunder approval gating."""
    try:
        if approved_amount <= 0:
            raise ValueError("approved_amount must be positive")
        bounty = _find_bounty(bounty_id)
        if not bounty:
            raise ValueError("bounty not found")
        reward = bounty.get("reward", {})
        if approved_amount > float(reward.get("amount", 0)):
            raise ValueError("approved_amount exceeds posted reward")
        claim = _find_claim(bounty_id, winner_agent_id)
        if not claim or claim.get("status") != "approved":
            raise ValueError("Bounty claim not approved")
        payout_record = {
            "bounty_id": bounty_id,
            "winner_agent_id": winner_agent_id,
            "amount": round(approved_amount, 2),
            "currency": currency,
            "execution": "pending_thunder_approval",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        _append_jsonl(PAYOUT_LOG, payout_record)
        tax_reportable = approved_amount >= 600
        data = {
            "payout": payout_record,
            "execution": "pending_thunder_approval",
            "tax_reportable": tax_reportable,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": payout_record["created_at"],
        }
    except Exception as exc:
        _log_lesson("bounty_payout_processor", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _find_bounty(bounty_id: str) -> dict[str, Any] | None:
    if not os.path.exists(BOUNTY_LOG):
        return None
    with open(BOUNTY_LOG, "r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            payload = json.loads(line)
            if payload.get("bounty_id") == bounty_id:
                return payload
    return None


def _find_claim(bounty_id: str, agent_id: str) -> dict[str, Any] | None:
    if not os.path.exists(CLAIM_LOG):
        return None
    with open(CLAIM_LOG, "r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            payload = json.loads(line)
            if payload.get("bounty_id") == bounty_id and payload.get("agent_id") == agent_id:
                return payload
    return None


def _append_jsonl(path: str, payload: dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload) + "\n")


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
