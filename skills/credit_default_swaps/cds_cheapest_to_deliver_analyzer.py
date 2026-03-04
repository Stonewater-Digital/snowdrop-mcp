"""Cheapest-to-deliver screening for CDS auctions.
Ranks deliverable obligations using bond prices and recovery assumptions.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "cds_cheapest_to_deliver_analyzer",
    "description": "Identifies the cheapest deliverable bond and expected auction recovery.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "deliverables": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "cusip": {"type": "string"},
                        "price_pct": {"type": "number"},
                        "accrued_pct": {"type": "number"},
                        "face_value": {"type": "number"},
                    },
                    "required": ["cusip", "price_pct", "accrued_pct", "face_value"],
                },
            }
        },
        "required": ["deliverables"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def cds_cheapest_to_deliver_analyzer(deliverables: Sequence[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return cheapest bond and recovery statistics."""
    try:
        ranked = sorted(
            (
                {
                    "cusip": item["cusip"],
                    "clean_price_pct": round(item["price_pct"], 3),
                    "dirty_price_pct": round(item["price_pct"] + item["accrued_pct"], 3),
                    "implied_recovery_pct": round((item["price_pct"] + item["accrued_pct"]) / 100 * 100, 2),
                    "deliverable_value": round((item["price_pct"] + item["accrued_pct"]) / 100 * item["face_value"], 2),
                }
                for item in deliverables
            ),
            key=lambda row: row["dirty_price_pct"],
        )
        top = ranked[0] if ranked else {}
        avg_recovery = sum(row["implied_recovery_pct"] for row in ranked) / len(ranked) if ranked else 0.0
        data = {
            "cheapest_to_deliver": top,
            "deliverable_rankings": ranked,
            "average_dirty_price_pct": round(sum(row["dirty_price_pct"] for row in ranked) / len(ranked), 2) if ranked else 0.0,
            "average_implied_recovery_pct": round(avg_recovery, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("cds_cheapest_to_deliver_analyzer failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
