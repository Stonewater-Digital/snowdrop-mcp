"""Estimate regulatory capital required for RWA pools.
Applies risk weights and capital ratio targets to balance sheet exposures."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "rwa_regulatory_capital_calculator",
    "description": "Calculates RWA exposure and capital requirement based on risk weights and target ratios.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "asset_balance": {"type": "number", "description": "Balance of tokenized assets"},
            "risk_weight_pct": {"type": "number", "description": "Regulatory risk weight percent"},
            "capital_ratio_target_pct": {"type": "number", "description": "Target capital ratio percent"},
        },
        "required": ["asset_balance", "risk_weight_pct", "capital_ratio_target_pct"],
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


def rwa_regulatory_capital_calculator(
    asset_balance: float,
    risk_weight_pct: float,
    capital_ratio_target_pct: float,
    **_: Any,
) -> dict[str, Any]:
    """Compute required capital for RWA book.

    Args:
        asset_balance: Exposure balance.
        risk_weight_pct: Regulatory risk weight.
        capital_ratio_target_pct: Capital requirement percent.

    Returns:
        Dict containing RWA amount and required capital.
    """
    try:
        rwa_amount = asset_balance * risk_weight_pct / 100
        required_capital = rwa_amount * capital_ratio_target_pct / 100
        data = {
            "rwa_amount": round(rwa_amount, 2),
            "required_capital": round(required_capital, 2),
            "capital_ratio_excess_pct": round((required_capital / asset_balance * 100) if asset_balance else 0.0, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("rwa_regulatory_capital_calculator failure: %s", exc)
        log_lesson(f"rwa_regulatory_capital_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
