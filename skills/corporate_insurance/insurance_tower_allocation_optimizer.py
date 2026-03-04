"""Insurance tower allocation optimizer.
Distributes layered limits to align with loss percentiles.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "insurance_tower_allocation_optimizer",
    "description": "Aligns tower layers with modeled loss percentiles to minimize gaps.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "layers": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "attachment": {"type": "number"},
                        "limit": {"type": "number"},
                        "price": {"type": "number"},
                    },
                    "required": ["attachment", "limit", "price"],
                },
            },
            "loss_percentiles": {"type": "array", "items": {"type": "number"}},
        },
        "required": ["layers", "loss_percentiles"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def insurance_tower_allocation_optimizer(
    layers: Sequence[dict[str, Any]],
    loss_percentiles: Sequence[float],
    **_: Any,
) -> dict[str, Any]:
    """Return attachment adequacy and suggested reallocations."""
    try:
        optimized = []
        for layer in sorted(layers, key=lambda row: row["attachment"]):
            layer_top = layer["attachment"] + layer["limit"]
            covered_percentiles = [pct for pct in loss_percentiles if layer["attachment"] <= pct <= layer_top]
            adequacy = "aligned" if covered_percentiles else "gap"
            optimized.append(
                {
                    "attachment": layer["attachment"],
                    "limit": layer["limit"],
                    "price": layer["price"],
                    "adequacy": adequacy,
                    "covered_percentiles": covered_percentiles,
                }
            )
        uncovered = [pct for pct in loss_percentiles if not any(layer["attachment"] <= pct <= layer["attachment"] + layer["limit"] for layer in layers)]
        data = {
            "layer_analysis": optimized,
            "uncovered_percentiles": uncovered,
            "tower_spend": round(sum(layer["price"] for layer in layers), 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("insurance_tower_allocation_optimizer failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
