"""Estimate executable liquidity depth across DEX order books.
Accumulated liquidity stops once a slippage threshold is reached."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Sequence
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "on_chain_liquidity_depth_estimator",
    "description": "Aggregates order book levels until price impact exceeds a defined slippage limit.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "orderbook_levels": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "price": {"type": "number"},
                        "size": {"type": "number"},
                    },
                    "required": ["price", "size"],
                },
                "description": "Price/size tuples sorted best to worst.",
            },
            "mid_price": {"type": "number", "description": "Reference mid-market price"},
            "max_slippage_pct": {"type": "number", "description": "Allowed slippage percent", "default": 1.0},
        },
        "required": ["orderbook_levels", "mid_price"],
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


def on_chain_liquidity_depth_estimator(
    orderbook_levels: Sequence[dict[str, float]],
    mid_price: float,
    max_slippage_pct: float = 1.0,
    **_: Any,
) -> dict[str, Any]:
    """Aggregate available liquidity up to a slippage threshold.

    Args:
        orderbook_levels: Ordered pairs of price and available size.
        mid_price: Prevailing mid price used to define slippage.
        max_slippage_pct: Maximum percent deviation from mid price.

    Returns:
        Payload describing executable notional and weighted-average price.
    """
    try:
        if mid_price <= 0:
            raise ValueError("mid_price must be positive")
        cumulative_size = 0.0
        notional = 0.0
        last_price = mid_price
        hit_limit = False
        for level in orderbook_levels:
            price = float(level.get("price", 0))
            size = max(float(level.get("size", 0)), 0.0)
            if size <= 0 or price <= 0:
                continue
            slippage = abs(price - mid_price) / mid_price * 100
            if slippage > max_slippage_pct:
                hit_limit = cumulative_size > 0
                break
            cumulative_size += size
            notional += size * price
            last_price = price
        avg_price = notional / cumulative_size if cumulative_size else 0.0
        data = {
            "executable_volume": round(cumulative_size, 4),
            "weighted_average_price": round(avg_price, 6),
            "last_price_level": round(last_price, 6),
            "slippage_reached": hit_limit,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("on_chain_liquidity_depth_estimator failure: %s", exc)
        log_lesson(f"on_chain_liquidity_depth_estimator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
