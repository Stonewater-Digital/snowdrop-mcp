"""Workers compensation experience modifier estimator.
Builds actual vs expected loss ratios to derive mod factor.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "workers_comp_experience_modifier",
    "description": "Calculates WC experience modifier from actual and expected losses.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "actual_losses": {"type": "number"},
            "expected_losses": {"type": "number"},
            "credibility_factor": {"type": "number", "default": 0.33},
            "primary_threshold": {"type": "number", "default": 250000.0},
        },
        "required": ["actual_losses", "expected_losses"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def workers_comp_experience_modifier(
    actual_losses: float,
    expected_losses: float,
    credibility_factor: float = 0.33,
    primary_threshold: float = 250_000.0,
    **_: Any,
) -> dict[str, Any]:
    """Return experience mod factor and debit/credit indication."""
    try:
        credibility = min(max(credibility_factor, 0.0), 1.0)
        primary_actual = min(actual_losses, primary_threshold)
        excess_actual = max(actual_losses - primary_threshold, 0.0)
        mod = (credibility * primary_actual + (1 - credibility) * excess_actual) / expected_losses if expected_losses else 0.0
        status = "debit" if mod > 1 else "credit"
        data = {
            "experience_mod": round(mod, 3),
            "primary_actual": round(primary_actual, 2),
            "excess_actual": round(excess_actual, 2),
            "status": status,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("workers_comp_experience_modifier failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
