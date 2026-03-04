"""Approximate spread duration for CDS positions.
Provides DV01 and spread beta metrics for hedging.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "cds_duration_calculator",
    "description": "Calculates CDS PV01 and spread duration based on discount curve.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "notional": {"type": "number"},
            "discount_factors": {"type": "array", "items": {"type": "number"}},
            "payment_interval_years": {"type": "number", "default": 0.25},
            "spread_bps": {"type": "number"},
        },
        "required": ["notional", "discount_factors", "spread_bps"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def cds_duration_calculator(
    notional: float,
    discount_factors: Sequence[float],
    spread_bps: float,
    payment_interval_years: float = 0.25,
    **_: Any,
) -> dict[str, Any]:
    """Return DV01 and effective spread duration."""
    try:
        interval = max(payment_interval_years, 0.0)
        pv01 = sum(df * interval for df in discount_factors) * notional / 1e4
        duration_years = sum((idx + 1) * interval * df for idx, df in enumerate(discount_factors)) / sum(discount_factors) if discount_factors else 0.0
        dollar_value = pv01 * spread_bps
        data = {
            "pv01": round(pv01, 4),
            "spread_duration_years": round(duration_years, 4),
            "dollar_value_of_spread": round(dollar_value, 2),
            "weighted_payment_count": len(discount_factors),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("cds_duration_calculator failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
