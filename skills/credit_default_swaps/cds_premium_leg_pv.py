"""Present value of CDS premium leg cashflows.
Uses running spread, notional, and discount factors to size PV and DV01.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "cds_premium_leg_pv",
    "description": "Discounts CDS premium leg coupons to compute PV and annuity.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "notional": {"type": "number"},
            "spread_bps": {"type": "number"},
            "discount_factors": {"type": "array", "items": {"type": "number"}},
            "payment_interval_years": {"type": "number", "default": 0.25},
        },
        "required": ["notional", "spread_bps", "discount_factors"],
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


def cds_premium_leg_pv(
    notional: float,
    spread_bps: float,
    discount_factors: Sequence[float],
    payment_interval_years: float = 0.25,
    **_: Any,
) -> dict[str, Any]:
    """Return PV of premium leg and risky annuity."""
    try:
        interval = max(payment_interval_years, 0.0)
        spread_decimal = spread_bps / 1e4
        pv = 0.0
        risky_annuity = 0.0
        for df in discount_factors:
            cashflow = notional * spread_decimal * interval
            pv += cashflow * df
            risky_annuity += df * interval
        data = {
            "premium_leg_pv": round(pv, 2),
            "risky_annuity": round(risky_annuity * notional, 4),
            "equivalent_rate_pct": round((pv / (notional * len(discount_factors) * interval)) * 100 if discount_factors else 0.0, 4),
            "payment_count": len(discount_factors),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("cds_premium_leg_pv failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
