"""Spread convexity approximator for CDS positions.
Provides gamma-like metric for large spread moves.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "cds_convexity_calculator",
    "description": "Estimates convexity impact from nonlinear CDS spread moves.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "notional": {"type": "number"},
            "pv01": {"type": "number"},
            "spread_delta_bps": {"type": "number"},
            "spread_gamma": {"type": "number", "default": 0.0},
        },
        "required": ["notional", "pv01", "spread_delta_bps"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def cds_convexity_calculator(
    notional: float,
    pv01: float,
    spread_delta_bps: float,
    spread_gamma: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Return first and second-order P&L for spread move."""
    try:
        linear_pnl = pv01 * spread_delta_bps
        convexity = 0.5 * spread_gamma * (spread_delta_bps / 100) ** 2 * notional
        total = linear_pnl + convexity
        breakeven = 0.0
        if spread_gamma and linear_pnl * spread_gamma < 0:
            breakeven = ((-2 * linear_pnl) / (spread_gamma * notional)) ** 0.5 * 100 if notional else 0.0
        data = {
            "linear_pnl": round(linear_pnl, 2),
            "convexity_adjustment": round(convexity, 2),
            "total_pnl": round(total, 2),
            "breakeven_move_bps": round(breakeven, 4),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("cds_convexity_calculator failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
