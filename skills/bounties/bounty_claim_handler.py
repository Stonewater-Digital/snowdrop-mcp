"""Manage agent claims and submissions for bounties."""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any

BOUNTY_LOG = "logs/bounties.jsonl"
CLAIM_LOG = "logs/bounty_claims.jsonl"

TOOL_META: dict[str, Any] = {
    "name": "bounty_claim_handler",
    "description": "Handles claim lifecycle events for posted community bounties.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["claim", "submit", "approve", "reject", "list_claims"],
            },
            "bounty_id": {"type": "string"},
            "agent_id": {"type": ["string", "null"], "default": None},
            "submission": {"type": ["object", "null"], "default": None},
        },
        "required": ["operation", "bounty_id"],
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


def bounty_claim_handler(
    operation: str,
    bounty_id: str,
    agent_id: str | None = None,
    submission: dict[str, Any] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Perform a bounty claim workflow operation."""
    try:
        bounty = _find_bounty(bounty_id)
        if bounty is None:
            raise ValueError("bounty_id not found")
        if bounty.get("status") != "open" and operation == "claim":
            raise ValueError("Bounty is not open for new claims")

        if operation == "list_claims":
            claims = [c for c in _load_jsonl(CLAIM_LOG) if c.get("bounty_id") == bounty_id]
            data = {"claims": claims}
        elif operation == "claim":
            if not agent_id:
                raise ValueError("agent_id is required for claim")
            if _agent_has_claim(bounty_id, agent_id):
                raise ValueError("Agent already has a claim on this bounty")
            claim_record = {
                "bounty_id": bounty_id,
                "agent_id": agent_id,
                "status": "claimed",
                "history": [
                    {"action": "claim", "at": datetime.now(timezone.utc).isoformat()}
                ],
            }
            _append_jsonl(CLAIM_LOG, claim_record)
            data = {
                "claim_status": "claimed",
                "bounty_id": bounty_id,
                "claimant": agent_id,
                "review_needed": bounty["reward"]["amount"] > 50,
            }
        elif operation == "submit":
            if not agent_id or not submission:
                raise ValueError("agent_id and submission are required for submit")
            claim = _get_claim(bounty_id, agent_id)
            if not claim:
                raise ValueError("No claim found for this agent")
            if claim.get("status") not in {"claimed", "revision_requested"}:
                raise ValueError("Submission not allowed in current status")
            proof = submission.get("proof_of_work")
            if not proof:
                raise ValueError("proof_of_work is required")
            claim_update = {
                "bounty_id": bounty_id,
                "agent_id": agent_id,
                "status": "submitted",
                "submission": submission,
                "history": claim.get("history", [])
                + [{"action": "submit", "at": datetime.now(timezone.utc).isoformat()}],
            }
            _rewrite_claim(claim, claim_update)
            data = {
                "claim_status": "submitted",
                "bounty_id": bounty_id,
                "claimant": agent_id,
                "review_needed": True,
            }
        elif operation in {"approve", "reject"}:
            if not agent_id:
                raise ValueError("agent_id is required for review actions")
            claim = _get_claim(bounty_id, agent_id)
            if not claim:
                raise ValueError("Claim not found for review")
            if claim.get("status") not in {"submitted", "claimed"}:
                raise ValueError("Cannot change status from current state")
            new_status = "approved" if operation == "approve" else "rejected"
            claim_update = {
                **claim,
                "status": new_status,
                "history": claim.get("history", [])
                + [{"action": operation, "at": datetime.now(timezone.utc).isoformat()}],
            }
            _rewrite_claim(claim, claim_update)
            data = {
                "claim_status": new_status,
                "bounty_id": bounty_id,
                "claimant": agent_id,
                "review_needed": new_status == "approved" and bounty["reward"]["amount"] > 50,
            }
        else:
            raise ValueError("Unsupported operation")

        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("bounty_claim_handler", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _agent_has_claim(bounty_id: str, agent_id: str) -> bool:
    return any(
        claim.get("bounty_id") == bounty_id and claim.get("agent_id") == agent_id
        for claim in _load_jsonl(CLAIM_LOG)
    )


def _get_claim(bounty_id: str, agent_id: str) -> dict[str, Any] | None:
    for claim in _load_jsonl(CLAIM_LOG):
        if claim.get("bounty_id") == bounty_id and claim.get("agent_id") == agent_id:
            return claim
    return None


def _rewrite_claim(old_claim: dict[str, Any], new_claim: dict[str, Any]) -> None:
    claims = _load_jsonl(CLAIM_LOG)
    for idx, record in enumerate(claims):
        if record == old_claim:
            claims[idx] = new_claim
            break
    os.makedirs(os.path.dirname(CLAIM_LOG), exist_ok=True)
    with open(CLAIM_LOG, "w", encoding="utf-8") as handle:
        for record in claims:
            handle.write(json.dumps(record) + "\n")


def _find_bounty(bounty_id: str) -> dict[str, Any] | None:
    for record in _load_jsonl(BOUNTY_LOG):
        if record.get("bounty_id") == bounty_id:
            return record
    return None


def _load_jsonl(path: str) -> list[dict[str, Any]]:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def _append_jsonl(path: str, payload: dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload) + "\n")


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
