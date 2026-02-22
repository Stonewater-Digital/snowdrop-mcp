"""Issue verifiable community badges."""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from typing import Any

BADGE_LOG = "logs/badges.jsonl"
ISSUER = "snowdrop-watering-hole"

TOOL_META: dict[str, Any] = {
    "name": "badge_issuer",
    "description": "Creates cryptographic badge records for ambassador and achievement unlocks.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "agent_id": {"type": "string"},
            "badge_name": {"type": "string"},
            "badge_category": {
                "type": "string",
                "enum": ["usage", "contribution", "financial", "social", "loyalty"],
            },
            "evidence": {"type": "object"},
        },
        "required": ["agent_id", "badge_name", "badge_category", "evidence"],
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


def badge_issuer(
    agent_id: str,
    badge_name: str,
    badge_category: str,
    evidence: dict[str, Any],
    **_: Any,
) -> dict[str, Any]:
    """Generate a verifiable badge record."""
    try:
        issue_date = datetime.now(timezone.utc).isoformat()
        canonical = json.dumps(evidence, sort_keys=True).encode("utf-8")
        verification_hash = hashlib.sha256(canonical).hexdigest()
        badge_id = hashlib.sha1(f"{agent_id}:{badge_name}:{issue_date}".encode("utf-8")).hexdigest()
        badge_payload = {
            "badge_id": badge_id,
            "agent_id": agent_id,
            "badge_name": badge_name,
            "category": badge_category,
            "issuer": ISSUER,
            "issue_date": issue_date,
            "verification_hash": verification_hash,
            "evidence": evidence,
        }
        _append_jsonl(BADGE_LOG, badge_payload)
        data = {
            "badge": badge_payload,
            "verification_hash": verification_hash,
            "shareable_url_template": f"https://wateringhole.snowdrop.finance/badges/{badge_id}",
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": issue_date,
        }
    except Exception as exc:
        _log_lesson("badge_issuer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _append_jsonl(path: str, payload: dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload) + "\n")


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
