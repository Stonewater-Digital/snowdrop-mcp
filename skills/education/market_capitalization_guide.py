"""Educational guide to market capitalization.

MCP Tool Name: market_capitalization_guide
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "market_capitalization_guide",
    "description": "Returns educational content on market capitalization: calculation, large/mid/small cap categories, and implications.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def market_capitalization_guide() -> dict[str, Any]:
    """Returns educational content on market capitalization."""
    try:
        return {
            "status": "ok",
            "data": {
                "definition": "Market capitalization (market cap) is the total market value of a company's outstanding shares of stock. It represents what the market believes the entire company is worth at a given moment.",
                "key_concepts": [
                    "Market cap = Share Price x Total Shares Outstanding",
                    "It reflects market perception of value, not book value or intrinsic value",
                    "Market cap changes whenever the stock price changes",
                    "It is the primary way to classify companies by size",
                ],
                "formula": "Market Capitalization = Current Share Price x Total Outstanding Shares",
                "categories": {
                    "mega_cap": {
                        "range": "$200 billion+",
                        "characteristics": "The largest companies in the world. Household names with global operations. Extremely liquid. Often market leaders.",
                        "examples_type": "Major tech, energy, financial conglomerates",
                        "risk_profile": "Lower volatility, more stable earnings, established competitive moats",
                    },
                    "large_cap": {
                        "range": "$10 billion - $200 billion",
                        "characteristics": "Well-established companies with proven track records. Dominant in their industries. Often pay dividends.",
                        "examples_type": "Major industry players, S&P 500 components",
                        "risk_profile": "Moderate volatility, reliable revenue streams, lower growth rates",
                    },
                    "mid_cap": {
                        "range": "$2 billion - $10 billion",
                        "characteristics": "Companies in the process of expanding. Higher growth potential than large caps. Balance of growth and stability.",
                        "examples_type": "Regional leaders, emerging national brands",
                        "risk_profile": "Moderate volatility, higher growth potential, less analyst coverage",
                    },
                    "small_cap": {
                        "range": "$300 million - $2 billion",
                        "characteristics": "Smaller companies with significant growth potential but higher risk. Less liquid. May be more niche or regional.",
                        "examples_type": "Emerging companies, niche market players",
                        "risk_profile": "Higher volatility, less liquidity, greater potential for both gains and losses",
                    },
                    "micro_cap": {
                        "range": "$50 million - $300 million",
                        "characteristics": "Very small companies. Highly speculative. Limited institutional ownership. Thin trading volume.",
                        "examples_type": "Startups, very early-stage public companies",
                        "risk_profile": "Very high volatility, liquidity risk, limited public information",
                    },
                },
                "implications": {
                    "for_investors": "Market cap helps determine appropriate allocation. Large caps for stability, small caps for growth. Index funds use market cap weighting (larger companies get more weight).",
                    "for_indices": "Most major indices are market-cap weighted. A company's weight in the S&P 500 is proportional to its market cap relative to the total market cap of all 500 companies.",
                    "for_valuation": "Market cap alone does not tell you if a stock is cheap or expensive. Use valuation ratios (P/E, P/B, EV/EBITDA) to assess whether the market cap is justified by fundamentals.",
                    "enterprise_value": "Enterprise Value (EV) = Market Cap + Total Debt - Cash. EV is often a better measure of total company value than market cap alone because it accounts for capital structure.",
                },
                "example": "A company with 500 million shares outstanding trading at $80 per share has a market cap of $40 billion (large cap). If the stock drops to $60, market cap falls to $30 billion. If the company issues 100 million new shares at $60, market cap becomes 600M x $60 = $36 billion.",
                "common_mistakes": [
                    "Assuming market cap equals the cost to acquire a company (acquisition cost includes premium, debt, and other factors)",
                    "Confusing share price with company size — a $500 stock can have a smaller market cap than a $10 stock",
                    "Ignoring that market cap categories shift over time as boundaries are not fixed",
                    "Over-allocating to mega-cap stocks and missing the diversification benefit of including smaller companies",
                    "Using market cap as a sole measure of value without considering debt, cash, and earnings",
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
