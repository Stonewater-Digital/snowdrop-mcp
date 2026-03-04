"""Convert CDS upfront payments to running spreads.
Applies standard PV01 approximations for quick quote translation.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "cds_upfront_to_running_converter",
    "description": "Converts CDS upfront percentage into equivalent running spread.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "notional": {"type": "number"},
            "upfront_pct": {"type": "number"},
            "risky_annuity": {"type": "number"},
            "coupon_bps": {"type": "number", "default": 100.0},
        },
        "required": ["notional", "upfront_pct", "risky_annuity"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def cds_upfront_to_running_converter(
    notional: float,
    upfront_pct: float,
    risky_annuity: float,
    coupon_bps: float = 100.0,
    **_: Any,
) -> dict[str, Any]:
    """Return equivalent running spread and clean price."""
    try:
        upfront_amount = notional * upfront_pct / 100
        annuity = risky_annuity if risky_annuity else 1.0
        incremental_spread = (upfront_amount / annuity / notional) * 1e4 if (annuity and notional) else 0.0
        fair_spread = coupon_bps + incremental_spread
        dirty_price = coupon_bps + fair_spread
        data = {
            "upfront_amount": round(upfront_amount, 2),
            "equivalent_running_spread_bps": round(fair_spread, 2),
            "dirty_price_bps": round(dirty_price, 2),
            "risky_annuity": risky_annuity,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("cds_upfront_to_running_converter failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
