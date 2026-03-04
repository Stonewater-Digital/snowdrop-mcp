"""Section 1231 gain/loss calculator.
Determines ordinary recapture vs capital gain treatment for business property.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "section_1231_gain_loss_calculator",
    "description": "Computes 1231 gains and recapture amounts under 5-year lookback.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "current_year_gain": {"type": "number"},
            "current_year_loss": {"type": "number"},
            "prior_lookback_losses": {"type": "number"},
        },
        "required": ["current_year_gain", "current_year_loss", "prior_lookback_losses"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def section_1231_gain_loss_calculator(
    current_year_gain: float,
    current_year_loss: float,
    prior_lookback_losses: float,
    **_: Any,
) -> dict[str, Any]:
    """Return amounts treated as ordinary vs capital."""
    try:
        net_gain = current_year_gain - current_year_loss
        recapture = min(max(net_gain, 0.0), prior_lookback_losses)
        capital_gain = net_gain - recapture
        data = {
            "net_gain": round(net_gain, 2),
            "ordinary_recap": round(recapture, 2),
            "capital_gain": round(capital_gain, 2),
            "capital_percentage": round(capital_gain / net_gain * 100 if net_gain > 0 else 0.0, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("section_1231_gain_loss_calculator failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
