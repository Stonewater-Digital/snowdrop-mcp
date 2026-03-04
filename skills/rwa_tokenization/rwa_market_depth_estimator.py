"""Estimate secondary market depth for RWA tokens.
Uses trading data to derive average depth and turnover."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Sequence
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "rwa_market_depth_estimator",
    "description": "Calculates average daily volume and depth to gauge token liquidity.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "daily_trades": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "day": {"type": "string"},
                        "volume_usd": {"type": "number"},
                        "orders": {"type": "integer"},
                    },
                    "required": ["volume_usd", "orders"],
                },
                "description": "Recent daily trading stats",
            },
            "outstanding_supply_usd": {"type": "number", "description": "Market cap of token"},
        },
        "required": ["daily_trades", "outstanding_supply_usd"],
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


def rwa_market_depth_estimator(
    daily_trades: Sequence[dict[str, Any]],
    outstanding_supply_usd: float,
    **_: Any,
) -> dict[str, Any]:
    """Summarize market depth.

    Args:
        daily_trades: Sequence of daily trading metrics.
        outstanding_supply_usd: Market capitalization.

    Returns:
        Dict with turnover ratios and typical ticket sizes.
    """
    try:
        if not daily_trades:
            raise ValueError("daily_trades must not be empty")
        avg_volume = sum(float(day.get("volume_usd", 0)) for day in daily_trades) / len(daily_trades)
        avg_orders = sum(int(day.get("orders", 0)) for day in daily_trades) / len(daily_trades)
        avg_order_size = avg_volume / avg_orders if avg_orders else 0.0
        turnover_pct = avg_volume / outstanding_supply_usd * 100 if outstanding_supply_usd else 0.0
        data = {
            "average_daily_volume": round(avg_volume, 2),
            "average_order_size": round(avg_order_size, 2),
            "turnover_pct": round(turnover_pct, 2),
            "liquidity_flag": turnover_pct > 1,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("rwa_market_depth_estimator failure: %s", exc)
        log_lesson(f"rwa_market_depth_estimator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
