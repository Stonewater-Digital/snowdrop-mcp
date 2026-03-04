"""Calculate M&A deal closing probability from merger arbitrage spread."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "merger_spread_implied_probability",
    "description": "Calculates M&A deal closing probability from market spread, offer price, and unaffected downside.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "target_ticker": {"type": "string", "description": "Ticker symbol of the target company."},
            "offer_price": {"type": "number", "description": "Acquisition offer price per share. Must be > unaffected_price."},
            "current_price": {"type": "number", "description": "Current trading price of the target. Must be > 0."},
            "unaffected_price": {"type": "number", "description": "Estimated price if the deal breaks. Must be > 0."},
        },
        "required": ["target_ticker", "offer_price", "current_price", "unaffected_price"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "data": {
                "type": "object",
                "properties": {
                    "target_ticker": {"type": "string"},
                    "offer_price": {"type": "number"},
                    "current_price": {"type": "number"},
                    "unaffected_price": {"type": "number"},
                    "implied_closing_probability_pct": {"type": "number"},
                    "gross_spread_pct": {"type": "number"},
                    "downside_risk_pct": {"type": "number"},
                    "market_sentiment": {"type": "string"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def merger_spread_implied_probability(
    target_ticker: str,
    offer_price: float,
    current_price: float,
    unaffected_price: float,
    **_: Any,
) -> dict[str, Any]:
    """Calculate the market-implied probability of an M&A transaction closing.

    Uses the binary deal model:
        implied_prob = (current - unaffected) / (offer - unaffected)

    This assumes current price linearly interpolates between the break price
    (unaffected) and the deal completion price (offer).

    Args:
        target_ticker: Ticker symbol of the target company.
        offer_price: Acquisition offer price per share.
        current_price: Current trading price of the target (must be > 0).
        unaffected_price: Estimated price if the deal breaks (must be > 0).

    Returns:
        dict with implied_closing_probability_pct, gross_spread_pct,
        downside_risk_pct, and market_sentiment.
    """
    try:
        if current_price <= 0:
            raise ValueError("current_price must be positive")
        if unaffected_price <= 0:
            raise ValueError("unaffected_price must be positive")
        if offer_price <= unaffected_price:
            raise ValueError("offer_price must be greater than unaffected_price for a valid spread")

        deal_range = offer_price - unaffected_price

        if current_price >= offer_price:
            # Trading at or above offer: market fully (or over) prices deal
            implied_prob = 1.0
            gross_spread = (offer_price - current_price) / current_price
        elif current_price <= unaffected_price:
            # Trading below unaffected: market prices deal as broken
            implied_prob = 0.0
            gross_spread = (offer_price - current_price) / current_price
        else:
            # Standard case: interpolate
            implied_prob = (current_price - unaffected_price) / deal_range
            gross_spread = (offer_price - current_price) / current_price

        # Downside risk: percentage loss from current price to unaffected price
        downside_risk = (current_price - unaffected_price) / current_price

        if implied_prob > 0.8:
            sentiment = "High Confidence"
        elif implied_prob < 0.5:
            sentiment = "Skeptical"
        else:
            sentiment = "Neutral"

        return {
            "status": "success",
            "data": {
                "target_ticker": target_ticker.upper(),
                "offer_price": offer_price,
                "current_price": current_price,
                "unaffected_price": unaffected_price,
                "implied_closing_probability_pct": round(implied_prob * 100, 2),
                "gross_spread_pct": round(gross_spread * 100, 2),
                "downside_risk_pct": round(downside_risk * 100, 2),
                "market_sentiment": sentiment,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson(f"merger_spread_implied_probability: {exc}")
        return {
            "status": "error",
            "error": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
