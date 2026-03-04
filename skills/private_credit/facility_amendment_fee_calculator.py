"""Calculate consent fees for facility amendments."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "facility_amendment_fee_calculator",
    "description": "Computes amendment consent fees based on participation levels.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "facility_size": {"type": "number"},
            "consent_obtained_pct": {"type": "number"},
            "required_consent_pct": {"type": "number"},
            "base_fee_bps": {"type": "number"},
            "incentive_fee_bps": {"type": "number", "default": 0.0},
        },
        "required": ["facility_size", "consent_obtained_pct", "required_consent_pct", "base_fee_bps"],
    },
    "outputSchema": {"type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def facility_amendment_fee_calculator(
    facility_size: float,
    consent_obtained_pct: float,
    required_consent_pct: float,
    base_fee_bps: float,
    incentive_fee_bps: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Return total consent fee outlay and per-lender check."""
    try:
        if required_consent_pct <= 0:
            raise ValueError("required_consent_pct must be positive")
        participation_ratio = consent_obtained_pct / required_consent_pct
        participation_ratio = min(participation_ratio, 1.5)
        fee_bps = base_fee_bps * participation_ratio
        if consent_obtained_pct >= 90:
            fee_bps += incentive_fee_bps
        total_fee = facility_size * (fee_bps / 10000)
        data = {
            "effective_fee_bps": round(fee_bps, 2),
            "total_fee_amount": round(total_fee, 2),
            "per_100k_check": round(100000 * (fee_bps / 10000), 2),
            "consent_shortfall_pct": max(required_consent_pct - consent_obtained_pct, 0.0),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("facility_amendment_fee_calculator", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
