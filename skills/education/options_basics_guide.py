"""Educational guide to options trading fundamentals.

MCP Tool Name: options_basics_guide
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "options_basics_guide",
    "description": "Returns educational content on options: calls/puts, intrinsic/extrinsic value, the Greeks, and basic strategies.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def options_basics_guide() -> dict[str, Any]:
    """Returns educational content on options trading fundamentals."""
    try:
        return {
            "status": "ok",
            "data": {
                "definition": "An option is a financial derivative contract that gives the buyer the right, but not the obligation, to buy (call) or sell (put) an underlying asset at a specified price (strike) on or before a certain date (expiration). The seller (writer) has the obligation to fulfill the contract if exercised.",
                "key_concepts": [
                    "Options are leveraged instruments — small premium controls a larger position",
                    "Buyers have limited risk (premium paid) but unlimited profit potential (calls) or substantial profit potential (puts)",
                    "Sellers collect premium but face potentially unlimited risk (naked calls)",
                    "Time decay (theta) works against option buyers and benefits sellers",
                ],
                "calls_and_puts": {
                    "call_option": "Gives the buyer the right to BUY the underlying at the strike price. Profitable when the underlying price rises above the strike + premium paid. Bullish position.",
                    "put_option": "Gives the buyer the right to SELL the underlying at the strike price. Profitable when the underlying price falls below the strike - premium paid. Bearish position.",
                    "long_vs_short": "Buying (going long) an option costs premium and gives rights. Selling (going short/writing) an option collects premium and creates obligations.",
                },
                "value_components": {
                    "intrinsic_value": "The amount an option is in-the-money (ITM). Call intrinsic = max(0, stock price - strike). Put intrinsic = max(0, strike - stock price).",
                    "extrinsic_value": "Also called time value. The portion of premium above intrinsic value, driven by time to expiration, volatility, and interest rates. Decays to zero at expiration.",
                    "moneyness": {
                        "in_the_money": "Call: stock > strike. Put: stock < strike. Has intrinsic value.",
                        "at_the_money": "Stock price equals or near strike price.",
                        "out_of_the_money": "Call: stock < strike. Put: stock > strike. No intrinsic value.",
                    },
                },
                "the_greeks": {
                    "delta": "Rate of change of option price per $1 move in underlying. Calls: 0 to +1. Puts: 0 to -1. ATM options have ~0.50 delta.",
                    "gamma": "Rate of change of delta per $1 move in underlying. Highest for ATM options near expiration. Measures the acceleration of price change.",
                    "theta": "Rate of time decay per day. Negative for option buyers (losing value daily). Accelerates as expiration approaches.",
                    "vega": "Sensitivity to a 1% change in implied volatility. Higher for longer-dated options. Positive for long options, negative for short.",
                    "rho": "Sensitivity to interest rate changes. Generally the least significant Greek for most options traders.",
                },
                "basic_strategies": {
                    "covered_call": "Own 100 shares + sell 1 call. Generates income from premium. Caps upside at strike price. Reduces effective cost basis.",
                    "protective_put": "Own 100 shares + buy 1 put. Acts as portfolio insurance. Limits downside to strike - premium. Costs premium.",
                    "bull_call_spread": "Buy lower strike call + sell higher strike call. Reduces cost vs buying call alone. Caps maximum profit at spread width.",
                    "bear_put_spread": "Buy higher strike put + sell lower strike put. Cheaper than buying put alone. Limited profit and limited risk.",
                    "straddle": "Buy ATM call + ATM put (same strike, expiration). Profits from large moves in either direction. Requires significant price movement to overcome double premium cost.",
                },
                "example": "Stock at $100. Buy a $105 call for $3 premium. Break-even: $108 ($105 + $3). Max loss: $3 (premium). Unlimited upside above $108. At expiration, if stock is $115, profit = $115 - $105 - $3 = $7 per share ($700 per contract).",
                "common_mistakes": [
                    "Buying out-of-the-money options purely because they're cheap (low probability of profit)",
                    "Ignoring the impact of implied volatility on premium pricing",
                    "Holding options too close to expiration and suffering accelerated time decay",
                    "Selling naked calls without understanding the unlimited risk exposure",
                    "Not having an exit plan before entering a trade",
                ],
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
