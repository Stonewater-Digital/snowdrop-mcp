"""Estimate liquidity premium demanded for RWA tokens.
Outputs yield targets from base rates plus illiquidity spread."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "rwa_liquidity_premium_calculator",
    "description": "Combines base rates, liquidity spreads, and tenor adjustments to set yield targets.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "base_rate_pct": {"type": "number", "description": "Risk-free benchmark rate"},
            "illiquidity_spread_bps": {"type": "number", "description": "Spread per 100 bps of illiquidity"},
            "tenor_years": {"type": "number", "description": "Investment tenor in years"},
        },
        "required": ["base_rate_pct", "illiquidity_spread_bps", "tenor_years"],
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


def rwa_liquidity_premium_calculator(
    base_rate_pct: float,
    illiquidity_spread_bps: float,
    tenor_years: float,
    **_: Any,
) -> dict[str, Any]:
    """Combine rate components to set required return.

    Args:
        base_rate_pct: Benchmark rate for similar tenor.
        illiquidity_spread_bps: Additional compensation required.
        tenor_years: Duration of lockup.

    Returns:
        Dict containing total target yield and premium breakdown.
    """
    try:
        liquidity_premium_pct = illiquidity_spread_bps / 100
        tenor_adjustment_pct = max(tenor_years - 1, 0) * 0.2
        required_return = base_rate_pct + liquidity_premium_pct + tenor_adjustment_pct
        data = {
            "base_rate_pct": base_rate_pct,
            "liquidity_premium_pct": round(liquidity_premium_pct, 2),
            "tenor_adjustment_pct": round(tenor_adjustment_pct, 2),
            "required_return_pct": round(required_return, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("rwa_liquidity_premium_calculator failure: %s", exc)
        log_lesson(f"rwa_liquidity_premium_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
