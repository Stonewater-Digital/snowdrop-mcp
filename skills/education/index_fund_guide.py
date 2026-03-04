"""Educational guide to index fund investing.

MCP Tool Name: index_fund_guide
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "index_fund_guide",
    "description": "Returns educational content on index funds: passive investing, major indices, advantages, and rebalancing.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def index_fund_guide() -> dict[str, Any]:
    """Returns educational content on index fund investing."""
    try:
        return {
            "status": "ok",
            "data": {
                "definition": "An index fund is a type of mutual fund or ETF designed to replicate the performance of a specific market index by holding the same securities in the same proportions as the index. Index funds follow a passive investment strategy, requiring minimal management decisions.",
                "key_concepts": [
                    "Index funds aim to match market returns, not beat them",
                    "Lower costs are the primary structural advantage of index investing",
                    "Over long periods, most actively managed funds underperform their benchmark index after fees",
                    "Pioneered by John Bogle and Vanguard with the first retail index fund in 1976",
                ],
                "passive_investing": {
                    "philosophy": "Rather than trying to pick winning stocks or time the market, passive investors accept market returns through broad diversification at minimal cost.",
                    "evidence": "S&P SPIVA scorecards consistently show that over 15-year periods, 85-95% of actively managed large-cap funds underperform the S&P 500 index.",
                    "efficient_market_hypothesis": "Markets are generally efficient — stock prices reflect available information, making it extremely difficult to consistently outperform through stock picking or market timing.",
                },
                "major_indices": {
                    "sp500": "S&P 500 — 500 large-cap U.S. companies representing ~80% of U.S. stock market value. Market-cap weighted. The most widely followed equity benchmark.",
                    "total_stock_market": "Covers the entire U.S. stock market (~4,000 stocks). Includes large, mid, small, and micro-cap. Examples: VTSAX, VTI.",
                    "nasdaq_100": "100 largest non-financial companies listed on the Nasdaq exchange. Technology-heavy. Examples: QQQ.",
                    "dow_jones": "Dow Jones Industrial Average — 30 large-cap U.S. blue-chip stocks. Price-weighted (unusual). More of a historical indicator than a practical benchmark.",
                    "russell_2000": "2,000 small-cap U.S. companies. The standard small-cap benchmark.",
                    "msci_eafe": "International developed markets index (Europe, Australasia, Far East). Excludes U.S. and Canada.",
                    "msci_emerging": "Emerging market stocks from 24 countries (China, India, Brazil, etc.).",
                    "bloomberg_agg": "Bloomberg U.S. Aggregate Bond Index — the standard U.S. bond market benchmark covering government, corporate, and mortgage-backed bonds.",
                },
                "advantages": [
                    "Extremely low expense ratios (0.03-0.20% vs 0.50-1.50% for active funds)",
                    "Broad diversification reduces single-stock risk",
                    "Tax-efficient — lower turnover means fewer capital gains distributions",
                    "Simplicity — no fund manager selection, style drift, or strategy changes",
                    "Consistent performance relative to the index (low tracking error)",
                    "Transparent — holdings are known (they mirror the index)",
                ],
                "rebalancing": {
                    "why": "Over time, asset allocation drifts as different assets produce different returns. Rebalancing returns the portfolio to target weights.",
                    "methods": {
                        "calendar_based": "Rebalance on a fixed schedule (quarterly, semi-annually, annually). Simple and disciplined.",
                        "threshold_based": "Rebalance when an allocation drifts more than a set amount (e.g., 5%) from target. More responsive but requires monitoring.",
                    },
                    "tax_considerations": "In taxable accounts, rebalancing may trigger capital gains taxes. Use tax-loss harvesting, new contributions, or rebalance within tax-advantaged accounts first.",
                },
                "example": "An investor builds a three-fund portfolio: 60% U.S. total stock market index (VTSAX, 0.04% ER), 25% international index (VTIAX, 0.12% ER), 15% U.S. bond index (VBTLX, 0.05% ER). Blended expense ratio: ~0.06%. Annual cost on $100,000: $60.",
                "common_mistakes": [
                    "Switching to active management during market downturns (abandoning the strategy at the worst time)",
                    "Holding overlapping index funds (e.g., S&P 500 fund + total market fund — the S&P 500 is ~80% of total market)",
                    "Ignoring international diversification by holding only U.S. index funds",
                    "Failing to rebalance and allowing the portfolio to drift far from target allocation",
                    "Comparing index fund returns to cherry-picked active fund returns (survivorship bias)",
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
