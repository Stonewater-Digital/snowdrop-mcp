"""Educational guide to investment diversification.

MCP Tool Name: diversification_guide
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "diversification_guide",
    "description": "Returns educational content on diversification: asset classes, correlation, rebalancing, and international diversification.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def diversification_guide() -> dict[str, Any]:
    """Returns educational content on investment diversification."""
    try:
        return {
            "status": "ok",
            "data": {
                "definition": "Diversification is the investment strategy of spreading capital across different asset classes, sectors, geographies, and securities to reduce the overall risk of a portfolio. By holding assets that do not move in perfect lockstep, the poor performance of one investment can be offset by better performance of another.",
                "key_concepts": [
                    "Diversification is the only 'free lunch' in finance — reduces risk without necessarily reducing expected return",
                    "It reduces unsystematic (company-specific) risk but cannot eliminate systematic (market) risk",
                    "The key is low correlation between holdings, not simply owning many things",
                    "Over-diversification (diworsification) can dilute returns without meaningfully reducing risk",
                ],
                "asset_classes": {
                    "equities": "Stocks provide growth potential. Subcategorize by size (large/mid/small cap), style (growth/value), and geography.",
                    "fixed_income": "Bonds provide income and stability. Subcategorize by type (government/corporate/municipal), duration, and credit quality.",
                    "real_estate": "Property and REITs provide income and inflation protection. Low correlation with stocks and bonds.",
                    "commodities": "Gold, oil, agricultural products. Inflation hedge with low equity correlation. No income generation.",
                    "cash_equivalents": "Money market funds, T-Bills, CDs. Provide safety and liquidity. Lowest expected return.",
                    "alternatives": "Private equity, hedge funds, infrastructure, venture capital. Potentially higher returns with less liquidity and higher fees.",
                },
                "correlation": {
                    "definition": "A statistical measure (-1 to +1) of how two assets move relative to each other.",
                    "positive_correlation": "+1 means assets move in the same direction. Same asset class members tend to be positively correlated. Provides less diversification benefit.",
                    "zero_correlation": "0 means no relationship. Assets move independently. Good diversification benefit.",
                    "negative_correlation": "-1 means assets move in opposite directions. Maximum diversification benefit. Rare in practice.",
                    "important_pairs": {
                        "stocks_and_bonds": "Historically low to negative correlation (0.0 to -0.3), though this varies by economic regime. Both can decline during stagflation.",
                        "us_and_international_stocks": "Moderate positive correlation (0.5-0.8). Still provides some diversification but less than stock-bond combinations.",
                        "stocks_and_gold": "Low correlation (0.0 to 0.1). Gold serves as a crisis hedge.",
                        "stocks_and_real_estate": "Moderate correlation (0.3-0.6). REITs are somewhat equity-like but provide diversification.",
                    },
                },
                "rebalancing": {
                    "why": "Market movements cause portfolio weights to drift from targets. Rebalancing maintains the intended risk profile and enforces a disciplined buy-low-sell-high approach.",
                    "calendar_method": "Rebalance on a fixed schedule (quarterly, semi-annually, annually). Simple to implement. Annual or semi-annual is sufficient for most investors.",
                    "threshold_method": "Rebalance when any asset class drifts more than 5% from its target weight. More responsive but requires monitoring.",
                    "tax_smart": "Rebalance within tax-advantaged accounts (IRA, 401k) first to avoid triggering capital gains. Use new contributions to realign weights.",
                },
                "international_diversification": {
                    "rationale": "U.S. stocks represent ~60% of global market cap. International exposure captures the remaining 40% and reduces country-specific risk.",
                    "developed_markets": "Japan, UK, Germany, France, Australia, Canada. Stable economies, strong institutions, moderate growth.",
                    "emerging_markets": "China, India, Brazil, Taiwan, South Korea. Higher growth potential with higher volatility and political risk.",
                    "currency_risk": "International investments introduce currency exposure. A falling dollar benefits international holdings; a rising dollar hurts them. Can be hedged.",
                    "home_bias": "Investors tend to over-allocate to their home country. A reasonable international allocation is 20-40% of equity holdings.",
                },
                "example": "A portfolio of 60% U.S. stocks, 20% international stocks, and 20% bonds. In a year where U.S. stocks fall 15%, international stocks might fall only 5% and bonds might gain 5%. The diversified portfolio drops about 7% vs 15% for a U.S.-only stock portfolio.",
                "common_mistakes": [
                    "Assuming you are diversified because you own many stocks (if they are all in one sector, correlation is high)",
                    "Ignoring that correlations increase during crises — when diversification is needed most, it works least well",
                    "Over-diversifying with too many funds that overlap significantly (5 different large-cap funds is not diversification)",
                    "Neglecting to rebalance, allowing winners to become an oversized portfolio position",
                    "Avoiding international investments entirely due to home bias",
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
