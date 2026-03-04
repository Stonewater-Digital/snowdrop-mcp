"""Recovery rate stress-testing for CDS pricing.
Evaluates spread impact across user-defined recovery scenarios.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "cds_recovery_rate_sensitivity",
    "description": "Analyzes CDS spread sensitivity to recovery rate scenarios.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "base_spread_bps": {"type": "number"},
            "recovery_scenarios_pct": {"type": "array", "items": {"type": "number"}},
            "default_probability_pct": {"type": "number"},
        },
        "required": ["base_spread_bps", "recovery_scenarios_pct", "default_probability_pct"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def cds_recovery_rate_sensitivity(
    base_spread_bps: float,
    recovery_scenarios_pct: Sequence[float],
    default_probability_pct: float,
    **_: Any,
) -> dict[str, Any]:
    """Return recovery scenario table showing implied spread deltas."""
    try:
        base_lgd = 1 - min(max(recovery_scenarios_pct[0] if recovery_scenarios_pct else 40.0, 0.0), 100.0) / 100
        default_prob = max(default_probability_pct, 0.0) / 100
        table = []
        for rec in recovery_scenarios_pct:
            lgd = 1 - min(max(rec, 0.0), 100.0) / 100
            spread = default_prob * lgd * 1e4
            table.append(
                {
                    "recovery_rate_pct": round(rec, 2),
                    "implied_spread_bps": round(spread, 2),
                    "delta_vs_base_bps": round(spread - base_spread_bps, 2),
                }
            )
        data = {
            "base_spread_bps": round(base_spread_bps, 2),
            "scenario_results": table,
            "highest_spread_bps": max((row["implied_spread_bps"] for row in table), default=base_spread_bps),
            "lowest_spread_bps": min((row["implied_spread_bps"] for row in table), default=base_spread_bps),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("cds_recovery_rate_sensitivity failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
