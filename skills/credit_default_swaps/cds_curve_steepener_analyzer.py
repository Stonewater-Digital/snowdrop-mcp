"""Curve steepener diagnostics for CDS spreads.
Compares short vs long tenors and quantifies roll risks.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "cds_curve_steepener_analyzer",
    "description": "Evaluates CDS curve slope and roll yield for steepener trades.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "tenors_years": {"type": "array", "items": {"type": "number"}},
            "spreads_bps": {"type": "array", "items": {"type": "number"}},
        },
        "required": ["tenors_years", "spreads_bps"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def cds_curve_steepener_analyzer(tenors_years: Sequence[float], spreads_bps: Sequence[float], **_: Any) -> dict[str, Any]:
    """Return slope metrics and trade bias."""
    try:
        points = min(len(tenors_years), len(spreads_bps))
        if points < 2:
            raise ValueError("At least two tenor points required")
        short = spreads_bps[0]
        long = spreads_bps[points - 1]
        slope = (long - short) / (tenors_years[points - 1] - tenors_years[0])
        roll = spreads_bps[1] - spreads_bps[0] if points > 1 else 0.0
        direction = "put_on_steepener" if slope > 0 else "put_on_flattener" if slope < 0 else "neutral"
        data = {
            "slope_bps_per_year": round(slope, 3),
            "front_roll_bps": round(roll, 2),
            "long_short_spread_bps": round(long - short, 2),
            "signal": direction,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("cds_curve_steepener_analyzer failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
