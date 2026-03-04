"""Directors & Officers liability loss estimator.
Provides severity, limit adequacy, and retention guidance.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "directors_officers_liability_calculator",
    "description": "Estimates D&O expected loss, limit adequacy, and retention impacts.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "claim_frequency_pct": {"type": "number"},
            "average_claim_severity": {"type": "number"},
            "policy_limit": {"type": "number"},
            "retention": {"type": "number"},
            "market_cap": {"type": "number"},
        },
        "required": ["claim_frequency_pct", "average_claim_severity", "policy_limit", "retention", "market_cap"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def directors_officers_liability_calculator(
    claim_frequency_pct: float,
    average_claim_severity: float,
    policy_limit: float,
    retention: float,
    market_cap: float,
    **_: Any,
) -> dict[str, Any]:
    """Return expected annual loss and capital at risk."""
    try:
        freq = max(claim_frequency_pct, 0.0) / 100
        expected_loss = freq * max(min(average_claim_severity, policy_limit), 0.0)
        retention_share = min(retention / policy_limit, 1.0) if policy_limit else 0.0
        limit_adequacy = "adequate" if policy_limit >= average_claim_severity * 1.5 else "tight"
        data = {
            "expected_loss": round(expected_loss, 2),
            "retention_share_pct": round(retention_share * 100, 2),
            "limit_adequacy": limit_adequacy,
            "loss_to_market_cap_pct": round(expected_loss / market_cap * 100 if market_cap else 0.0, 4),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("directors_officers_liability_calculator failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
