"""Estimate custody costs for off-chain collateral.
Converts basis point fees and flat retainers into annual totals."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "rwa_custody_cost_calculator",
    "description": "Summarizes custody expenses for RWA structures using AUC fees and retainers.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "assets_under_custody": {"type": "number", "description": "Collateral value held by custodian"},
            "custody_fee_bps": {"type": "number", "description": "Annual basis points on AUC"},
            "flat_fee_usd": {"type": "number", "description": "Annual retainer"},
        },
        "required": ["assets_under_custody", "custody_fee_bps", "flat_fee_usd"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"},
            "error": {"type": "string"},
        },
    },
}


def rwa_custody_cost_calculator(
    assets_under_custody: float,
    custody_fee_bps: float,
    flat_fee_usd: float,
    **_: Any,
) -> dict[str, Any]:
    """Calculate annual custody costs.

    Args:
        assets_under_custody: Value of assets held.
        custody_fee_bps: Basis points charged annually.
        flat_fee_usd: Fixed annual fee.

    Returns:
        Dict with total fee and cost per asset unit.
    """
    try:
        basis_point_fee = assets_under_custody * custody_fee_bps / 10_000
        total_fee = basis_point_fee + flat_fee_usd
        cost_pct = total_fee / assets_under_custody * 100 if assets_under_custody else 0.0
        data = {
            "basis_point_fee": round(basis_point_fee, 2),
            "total_fee": round(total_fee, 2),
            "cost_pct": round(cost_pct, 3),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("rwa_custody_cost_calculator failure: %s", exc)
        log_lesson(f"rwa_custody_cost_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
