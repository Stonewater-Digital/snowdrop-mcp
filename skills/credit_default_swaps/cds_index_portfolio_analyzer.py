"""Aggregate CDS index portfolio metrics.
Summarizes gross, net, and sector exposures for index strategies.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "cds_index_portfolio_analyzer",
    "description": "Aggregates CDS index notionals, sectors, and risk skew.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "positions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "index": {"type": "string"},
                        "sector": {"type": "string"},
                        "notional": {"type": "number"},
                        "direction": {"type": "string", "enum": ["long", "short"]},
                        "spread_bps": {"type": "number"},
                    },
                    "required": ["index", "sector", "notional", "direction", "spread_bps"],
                },
            }
        },
        "required": ["positions"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def cds_index_portfolio_analyzer(positions: Sequence[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return portfolio gross/net exposure and sector detail."""
    try:
        gross = 0.0
        net = 0.0
        sector_map: dict[str, float] = {}
        weighted_spread = 0.0
        for pos in positions:
            notional = pos.get("notional", 0.0)
            direction = pos.get("direction", "long")
            spread = pos.get("spread_bps", 0.0)
            gross += abs(notional)
            net += notional if direction == "long" else -notional
            weighted_spread += spread * notional * (1 if direction == "long" else -1)
            sector = pos.get("sector", "unknown")
            sector_map[sector] = sector_map.get(sector, 0.0) + (notional if direction == "long" else -notional)
        avg_spread = weighted_spread / net if net else 0.0
        data = {
            "gross_notional": round(gross, 2),
            "net_notional": round(net, 2),
            "avg_effective_spread_bps": round(avg_spread, 2),
            "sector_skew": {k: round(v, 2) for k, v in sector_map.items()},
            "long_short_ratio": round((gross + net) / (gross - net), 3) if gross != abs(net) else 1.0,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("cds_index_portfolio_analyzer failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
