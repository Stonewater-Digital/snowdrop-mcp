"""Commercial umbrella coverage analyzer.
Evaluates stacking of limits atop primary layers.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "commercial_umbrella_coverage_analyzer",
    "description": "Determines umbrella exhaustion probabilities and gap coverage.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "primary_layers": {
                "type": "array",
                "items": {"type": "number"},
            },
            "umbrella_limit": {"type": "number"},
            "loss_curve": {"type": "array", "items": {"type": "number"}},
        },
        "required": ["primary_layers", "umbrella_limit", "loss_curve"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def commercial_umbrella_coverage_analyzer(
    primary_layers: Sequence[float],
    umbrella_limit: float,
    loss_curve: Sequence[float],
    **_: Any,
) -> dict[str, Any]:
    """Return exhaustion probability and uncovered tail."""
    try:
        total_primary = sum(primary_layers)
        attachment = total_primary
        exhaustion_prob = sum(1 for loss in loss_curve if loss > attachment) / len(loss_curve) if loss_curve else 0.0
        tail_exposure = sum(max(loss - (attachment + umbrella_limit), 0.0) for loss in loss_curve) / len(loss_curve) if loss_curve else 0.0
        data = {
            "primary_stack_limit": round(total_primary, 2),
            "umbrella_attachment": round(attachment, 2),
            "exhaustion_probability_pct": round(exhaustion_prob * 100, 2),
            "average_tail_exposure": round(tail_exposure, 2),
            "adequacy": "adequate" if tail_exposure == 0 else "gap",
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("commercial_umbrella_coverage_analyzer failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
