"""CDS par spread estimator and loss metrics.
Provides simplified top-of-book analytics for credit default swaps.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "cds_spread_calculator",
    "description": "Estimates CDS par spread and expected loss using default probabilities.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "notional": {"type": "number"},
            "default_probability_pct": {"type": "number"},
            "recovery_rate_pct": {"type": "number"},
            "maturity_years": {"type": "number"},
        },
        "required": ["notional", "default_probability_pct", "recovery_rate_pct", "maturity_years"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
    },
}


def cds_spread_calculator(
    notional: float,
    default_probability_pct: float,
    recovery_rate_pct: float,
    maturity_years: float,
    **_: Any,
) -> dict[str, Any]:
    """Return par spread in basis points and expected loss profile."""
    try:
        default_prob = max(default_probability_pct, 0.0) / 100
        recovery = min(max(recovery_rate_pct, 0.0), 100.0) / 100
        maturity = max(maturity_years, 0.0)
        expected_loss = notional * default_prob * (1 - recovery)
        spread_decimal = (expected_loss / notional / maturity) if (notional and maturity) else 0.0
        spread_bps = spread_decimal * 1e4
        data = {
            "par_spread_bps": round(spread_bps, 2),
            "expected_loss": round(expected_loss, 2),
            "loss_pct": round(default_prob * (1 - recovery) * 100, 4),
            "loss_given_default_pct": round((1 - recovery) * 100, 2),
            "maturity_years": maturity,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        logger.exception("cds_spread_calculator failed")
        return {
            "status": "error",
            "error": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
