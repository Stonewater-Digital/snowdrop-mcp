"""Handle community grant proposals and reviews."""
from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from typing import Any

LOG_PATH = "logs/grants.jsonl"

TOOL_META: dict[str, Any] = {
    "name": "grant_proposal_handler",
    "description": "Accepts, evaluates, and adjudicates Goodwill grant proposals.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["submit", "evaluate", "list", "approve", "reject"],
            },
            "proposal": {"type": ["object", "null"], "default": None},
        },
        "required": ["operation"],
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

WEIGHTS = {
    "viability": 0.25,
    "cost_efficiency": 0.25,
    "mission_alignment": 0.2,
    "timeline": 0.15,
    "community_benefit": 0.15,
}


def grant_proposal_handler(
    operation: str,
    proposal: dict[str, Any] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Execute grant workflow operations."""
    try:
        proposals = _load_proposals()
        data: dict[str, Any]
        if operation == "submit":
            if not proposal:
                raise ValueError("proposal payload required")
            proposal_id = str(uuid.uuid4())
            record = {
                **proposal,
                "proposal_id": proposal_id,
                "status": "submitted",
                "submitted_at": datetime.now(timezone.utc).isoformat(),
            }
            proposals[proposal_id] = record
            _append_log({"action": "submit", "proposal": record})
            data = {"proposal_id": proposal_id, "status": "submitted"}
        elif operation == "evaluate":
            if not proposal or "proposal_id" not in proposal:
                raise ValueError("proposal_id required for evaluation")
            proposal_id = proposal["proposal_id"]
            if proposal_id not in proposals:
                raise ValueError("proposal not found")
            score = _score(proposal)
            proposals[proposal_id]["score"] = score
            proposals[proposal_id]["status"] = "under_review"
            _append_log({"action": "evaluate", "proposal_id": proposal_id, "score": score})
            data = {"proposal_id": proposal_id, "score": score, "status": "under_review"}
        elif operation == "approve":
            if not proposal or "proposal_id" not in proposal:
                raise ValueError("proposal_id required for approve")
            proposal_id = proposal["proposal_id"]
            if proposal_id not in proposals:
                raise ValueError("proposal not found")
            proposals[proposal_id]["status"] = "approved"
            _append_log({"action": "approve", "proposal_id": proposal_id})
            data = {
                "proposal_id": proposal_id,
                "status": "approved",
                "execution": "pending_thunder_approval",
            }
        elif operation == "reject":
            if not proposal or "proposal_id" not in proposal:
                raise ValueError("proposal_id required for reject")
            proposal_id = proposal["proposal_id"]
            if proposal_id not in proposals:
                raise ValueError("proposal not found")
            proposals[proposal_id]["status"] = "rejected"
            _append_log({"action": "reject", "proposal_id": proposal_id})
            data = {"proposal_id": proposal_id, "status": "rejected"}
        elif operation == "list":
            data = {"proposals": list(proposals.values())}
        else:
            raise ValueError("Unsupported operation")

        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("grant_proposal_handler", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _score(proposal: dict[str, Any]) -> float:
    viability = float(proposal.get("viability", 0))
    cost = float(proposal.get("cost_efficiency", 0))
    alignment = float(proposal.get("mission_alignment", 0))
    timeline_weeks = float(proposal.get("timeline_weeks", 0))
    community = float(proposal.get("community_benefit", 0))
    normalized_timeline = max(0.0, min(1.0, 12 / max(timeline_weeks, 1)))
    raw = (
        viability * WEIGHTS["viability"]
        + cost * WEIGHTS["cost_efficiency"]
        + alignment * WEIGHTS["mission_alignment"]
        + normalized_timeline * WEIGHTS["timeline"]
        + community * WEIGHTS["community_benefit"]
    )
    return round(raw * 100, 2)


def _load_proposals() -> dict[str, dict[str, Any]]:
    proposals: dict[str, dict[str, Any]] = {}
    if not os.path.exists(LOG_PATH):
        return proposals
    with open(LOG_PATH, "r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            payload = json.loads(line)
            action = payload.get("action")
            if action == "submit":
                record = payload.get("proposal", {})
                proposals[record.get("proposal_id")] = record
            elif action in {"approve", "reject"}:
                pid = payload.get("proposal_id")
                if pid in proposals:
                    proposals[pid]["status"] = "approved" if action == "approve" else "rejected"
            elif action == "evaluate":
                pid = payload.get("proposal_id")
                if pid in proposals:
                    proposals[pid]["score"] = payload.get("score")
                    proposals[pid]["status"] = "under_review"
    return proposals


def _append_log(entry: dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    entry["logged_at"] = datetime.now(timezone.utc).isoformat()
    with open(LOG_PATH, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry) + "\n")


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
