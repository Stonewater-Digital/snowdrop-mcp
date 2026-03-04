"""CDS P&L attribution model.
Splits daily P&L into spread, carry, curve, and FX effects.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "cds_pnl_attribution_model",
    "description": "Attributes CDS P&L into carry, spread, and curve components.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "notional": {"type": "number"},
            "spread_change_bps": {"type": "number"},
            "pv01": {"type": "number"},
            "carry_income": {"type": "number"},
            "curve_roll": {"type": "number"},
            "fx_impact": {"type": "number", "default": 0.0},
        },
        "required": ["notional", "spread_change_bps", "pv01", "carry_income", "curve_roll"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def cds_pnl_attribution_model(
    notional: float,
    spread_change_bps: float,
    pv01: float,
    carry_income: float,
    curve_roll: float,
    fx_impact: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Return attribution buckets and totals."""
    try:
        spread_pnl = pv01 * spread_change_bps
        total = spread_pnl + carry_income + curve_roll + fx_impact
        data = {
            "spread_pnl": round(spread_pnl, 2),
            "carry_income": round(carry_income, 2),
            "curve_roll": round(curve_roll, 2),
            "fx_impact": round(fx_impact, 2),
            "total_pnl": round(total, 2),
            "pnl_contributions_pct": {
                "spread": round(spread_pnl / total * 100, 2) if total else 0.0,
                "carry": round(carry_income / total * 100, 2) if total else 0.0,
                "curve": round(curve_roll / total * 100, 2) if total else 0.0,
                "fx": round(fx_impact / total * 100, 2) if total else 0.0,
            },
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("cds_pnl_attribution_model failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
