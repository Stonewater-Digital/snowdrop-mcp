"""Capital gains tax calculator.
Determines short vs long-term gains and effective tax rate.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "capital_gains_tax_calculator",
    "description": "Calculates realized capital gain tax based on holding period and jurisdiction.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "proceeds": {"type": "number"},
            "cost_basis": {"type": "number"},
            "holding_period_days": {"type": "number"},
            "federal_rate_long_pct": {"type": "number", "default": 20.0},
            "federal_rate_short_pct": {"type": "number", "default": 37.0},
            "state_rate_pct": {"type": "number", "default": 5.0},
        },
        "required": ["proceeds", "cost_basis", "holding_period_days"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def capital_gains_tax_calculator(
    proceeds: float,
    cost_basis: float,
    holding_period_days: float,
    federal_rate_long_pct: float = 20.0,
    federal_rate_short_pct: float = 37.0,
    state_rate_pct: float = 5.0,
    **_: Any,
) -> dict[str, Any]:
    """Return gain amount and tax breakdown."""
    try:
        gain = proceeds - cost_basis
        classification = "long_term" if holding_period_days >= 365 else "short_term"
        federal_rate = federal_rate_long_pct if classification == "long_term" else federal_rate_short_pct
        tax = max(gain, 0.0) * (federal_rate + state_rate_pct) / 100
        data = {
            "gain": round(gain, 2),
            "classification": classification,
            "federal_rate_pct": federal_rate,
            "state_rate_pct": state_rate_pct,
            "tax_due": round(tax, 2),
            "effective_rate_pct": round(tax / gain * 100 if gain > 0 else 0.0, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("capital_gains_tax_calculator failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
