"""Educational guide to Exchange-Traded Funds (ETFs).

MCP Tool Name: etf_guide
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "etf_guide",
    "description": "Returns educational content on ETFs: vs mutual funds, creation/redemption, tracking error, and types.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def etf_guide() -> dict[str, Any]:
    """Returns educational content on Exchange-Traded Funds."""
    try:
        return {
            "status": "ok",
            "data": {
                "definition": "An Exchange-Traded Fund (ETF) is a type of investment fund that holds a basket of securities (stocks, bonds, commodities, etc.) and trades on a stock exchange like an individual stock. ETFs combine the diversification of mutual funds with the trading flexibility of stocks.",
                "key_concepts": [
                    "ETFs trade throughout the day at market prices, unlike mutual funds which trade at end-of-day NAV",
                    "The creation/redemption mechanism keeps ETF prices close to their net asset value",
                    "Most ETFs are passively managed, tracking an index, but actively managed ETFs are growing",
                    "ETFs are generally more tax-efficient than mutual funds due to in-kind redemptions",
                ],
                "etf_vs_mutual_fund": {
                    "trading": "ETFs trade intraday on exchanges; mutual funds trade once daily at NAV.",
                    "pricing": "ETFs have real-time market prices with bid-ask spreads; mutual funds use end-of-day NAV.",
                    "minimum_investment": "ETFs: price of one share (fractional shares available). Mutual funds: often $500-$3,000 minimum.",
                    "expense_ratios": "ETFs generally lower (0.03-0.50%). Mutual funds: 0.10-1.50%+.",
                    "tax_efficiency": "ETFs are more tax-efficient due to in-kind creation/redemption. Mutual funds may distribute capital gains annually.",
                    "dividend_reinvestment": "Mutual funds offer automatic reinvestment. ETF DRIP depends on broker support.",
                },
                "creation_redemption": {
                    "authorized_participants": "Large institutional investors (typically market makers or large broker-dealers) who can create or redeem ETF shares directly with the fund.",
                    "creation": "An AP delivers a basket of underlying securities to the ETF issuer and receives newly created ETF shares in return. This increases total shares outstanding.",
                    "redemption": "An AP returns ETF shares to the issuer and receives the underlying basket of securities. This decreases total shares outstanding.",
                    "arbitrage_mechanism": "If the ETF trades at a premium to NAV, APs create new shares (selling the ETF, buying underlying). If at a discount, APs redeem shares (buying ETF, selling underlying). This keeps prices aligned.",
                },
                "tracking_error": {
                    "definition": "The difference between an ETF's performance and its benchmark index performance over time.",
                    "causes": [
                        "Expense ratio dragging returns below the index",
                        "Sampling — holding a representative subset rather than all index constituents",
                        "Cash drag from uninvested dividends or new creations",
                        "Rebalancing timing differences",
                    ],
                    "acceptable_range": "Index ETFs typically have tracking error of 0.01-0.20% annually. Higher tracking error may indicate management issues.",
                },
                "types": {
                    "index_etfs": "Track market indices (S&P 500, Nasdaq 100, Total Stock Market). Lowest cost and most popular.",
                    "sector_etfs": "Focus on specific sectors (technology, healthcare, financials, energy).",
                    "bond_etfs": "Hold fixed-income securities (government, corporate, municipal, high-yield).",
                    "commodity_etfs": "Track commodity prices (gold, silver, oil) through physical holdings or futures.",
                    "international_etfs": "Provide exposure to foreign markets (developed, emerging, single-country).",
                    "thematic_etfs": "Target investment themes (clean energy, AI, cybersecurity, cannabis).",
                    "leveraged_and_inverse": "Use derivatives to provide 2x/3x or inverse returns of an index. Designed for short-term trading only — compounding causes drift from expected returns over longer periods.",
                    "actively_managed": "Portfolio managers make active investment decisions. Higher expense ratios than index ETFs but potentially better returns.",
                },
                "example": "An investor buying SPY (S&P 500 ETF) at $450/share owns a proportional slice of all 500 companies. With a 0.09% expense ratio, the annual cost on $10,000 invested is $9. The shares can be bought or sold any time during market hours.",
                "common_mistakes": [
                    "Trading ETFs with low volume and wide bid-ask spreads, increasing transaction costs",
                    "Using leveraged/inverse ETFs for long-term holding (they are designed for daily rebalancing)",
                    "Ignoring tracking error when comparing similar ETFs tracking the same index",
                    "Over-trading ETFs just because you can — transaction frequency does not improve returns",
                    "Not considering the total cost of ownership (expense ratio + spread + commissions)",
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
