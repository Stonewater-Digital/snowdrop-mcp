"""Corporate property catastrophe exposure model.
Aggregates location limits and indicates catastrophe stress metrics.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "corporate_property_cat_exposure_model",
    "description": "Summarizes property exposure by peril zone and cat return periods.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "locations": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "tiv": {"type": "number"},
                        "zone": {"type": "string"},
                        "probable_max_loss_pct": {"type": "number"},
                    },
                    "required": ["name", "tiv", "zone", "probable_max_loss_pct"],
                },
            }
        },
        "required": ["locations"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def corporate_property_cat_exposure_model(locations: Sequence[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return max location limits, total PMLs, and zone concentration."""
    try:
        total_tiv = sum(loc.get("tiv", 0.0) for loc in locations)
        zone_totals: dict[str, float] = {}
        pml_total = 0.0
        for loc in locations:
            pml = loc["tiv"] * loc["probable_max_loss_pct"] / 100
            pml_total += pml
            zone_totals[loc["zone"]] = zone_totals.get(loc["zone"], 0.0) + loc["tiv"]
        concentration_zone = max(zone_totals.items(), key=lambda item: item[1]) if zone_totals else ("n/a", 0.0)
        data = {
            "total_tiv": round(total_tiv, 2),
            "aggregate_pml": round(pml_total, 2),
            "zone_concentrations": {k: round(v / total_tiv * 100, 2) if total_tiv else 0.0 for k, v in zone_totals.items()},
            "peak_zone": {"zone": concentration_zone[0], "tiv_share_pct": round(concentration_zone[1] / total_tiv * 100 if total_tiv else 0.0, 2)},
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("corporate_property_cat_exposure_model failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
