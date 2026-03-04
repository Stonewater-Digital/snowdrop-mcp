"""
Executive Summary: Calculate maximum allowable trade slippage using order book depth analysis, spread estimation, and a 10% safety buffer.
Inputs: order (dict), market_data (dict: bid, ask, depth_bps)
Outputs: max_slippage_bps (float), estimated_impact_bps (float), current_spread_bps (float), recommended_limit_price (float)
MCP Tool Name: slippage_protection_buffer
"""
import os
import math
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "slippage_protection_buffer",
    "description": "Calculate maximum allowable slippage for a trade using bid/ask spread and order book depth. Sets max_slippage = spread + estimated_impact + 10% buffer.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "order": {
                "type": "object",
                "description": "Order dict with: token_pair (str), amount_usd (float), side ('buy'/'sell'), exchange (str).",
                "properties": {
                    "token_pair": {"type": "string"},
                    "amount_usd": {"type": "number"},
                    "side": {"type": "string", "enum": ["buy", "sell"]},
                    "exchange": {"type": "string"}
                },
                "required": ["token_pair", "amount_usd", "side", "exchange"]
            },
            "market_data": {
                "type": "object",
                "description": "Market data dict with: bid (float), ask (float), depth_bps (list of {price_level, quantity}).",
                "properties": {
                    "bid": {"type": "number"},
                    "ask": {"type": "number"},
                    "depth_bps": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "price_level": {"type": "number"},
                                "quantity": {"type": "number"}
                            }
                        }
                    }
                },
                "required": ["bid", "ask", "depth_bps"]
            }
        },
        "required": ["order", "market_data"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "max_slippage_bps": {"type": "number"},
            "estimated_impact_bps": {"type": "number"},
            "current_spread_bps": {"type": "number"},
            "recommended_limit_price": {"type": "number"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"}
        },
        "required": ["max_slippage_bps", "estimated_impact_bps", "current_spread_bps", "recommended_limit_price", "status", "timestamp"]
    }
}

# Safety buffer added on top of spread + impact (10%)
_SAFETY_BUFFER_MULTIPLIER = 0.10
# Minimum spread floor in bps to avoid division issues
_MIN_SPREAD_BPS = 0.1


def _compute_spread_bps(bid: float, ask: float) -> float:
    """Compute the bid-ask spread in basis points.

    Spread in bps = (ask - bid) / mid_price * 10,000

    Args:
        bid: Best bid price.
        ask: Best ask price.

    Returns:
        Spread in basis points (always non-negative).

    Raises:
        ValueError: If bid or ask are non-positive or ask < bid.
    """
    if bid <= 0 or ask <= 0:
        raise ValueError(f"bid ({bid}) and ask ({ask}) must be positive.")
    if ask < bid:
        raise ValueError(f"ask ({ask}) must be >= bid ({bid}).")

    mid = (bid + ask) / 2.0
    spread_bps = ((ask - bid) / mid) * 10_000.0
    return max(round(spread_bps, 4), _MIN_SPREAD_BPS)


def _estimate_price_impact_bps(
    amount_usd: float,
    side: str,
    bid: float,
    ask: float,
    depth_bps: list[dict],
) -> float:
    """Estimate price impact in bps by walking the order book depth.

    Price impact is computed by consuming liquidity from depth_bps levels
    until the order amount is filled, then measuring the average fill price
    vs. the best bid/ask.

    Args:
        amount_usd: Order size in USD.
        side: "buy" or "sell".
        bid: Best bid price.
        ask: Best ask price.
        depth_bps: List of {price_level (bps offset from mid), quantity (USD)} dicts.

    Returns:
        Estimated price impact in basis points.
    """
    if not depth_bps or amount_usd <= 0:
        return 0.0

    mid_price = (bid + ask) / 2.0

    # Sort depth levels by price proximity to mid
    # For buys: consume ask-side levels (positive bps offset)
    # For sells: consume bid-side levels (negative bps offset)
    if side == "buy":
        levels = sorted(
            [d for d in depth_bps if d.get("price_level", 0) >= 0],
            key=lambda d: d["price_level"]
        )
    else:
        levels = sorted(
            [d for d in depth_bps if d.get("price_level", 0) <= 0],
            key=lambda d: abs(d["price_level"])
        )

    remaining_usd = amount_usd
    weighted_price_sum = 0.0
    total_filled_usd = 0.0

    for level in levels:
        price_offset_bps = abs(level.get("price_level", 0))
        # Convert bps offset to actual price
        price_at_level = mid_price * (1 + price_offset_bps / 10_000.0)
        available_usd = float(level.get("quantity", 0))

        if available_usd <= 0:
            continue

        filled_at_this_level = min(remaining_usd, available_usd)
        weighted_price_sum += price_at_level * filled_at_this_level
        total_filled_usd += filled_at_this_level
        remaining_usd -= filled_at_this_level

        if remaining_usd <= 0:
            break

    if total_filled_usd <= 0:
        # Order is larger than all available depth — maximum impact
        if levels:
            worst_bps = abs(levels[-1].get("price_level", 0)) + 50.0
            return round(worst_bps, 4)
        return 500.0  # 5% default worst case

    avg_fill_price = weighted_price_sum / total_filled_usd
    reference_price = ask if side == "buy" else bid

    impact_bps = abs(avg_fill_price - reference_price) / reference_price * 10_000.0

    # If order couldn't be fully filled, add a partial-fill penalty
    if remaining_usd > 0:
        unfilled_ratio = remaining_usd / amount_usd
        impact_bps += unfilled_ratio * 100.0  # 1% penalty per 10% unfilled

    return round(impact_bps, 4)


def _compute_limit_price(
    side: str,
    bid: float,
    ask: float,
    max_slippage_bps: float,
) -> float:
    """Compute the recommended limit price given max slippage.

    Buy limit: ask * (1 + max_slippage_bps / 10_000)  — worst acceptable buy price
    Sell limit: bid * (1 - max_slippage_bps / 10_000)  — worst acceptable sell price

    Args:
        side: "buy" or "sell".
        bid: Best bid price.
        ask: Best ask price.
        max_slippage_bps: Maximum acceptable slippage in basis points.

    Returns:
        Recommended limit price rounded to 8 decimal places.
    """
    slippage_factor = max_slippage_bps / 10_000.0
    if side == "buy":
        limit = ask * (1.0 + slippage_factor)
    else:
        limit = bid * (1.0 - slippage_factor)
    return round(limit, 8)


def slippage_protection_buffer(order: dict, market_data: dict) -> dict:
    """Calculate maximum allowable slippage protection for a trade.

    Uses the formula:
        max_slippage_bps = spread_bps + estimated_impact_bps + (10% buffer of their sum)

    The 10% safety buffer accounts for transient market microstructure noise
    (e.g. quote refreshes, momentary liquidity gaps) without being so wide
    that the protection is meaningless.

    Args:
        order: Order dict with token_pair, amount_usd, side ("buy"/"sell"), exchange.
        market_data: Market data dict with bid, ask, and depth_bps (list of
            {price_level (bps from mid), quantity (USD available)} dicts).

    Returns:
        A dict with keys:
            - max_slippage_bps (float): Maximum tolerable slippage in bps.
            - estimated_impact_bps (float): Estimated price impact from depth walk.
            - current_spread_bps (float): Current bid-ask spread in bps.
            - recommended_limit_price (float): Limit price to enforce max_slippage.
            - status (str): "success" or "error".
            - timestamp (str): ISO 8601 UTC timestamp.
    """
    try:
        # Validate order fields
        required_order = {"token_pair", "amount_usd", "side", "exchange"}
        missing = required_order - set(order.keys())
        if missing:
            raise ValueError(f"order missing required fields: {missing}.")

        required_market = {"bid", "ask", "depth_bps"}
        missing_m = required_market - set(market_data.keys())
        if missing_m:
            raise ValueError(f"market_data missing required fields: {missing_m}.")

        side = str(order["side"]).strip().lower()
        if side not in ("buy", "sell"):
            raise ValueError(f"order.side must be 'buy' or 'sell', got '{side}'.")

        amount_usd = float(order["amount_usd"])
        if amount_usd <= 0:
            raise ValueError(f"order.amount_usd must be positive, got {amount_usd}.")

        bid = float(market_data["bid"])
        ask = float(market_data["ask"])
        depth_bps = market_data.get("depth_bps", [])

        if not isinstance(depth_bps, list):
            raise TypeError(f"market_data.depth_bps must be a list, got {type(depth_bps).__name__}.")

        # Compute spread
        current_spread_bps = _compute_spread_bps(bid, ask)

        # Estimate price impact via depth walk
        estimated_impact_bps = _estimate_price_impact_bps(amount_usd, side, bid, ask, depth_bps)

        # Apply 10% safety buffer on top of spread + impact
        base_slippage = current_spread_bps + estimated_impact_bps
        buffer = base_slippage * _SAFETY_BUFFER_MULTIPLIER
        max_slippage_bps = round(base_slippage + buffer, 4)

        # Compute limit price
        recommended_limit_price = _compute_limit_price(side, bid, ask, max_slippage_bps)

        # Warn if order is unusually large relative to available depth
        total_depth_usd = sum(float(d.get("quantity", 0)) for d in depth_bps)
        depth_coverage_pct = round(min(total_depth_usd / amount_usd * 100, 100.0), 2) if amount_usd else 100.0

        return {
            "status": "success",
            "max_slippage_bps": max_slippage_bps,
            "estimated_impact_bps": estimated_impact_bps,
            "current_spread_bps": current_spread_bps,
            "recommended_limit_price": recommended_limit_price,
            "safety_buffer_bps": round(buffer, 4),
            "safety_buffer_pct": _SAFETY_BUFFER_MULTIPLIER * 100,
            "depth_coverage_pct": depth_coverage_pct,
            "order_summary": {
                "token_pair": order["token_pair"],
                "amount_usd": amount_usd,
                "side": side,
                "exchange": order.get("exchange", ""),
                "mid_price": round((bid + ask) / 2.0, 8),
                "bid": bid,
                "ask": ask,
            },
            "interpretation": {
                "max_slippage_pct": round(max_slippage_bps / 100.0, 4),
                "safe": max_slippage_bps < 100.0,  # <1% is generally safe
                "warning": "high_slippage" if max_slippage_bps >= 100.0 else None,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"slippage_protection_buffer failed: {e}")
        _log_lesson(f"slippage_protection_buffer: {e}")
        return {
            "status": "error",
            "error": str(e),
            "max_slippage_bps": 0.0,
            "estimated_impact_bps": 0.0,
            "current_spread_bps": 0.0,
            "recommended_limit_price": 0.0,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    """Append an error lesson to the lessons log file.

    Args:
        message: The lesson message to record.
    """
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        logger.warning("Could not write to logs/lessons.md")
