"""Compute CDS breakeven spread from PV legs.
Bridges premium and protection leg assumptions to yield par coupon.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "cds_breakeven_spread",
    "description": "Calculates running spread that equates premium and protection PVs.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "notional": {"type": "number"},
            "protection_leg_pv": {"type": "number"},
            "discount_factors": {"type": "array", "items": {"type": "number"}},
            "payment_interval_years": {"type": "number", "default": 0.25},
        },
        "required": ["notional", "protection_leg_pv", "discount_factors"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def cds_breakeven_spread(
    notional: float,
    protection_leg_pv: float,
    discount_factors: Sequence[float],
    payment_interval_years: float = 0.25,
    **_: Any,
) -> dict[str, Any]:
    """Return breakeven running spread in basis points."""
    try:
        interval = max(payment_interval_years, 0.0)
        annuity = sum(df * interval for df in discount_factors)
        spread_decimal = protection_leg_pv / (notional * annuity) if (notional and annuity) else 0.0
        spread_bps = spread_decimal * 1e4
        data = {
            "breakeven_spread_bps": round(spread_bps, 3),
            "risky_annuity": round(annuity * notional, 4),
            "payment_count": len(discount_factors),
            "premium_leg_pv": round(spread_decimal * notional * annuity, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("cds_breakeven_spread failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
