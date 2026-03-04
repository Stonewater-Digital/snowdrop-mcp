"""Correlation basket analytics for CDS tranches.
Estimates tranche loss versus correlation inputs for simple baskets.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "cds_correlation_basket_analyzer",
    "description": "Analyzes basket correlation scenarios and tranche loss contributions.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "exposures": {"type": "array", "items": {"type": "number"}},
            "base_correlation": {"type": "number"},
            "attachment_points_pct": {"type": "array", "items": {"type": "number"}},
            "detachment_points_pct": {"type": "array", "items": {"type": "number"}},
        },
        "required": ["exposures", "base_correlation", "attachment_points_pct", "detachment_points_pct"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def cds_correlation_basket_analyzer(
    exposures: Sequence[float],
    base_correlation: float,
    attachment_points_pct: Sequence[float],
    detachment_points_pct: Sequence[float],
    **_: Any,
) -> dict[str, Any]:
    """Return tranche expected loss across basic correlation shocks."""
    try:
        portfolio_notional = sum(exposures)
        tranche_results = []
        shocks = [-0.1, 0.0, 0.1]
        for attach, detach in zip(attachment_points_pct, detachment_points_pct):
            tranche_width = max(detach - attach, 0.0)
            losses = []
            for shock in shocks:
                corr = max(min(base_correlation + shock, 0.99), 0.01)
                expected_loss_pct = (1 - corr) * tranche_width / 100
                losses.append({"correlation": round(corr, 3), "expected_loss_pct": round(expected_loss_pct * 100, 2)})
            tranche_results.append(
                {
                    "attachment_pct": attach,
                    "detachment_pct": detach,
                    "expected_loss_scenarios": losses,
                }
            )
        data = {
            "portfolio_notional": round(portfolio_notional, 2),
            "tranche_analysis": tranche_results,
            "avg_correlation": round(base_correlation, 3),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("cds_correlation_basket_analyzer failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
