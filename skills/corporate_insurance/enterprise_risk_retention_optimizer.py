"""Enterprise retention optimizer.
Determines optimal retention level balancing volatility and cost.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "enterprise_risk_retention_optimizer",
    "description": "Selects corporate retention using expected loss curve and premium quotes.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "retention_options": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "retention": {"type": "number"},
                        "premium": {"type": "number"},
                        "expected_loss": {"type": "number"},
                    },
                    "required": ["retention", "premium", "expected_loss"],
                },
            }
        },
        "required": ["retention_options"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def enterprise_risk_retention_optimizer(retention_options: Sequence[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return total cost and pick best retention level."""
    try:
        ranked = []
        for option in retention_options:
            total_cost = option["premium"] + option["expected_loss"]
            volatility_proxy = option["retention"] * 0.1
            score = total_cost + volatility_proxy
            ranked.append({"retention": option["retention"], "total_cost": total_cost, "score": score})
        ranked.sort(key=lambda row: row["score"])
        recommendation = ranked[0] if ranked else {}
        data = {
            "retention_analysis": [{"retention": row["retention"], "total_cost": round(row["total_cost"], 2), "score": round(row["score"], 2)} for row in ranked],
            "optimal_retention": recommendation,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("enterprise_risk_retention_optimizer failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
