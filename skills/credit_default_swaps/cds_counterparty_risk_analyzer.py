"""Counterparty risk scoring for CDS trades.
Calculates exposure at default and compares to credit limits.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "cds_counterparty_risk_analyzer",
    "description": "Evaluates CDS counterparty exposures versus assigned limits.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "counterparties": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "current_exposure": {"type": "number"},
                        "limit": {"type": "number"},
                        "downgrade_probability_pct": {"type": "number"},
                    },
                    "required": ["name", "current_exposure", "limit", "downgrade_probability_pct"],
                },
            }
        },
        "required": ["counterparties"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def cds_counterparty_risk_analyzer(counterparties: Sequence[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return headroom metrics and breach statuses."""
    try:
        results = []
        breaches = []
        total_exposure = 0.0
        total_limit = 0.0
        for cp in counterparties:
            exposure = cp["current_exposure"]
            limit = cp["limit"]
            headroom = limit - exposure
            utilization = exposure / limit if limit else 0.0
            total_exposure += exposure
            total_limit += limit
            status = "breach" if exposure > limit else "warning" if utilization > 0.8 else "ok"
            downgrade_prob = cp["downgrade_probability_pct"]
            stressed_exposure = exposure * (1 + downgrade_prob / 100)
            if status != "ok":
                breaches.append(cp["name"])
            results.append(
                {
                    "name": cp["name"],
                    "utilization_pct": round(utilization * 100, 2),
                    "headroom": round(headroom, 2),
                    "stressed_exposure": round(stressed_exposure, 2),
                    "status": status,
                }
            )
        portfolio_utilization = total_exposure / total_limit if total_limit else 0.0
        data = {
            "counterparty_metrics": results,
            "breaches": breaches,
            "portfolio_utilization_pct": round(portfolio_utilization * 100, 2),
            "total_exposure": round(total_exposure, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("cds_counterparty_risk_analyzer failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
