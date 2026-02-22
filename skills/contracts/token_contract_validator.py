"""Validate token contract safety controls."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "token_contract_validator",
    "description": "Flags risky token authority settings and liquidity constraints.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "token": {"type": "object"},
        },
        "required": ["token"],
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


def token_contract_validator(token: dict[str, Any], **_: Any) -> dict[str, Any]:
    """Return safety flags for a token contract."""
    try:
        flags = []
        risk_score = 0.0
        if token.get("mint_authority"):
            risk_score += 3
            flags.append("mint authority active")
        if token.get("freeze_authority"):
            risk_score += 2
            flags.append("freeze authority active")
        if int(token.get("holders", 0)) < 100:
            risk_score += 1.5
            flags.append("low holder count")
        if float(token.get("liquidity_usd", 0.0)) < 10_000:
            risk_score += 2.5
            flags.append("low liquidity")
        safe = risk_score < 3
        data = {
            "safe": safe,
            "flags": flags,
            "risk_score": round(risk_score, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("token_contract_validator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
