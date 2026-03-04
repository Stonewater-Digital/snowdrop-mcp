"""CDS protection leg present value engine.
Aggregates expected default settlement flows across tenor buckets.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "cds_protection_leg_pv",
    "description": "Computes PV of CDS protection leg using default probabilities.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "notional": {"type": "number"},
            "default_probabilities": {"type": "array", "items": {"type": "number"}},
            "discount_factors": {"type": "array", "items": {"type": "number"}},
            "recovery_rate_pct": {"type": "number", "default": 40.0},
        },
        "required": ["notional", "default_probabilities", "discount_factors"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def cds_protection_leg_pv(
    notional: float,
    default_probabilities: Sequence[float],
    discount_factors: Sequence[float],
    recovery_rate_pct: float = 40.0,
    **_: Any,
) -> dict[str, Any]:
    """Return PV of protection leg, expecting incremental probabilities per period."""
    try:
        loss_given_default = 1 - max(min(recovery_rate_pct, 100.0), 0.0) / 100
        periods = min(len(default_probabilities), len(discount_factors))
        pv = 0.0
        cumulative_default = 0.0
        breakdown = []
        for idx in range(periods):
            incremental_default = max(default_probabilities[idx] - cumulative_default, 0.0)
            cumulative_default = max(cumulative_default, default_probabilities[idx])
            expected_payment = notional * loss_given_default * incremental_default
            discounted = expected_payment * discount_factors[idx]
            pv += discounted
            breakdown.append(
                {
                    "period": idx + 1,
                    "incremental_default_pct": round(incremental_default * 100, 4),
                    "discount_factor": round(discount_factors[idx], 6),
                    "discounted_payment": round(discounted, 2),
                }
            )
        data = {
            "protection_leg_pv": round(pv, 2),
            "loss_given_default_pct": round(loss_given_default * 100, 2),
            "period_breakdown": breakdown,
            "cumulative_default_pct": round(cumulative_default * 100, 4),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("cds_protection_leg_pv failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
