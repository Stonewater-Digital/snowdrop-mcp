"""Issue compatibility certificates to agents."""
from __future__ import annotations

import hashlib
from datetime import datetime, timedelta, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "agent_certification_issuer",
    "description": "Generates signed certificates for agents who pass compatibility tests.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "agent_id": {"type": "string"},
            "compatibility_score": {"type": "number"},
            "test_date": {"type": "string"},
            "certification_level": {
                "type": "string",
                "enum": ["bronze", "silver", "gold"],
            },
        },
        "required": ["agent_id", "compatibility_score", "test_date", "certification_level"],
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


def agent_certification_issuer(
    agent_id: str,
    compatibility_score: float,
    test_date: str,
    certification_level: str,
    **_: Any,
) -> dict[str, Any]:
    """Return a certificate payload with verification hash."""
    try:
        issue_date = datetime.now(timezone.utc)
        expiry = issue_date + timedelta(days=365)
        cert_id = hashlib.sha1(f"{agent_id}:{issue_date.isoformat()}".encode("utf-8")).hexdigest()
        payload = {
            "cert_id": cert_id,
            "agent_id": agent_id,
            "level": certification_level,
            "issue_date": issue_date.isoformat(),
            "expiry_date": expiry.isoformat(),
            "compatibility_score": compatibility_score,
            "test_date": test_date,
        }
        verification_hash = hashlib.sha256(str(payload).encode("utf-8")).hexdigest()
        data = {
            "certificate": payload,
            "badge_url_template": f"https://wateringhole.snowdrop.finance/certs/{cert_id}",
            "verification_endpoint": "https://api.snowdrop.finance/certs/verify",
            "valid_until": expiry.isoformat(),
        }
        data["certificate"]["verification_hash"] = verification_hash
        return {
            "status": "success",
            "data": data,
            "timestamp": issue_date.isoformat(),
        }
    except Exception as exc:
        _log_lesson("agent_certification_issuer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
