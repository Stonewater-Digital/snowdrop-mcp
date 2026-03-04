"""Net/gross notional tracker for CDS books.
Summarizes exposure concentration and hedge effectiveness.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "cds_notional_risk_calculator",
    "description": "Computes gross, net, and concentration metrics for CDS notionals.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "positions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "notional": {"type": "number"},
                        "direction": {"type": "string", "enum": ["buy", "sell"]},
                    },
                    "required": ["name", "notional", "direction"],
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


def cds_notional_risk_calculator(positions: Sequence[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return notional totals and concentration ratios."""
    try:
        gross = 0.0
        net = 0.0
        concentrations: dict[str, float] = {}
        for pos in positions:
            notional = abs(pos.get("notional", 0.0))
            direction = pos.get("direction", "buy")
            gross += notional
            net += notional if direction == "buy" else -notional
            concentrations[pos.get("name", "unknown")] = concentrations.get(pos.get("name", "unknown"), 0.0) + notional
        top_name = max(concentrations.items(), key=lambda item: item[1]) if concentrations else ("n/a", 0.0)
        data = {
            "gross_notional": round(gross, 2),
            "net_notional": round(net, 2),
            "hedge_ratio": round((gross - abs(net)) / gross * 100 if gross else 0.0, 2),
            "top_concentration": {"name": top_name[0], "share_pct": round(top_name[1] / gross * 100 if gross else 0.0, 2)},
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("cds_notional_risk_calculator failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
