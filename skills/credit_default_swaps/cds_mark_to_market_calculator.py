"""Mark-to-market valuation for CDS trades.
Compares contractual spread to current market to compute MTM P&L.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "cds_mark_to_market_calculator",
    "description": "Marks CDS positions using PV01 and spread differentials.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "notional": {"type": "number"},
            "contract_spread_bps": {"type": "number"},
            "market_spread_bps": {"type": "number"},
            "discount_factors": {"type": "array", "items": {"type": "number"}},
            "payment_interval_years": {"type": "number", "default": 0.25},
        },
        "required": ["notional", "contract_spread_bps", "market_spread_bps", "discount_factors"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def cds_mark_to_market_calculator(
    notional: float,
    contract_spread_bps: float,
    market_spread_bps: float,
    discount_factors: Sequence[float],
    payment_interval_years: float = 0.25,
    **_: Any,
) -> dict[str, Any]:
    """Return MTM valuation based on PV01 * spread delta."""
    try:
        pv01 = sum(df * payment_interval_years for df in discount_factors) * notional / 1e4
        spread_delta = market_spread_bps - contract_spread_bps
        mtm = pv01 * spread_delta
        direction = "long_protection" if spread_delta < 0 else "short_protection"
        data = {
            "pv01": round(pv01, 4),
            "spread_delta_bps": round(spread_delta, 2),
            "mtm_value": round(mtm, 2),
            "pnl_direction": direction,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("cds_mark_to_market_calculator failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
