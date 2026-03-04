"""Track bond-CDS basis mechanics.
Compares cash bond yields with CDS-implied spreads for arbitrage signals.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "cds_bond_basis_tracker",
    "description": "Calculates CDS basis across bonds and flags rich/cheap signals.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "bond_yields_pct": {"type": "array", "items": {"type": "number"}},
            "cds_spreads_bps": {"type": "array", "items": {"type": "number"}},
            "tenors_years": {"type": "array", "items": {"type": "number"}},
        },
        "required": ["bond_yields_pct", "cds_spreads_bps", "tenors_years"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def cds_bond_basis_tracker(
    bond_yields_pct: Sequence[float],
    cds_spreads_bps: Sequence[float],
    tenors_years: Sequence[float],
    **_: Any,
) -> dict[str, Any]:
    """Return basis table and signal classification."""
    try:
        points = min(len(bond_yields_pct), len(cds_spreads_bps), len(tenors_years))
        table = []
        rich = 0
        cheap = 0
        for idx in range(points):
            basis = bond_yields_pct[idx] * 100 - cds_spreads_bps[idx]
            signal = "rich" if basis < 0 else "cheap" if basis > 0 else "neutral"
            rich += 1 if signal == "rich" else 0
            cheap += 1 if signal == "cheap" else 0
            table.append(
                {
                    "tenor_years": tenors_years[idx],
                    "bond_yield_pct": round(bond_yields_pct[idx], 4),
                    "cds_spread_bps": round(cds_spreads_bps[idx], 2),
                    "basis_bps": round(basis, 2),
                    "signal": signal,
                }
            )
        data = {
            "basis_table": table,
            "net_signal": "rich" if rich > cheap else "cheap" if cheap > rich else "neutral",
            "average_basis_bps": round(sum(row["basis_bps"] for row in table) / len(table), 2) if table else 0.0,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("cds_bond_basis_tracker failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
