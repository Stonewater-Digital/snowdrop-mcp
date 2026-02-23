"""
Executive Summary: Calculates the implied probability of a merger closing based on the current market spread, target price, offer price, and unaffected price.
"""
from __future__ import annotations
from datetime import datetime, timezone
from skills.utils import log_lesson

TOOL_META = {
    "name": "merger_spread_implied_probability",
    "tier": "free",
    "description": "Calculates M&A deal closing probability from market spread, offer price, and unaffected downside.",
}

def merger_spread_implied_probability(target_ticker: str, offer_price: float, current_price: float, unaffected_price: float) -> dict:
    """Calculate the market-implied probability of an M&A transaction closing.
    
    Args:
        target_ticker: Ticker symbol of the target company
        offer_price: The acquisition offer price per share
        current_price: The current trading price of the target
        unaffected_price: The estimated price if the deal breaks
        
    Returns:
        Dict with implied closing probability, gross spread, and downside risk.
    """
    try:
        ts = datetime.now(timezone.utc)
        
        # Gross spread
        if current_price >= offer_price:
            implied_prob = 1.0
            gross_spread = 0.0
        elif current_price <= unaffected_price:
            implied_prob = 0.0
            gross_spread = (offer_price - current_price) / current_price
        else:
            # (Current - Unaffected) / (Offer - Unaffected)
            implied_prob = (current_price - unaffected_price) / (offer_price - unaffected_price)
            gross_spread = (offer_price - current_price) / current_price
            
        # Downside risk
        downside_risk = (current_price - unaffected_price) / current_price
        
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
                "market_sentiment": "High Confidence" if implied_prob > 0.8 else ("Skeptical" if implied_prob < 0.5 else "Neutral")
            },
            "timestamp": ts.isoformat()
        }
    except Exception as e:
        log_lesson(f"merger_spread_implied_probability: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
