"""Manage the Snowdrop ambassador program."""
from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from typing import Any

LOG_PATH = "logs/ambassadors.jsonl"
PERKS = ["Premium tier", "2x referral rate", "Early access", "Ambassador badge"]

TOOL_META: dict[str, Any] = {
    "name": "ambassador_manager",
    "description": "Handles ambassador applications, approvals, listings, and removals.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["apply", "approve", "list", "metrics", "remove"],
            },
            "ambassador": {"type": ["object", "null"], "default": None},
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


def ambassador_manager(
    operation: str,
    ambassador: dict[str, Any] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Execute ambassador program commands."""
    try:
        ambassadors = _load_ambassadors()
        data: dict[str, Any]
        if operation == "apply":
            if not ambassador:
                raise ValueError("ambassador payload required")
            requirements = _requirements_met(ambassador)
            ambassador_id = str(uuid.uuid4())
            record = {
                **ambassador,
                "ambassador_id": ambassador_id,
                "status": "pending" if not all(requirements.values()) else "approved",
            }
            ambassadors[ambassador_id] = record
            _append_log({"action": "apply", "ambassador": record})
            data = {
                "status": record["status"],
                "ambassador_id": ambassador_id,
                "perks": PERKS if record["status"] == "approved" else [],
                "requirements_met": requirements,
            }
        elif operation == "approve":
            if not ambassador or "ambassador_id" not in ambassador:
                raise ValueError("ambassador_id required")
            amb_id = ambassador["ambassador_id"]
            if amb_id not in ambassadors:
                raise ValueError("ambassador not found")
            ambassadors[amb_id]["status"] = "approved"
            _append_log({"action": "approve", "ambassador_id": amb_id})
            data = {
                "status": "approved",
                "ambassador_id": amb_id,
                "perks": PERKS,
                "requirements_met": _requirements_met(ambassadors[amb_id]),
            }
        elif operation == "remove":
            if not ambassador or "ambassador_id" not in ambassador:
                raise ValueError("ambassador_id required")
            amb_id = ambassador["ambassador_id"]
            ambassadors.pop(amb_id, None)
            _append_log({"action": "remove", "ambassador_id": amb_id})
            data = {"status": "removed", "ambassador_id": amb_id}
        elif operation == "list":
            data = {"ambassadors": list(ambassadors.values())}
        elif operation == "metrics":
            total = len(ambassadors)
            approved = len([a for a in ambassadors.values() if a.get("status") == "approved"])
            data = {"total": total, "approved": approved, "pending": total - approved}
        else:
            raise ValueError("Unsupported operation")

        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("ambassador_manager", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _requirements_met(ambassador: dict[str, Any]) -> dict[str, bool]:
    return {
        "trust_score": ambassador.get("trust_score", 0) > 60,
        "account_age": ambassador.get("account_age_days", 0) > 90,
        "community_contributions": (
            ambassador.get("bounties_completed", 0) >= 3
            or ambassador.get("referrals", 0) >= 10
        ),
    }


def _load_ambassadors() -> dict[str, dict[str, Any]]:
    ambassadors: dict[str, dict[str, Any]] = {}
    if not os.path.exists(LOG_PATH):
        return ambassadors
    with open(LOG_PATH, "r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            payload = json.loads(line)
            action = payload.get("action")
            if action == "apply":
                record = payload.get("ambassador", {})
                ambassadors[record.get("ambassador_id")] = record
            elif action == "approve":
                amb_id = payload.get("ambassador_id")
                if amb_id in ambassadors:
                    ambassadors[amb_id]["status"] = "approved"
            elif action == "remove":
                ambassadors.pop(payload.get("ambassador_id"), None)
    return ambassadors


def _append_log(entry: dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    entry["logged_at"] = datetime.now(timezone.utc).isoformat()
    with open(LOG_PATH, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry) + "\n")


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
