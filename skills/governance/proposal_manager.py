"""Democracy Protocol proposal lifecycle manager."""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "proposal_manager",
    "description": "Submits, lists, fetches, or closes proposals per Snowdrop governance rules.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "operation": {"type": "string", "enum": ["submit", "list", "get", "close"]},
            "proposal": {"type": ["object", "null"]},
            "proposal_id": {"type": ["string", "null"]},
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

_PROPOSAL_FILE = "logs/proposals.jsonl"


def proposal_manager(
    operation: str,
    proposal: dict[str, Any] | None = None,
    proposal_id: str | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Perform governance operations on proposals."""
    try:
        proposals = _load_proposals()
        if operation == "submit":
            if not proposal:
                raise ValueError("proposal payload required")
            new_id = f"PROP-{len(proposals) + 1:04d}"
            proposal_record = {
                "proposal_id": new_id,
                "title": proposal.get("title"),
                "description": proposal.get("description"),
                "proposer_id": proposal.get("proposer_id"),
                "category": proposal.get("category"),
                "status": "open",
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
            _append_proposal(proposal_record)
            result = proposal_record
        elif operation == "list":
            result = {"proposals": proposals}
        elif operation == "get":
            result = next((p for p in proposals if p["proposal_id"] == proposal_id), None)
            if not result:
                raise ValueError("proposal not found")
        elif operation == "close":
            if not proposal_id:
                raise ValueError("proposal_id required to close")
            status = proposal.get("status") if proposal else "implemented"
            updated = False
            for row in proposals:
                if row["proposal_id"] == proposal_id:
                    row["status"] = status
                    row["closed_at"] = datetime.now(timezone.utc).isoformat()
                    updated = True
                    break
            if not updated:
                raise ValueError("proposal not found")
            _write_all(proposals)
            result = {"proposal_id": proposal_id, "status": status}
        else:
            raise ValueError("Unsupported operation")
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("proposal_manager", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _load_proposals() -> list[dict[str, Any]]:
    if not os.path.exists(_PROPOSAL_FILE):
        return []
    proposals = []
    with open(_PROPOSAL_FILE, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                proposals.append(json.loads(line))
    return proposals


def _append_proposal(record: dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(_PROPOSAL_FILE), exist_ok=True)
    with open(_PROPOSAL_FILE, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(record) + "\n")


def _write_all(records: list[dict[str, Any]]) -> None:
    with open(_PROPOSAL_FILE, "w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record) + "\n")


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
