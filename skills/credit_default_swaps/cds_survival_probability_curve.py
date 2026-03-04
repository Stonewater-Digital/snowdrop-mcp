"""Bootstrap a survival probability curve.
Uses piecewise hazard rates to estimate remaining life at each tenor point.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from math import exp
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "cds_survival_probability_curve",
    "description": "Generates survival probabilities from hazard rates and tenors.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "hazard_rates": {"type": "array", "items": {"type": "number"}},
            "tenors_years": {"type": "array", "items": {"type": "number"}},
        },
        "required": ["hazard_rates", "tenors_years"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def cds_survival_probability_curve(
    hazard_rates: Sequence[float],
    tenors_years: Sequence[float],
    **_: Any,
) -> dict[str, Any]:
    """Return tenor-aligned survival probabilities."""
    try:
        points = min(len(hazard_rates), len(tenors_years))
        cumulative_intensity = 0.0
        survival = []
        last_tenor = 0.0
        for idx in range(points):
            tenor = max(tenors_years[idx], last_tenor)
            dt = tenor - last_tenor
            cumulative_intensity += max(hazard_rates[idx], 0.0) * dt
            prob = exp(-cumulative_intensity)
            survival.append({"tenor_years": tenor, "survival_probability": round(prob, 6)})
            last_tenor = tenor
        curve_shape = "steep" if survival and survival[0]["survival_probability"] - survival[-1]["survival_probability"] > 0.3 else "flat"
        data = {
            "survival_curve": survival,
            "terminal_probability": round(survival[-1]["survival_probability"], 6) if survival else 1.0,
            "curve_shape": curve_shape,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("cds_survival_probability_curve failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
