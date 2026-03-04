"""Jump-to-default P&L estimator for CDS positions.
Measures immediate mark shock if name defaults overnight.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "cds_jump_to_default_calculator",
    "description": "Calculates jump-to-default impact using LGD and recovery assumptions.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "notional": {"type": "number"},
            "recovery_rate_pct": {"type": "number"},
            "current_spread_bps": {"type": "number"},
            "accrued_coupon_bps": {"type": "number", "default": 25.0},
        },
        "required": ["notional", "recovery_rate_pct", "current_spread_bps"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def cds_jump_to_default_calculator(
    notional: float,
    recovery_rate_pct: float,
    current_spread_bps: float,
    accrued_coupon_bps: float = 25.0,
    **_: Any,
) -> dict[str, Any]:
    """Return LGD settlement, accrued coupon, and P&L direction."""
    try:
        lgd = 1 - min(max(recovery_rate_pct, 0.0), 100.0) / 100
        payout = notional * lgd
        accrued = notional * accrued_coupon_bps / 1e4
        pnl = payout - accrued if current_spread_bps >= 0 else -payout
        data = {
            "lgd_settlement": round(payout, 2),
            "accrued_coupon": round(accrued, 2),
            "jump_pnl": round(pnl, 2),
            "direction": "long_protection" if pnl > 0 else "short_protection",
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("cds_jump_to_default_calculator failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
