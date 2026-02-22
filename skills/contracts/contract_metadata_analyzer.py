"""Analyze smart contract metadata for risk."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "contract_metadata_analyzer",
    "description": "Scores contract risk based on verification, usage, and deployer reputation.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "address": {"type": "string"},
            "chain": {"type": "string", "enum": ["ton", "solana", "ethereum"]},
            "metadata": {"type": "object"},
        },
        "required": ["address", "chain", "metadata"],
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


def contract_metadata_analyzer(
    address: str,
    chain: str,
    metadata: dict[str, Any],
    **_: Any,
) -> dict[str, Any]:
    """Return risk score and qualitative recommendation."""
    try:
        risk_score = 0.0
        flags: list[str] = []
        if not metadata.get("verified", False):
            risk_score += 4
            flags.append("contract not verified")
        interaction_count = int(metadata.get("interaction_count", 0))
        if interaction_count < 100:
            risk_score += 2
            flags.append("low usage")
        deployer = metadata.get("deployer_address")
        if deployer in {"0x000", "blacklist"}:
            risk_score += 3
            flags.append("untrusted deployer")
        risk_level = _risk_level(risk_score)
        recommendation = "proceed_with_caution" if risk_level != "low" else "greenlight"
        data = {
            "address": address,
            "chain": chain,
            "risk_score": round(risk_score, 2),
            "risk_level": risk_level,
            "flags": flags,
            "recommendation": recommendation,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("contract_metadata_analyzer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _risk_level(score: float) -> str:
    if score < 2:
        return "low"
    if score < 4:
        return "moderate"
    return "high"


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
