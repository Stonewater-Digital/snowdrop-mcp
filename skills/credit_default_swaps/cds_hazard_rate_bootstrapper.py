"""Approximate CDS hazard rates from spreads.
Applies a simple ratio between spreads and loss given default profile.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "cds_hazard_rate_bootstrapper",
    "description": "Bootstraps hazard rates from CDS spreads and recovery assumptions.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "spreads_bps": {"type": "array", "items": {"type": "number"}},
            "tenors_years": {"type": "array", "items": {"type": "number"}},
            "recovery_rate_pct": {"type": "number", "default": 40.0},
        },
        "required": ["spreads_bps", "tenors_years"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def cds_hazard_rate_bootstrapper(
    spreads_bps: Sequence[float],
    tenors_years: Sequence[float],
    recovery_rate_pct: float = 40.0,
    **_: Any,
) -> dict[str, Any]:
    """Return tenor hazard rates assuming flat forward LGD."""
    try:
        lgd = 1 - max(min(recovery_rate_pct, 100.0), 0.0) / 100
        points = min(len(spreads_bps), len(tenors_years))
        hazard_curve = []
        for idx in range(points):
            spread = spreads_bps[idx] / 1e4
            hazard = spread / lgd if lgd else 0.0
            hazard_curve.append({"tenor_years": tenors_years[idx], "hazard_rate": round(hazard, 6)})
        slope = "steepener" if points >= 2 and hazard_curve[-1]["hazard_rate"] - hazard_curve[0]["hazard_rate"] > 0 else "flattener"
        data = {"hazard_curve": hazard_curve, "recovery_rate_pct": round((1 - lgd) * 100, 2), "curve_bias": slope}
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("cds_hazard_rate_bootstrapper failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
