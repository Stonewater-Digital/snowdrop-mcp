"""Blue sky filing fee calculator.
Estimates registration costs per state based on offering amount.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "blue_sky_filing_fee_calculator",
    "description": "Calculates blue sky filing fees using schedule caps and minimums.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "offering_amount": {"type": "number"},
            "states": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["offering_amount", "states"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}

STATE_MIN_FEES = {
    "CA": 300,
    "NY": 500,
    "TX": 150,
    "FL": 200,
}

STATE_MAX_FEES = {
    "CA": 2500,
    "NY": 1200,
    "TX": 750,
    "FL": 1000,
}


def blue_sky_filing_fee_calculator(offering_amount: float, states: Sequence[str], **_: Any) -> dict[str, Any]:
    """Return filing fee schedule per state and aggregate total."""
    try:
        results = []
        total = 0.0
        for state in states:
            min_fee = STATE_MIN_FEES.get(state.upper(), 100)
            max_fee = STATE_MAX_FEES.get(state.upper(), 500)
            calc_fee = min(max(offering_amount * 0.0005, min_fee), max_fee)
            results.append({"state": state.upper(), "fee": round(calc_fee, 2)})
            total += calc_fee
        data = {
            "filing_fees": results,
            "total_fee": round(total, 2),
            "average_fee": round(total / len(results), 2) if results else 0.0,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("blue_sky_filing_fee_calculator failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
