"""Model fair value for RWA tokens in secondary trading.
Uses VWAP and volatility to output price bands."""
from __future__ import annotations

from datetime import datetime, timezone
from statistics import pstdev
from typing import Any, Sequence
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "rwa_secondary_market_price_model",
    "description": "Calculates VWAP and volatility-based bands for RWA tokens on secondary markets.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "trades": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "price": {"type": "number"},
                        "volume": {"type": "number"},
                    },
                    "required": ["price", "volume"],
                },
                "description": "List of recent trades",
            }
        },
        "required": ["trades"],
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


def rwa_secondary_market_price_model(
    trades: Sequence[dict[str, float]],
    **_: Any,
) -> dict[str, Any]:
    """Compute VWAP and volatility bands.

    Args:
        trades: Recent trade prices and volumes.

    Returns:
        Dict containing VWAP, 1-sigma band, and liquidity insight.
    """
    try:
        total_volume = sum(float(trade.get("volume", 0)) for trade in trades)
        if total_volume <= 0:
            raise ValueError("trades must include positive volume")
        vwap = sum(float(trade.get("price", 0)) * float(trade.get("volume", 0)) for trade in trades) / total_volume
        prices = [float(trade.get("price", 0)) for trade in trades]
        volatility = pstdev(prices) if len(prices) > 1 else 0.0
        band_upper = vwap + volatility
        band_lower = max(vwap - volatility, 0)
        data = {
            "vwap": round(vwap, 4),
            "volatility": round(volatility, 4),
            "band_upper": round(band_upper, 4),
            "band_lower": round(band_lower, 4),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("rwa_secondary_market_price_model failure: %s", exc)
        log_lesson(f"rwa_secondary_market_price_model: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
