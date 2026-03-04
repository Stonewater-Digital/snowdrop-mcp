"""Educational guide to mutual fund fundamentals.

MCP Tool Name: mutual_fund_guide
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "mutual_fund_guide",
    "description": "Returns educational content on mutual funds: types, expense ratios, load vs no-load, NAV calculation.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def mutual_fund_guide() -> dict[str, Any]:
    """Returns educational content on mutual fund fundamentals."""
    try:
        return {
            "status": "ok",
            "data": {
                "definition": "A mutual fund is a pooled investment vehicle managed by a professional fund manager that collects capital from many investors to purchase a diversified portfolio of stocks, bonds, or other securities. Investors own shares of the fund, not the underlying securities directly.",
                "key_concepts": [
                    "Mutual funds offer instant diversification and professional management",
                    "Shares are bought and sold at the end-of-day Net Asset Value (NAV)",
                    "Expense ratios directly reduce investor returns every year",
                    "Past performance does not guarantee future results",
                ],
                "types": {
                    "equity_funds": "Invest primarily in stocks. Subcategories: large-cap, mid-cap, small-cap, growth, value, blend, sector, international.",
                    "bond_funds": "Invest in fixed-income securities. Subcategories: government, corporate, municipal, high-yield, short/intermediate/long-term.",
                    "money_market_funds": "Invest in short-term, high-quality debt. Very low risk. Returns track short-term interest rates. Often used as cash equivalents.",
                    "balanced_funds": "Hold a mix of stocks and bonds (e.g., 60/40). Also called hybrid funds. Provide diversification in a single fund.",
                    "index_funds": "Passively track a market index (S&P 500, total market). Lowest expense ratios. No active management decisions.",
                    "target_date_funds": "Automatically adjust asset allocation to become more conservative as the target retirement date approaches. Glide path from stocks toward bonds.",
                },
                "expense_ratios": {
                    "definition": "The annual fee charged as a percentage of assets under management to cover operating costs, management fees, and administrative expenses.",
                    "typical_ranges": {
                        "index_funds": "0.03% - 0.20%",
                        "actively_managed": "0.50% - 1.50%",
                        "specialty_funds": "1.00% - 2.50%",
                    },
                    "impact": "A 1% expense ratio on a $100,000 investment costs $1,000/year. Over 30 years at 7% return, the difference between 0.10% and 1.00% expense ratios is over $100,000 in lost wealth.",
                },
                "load_vs_no_load": {
                    "front_end_load": "Sales charge paid when purchasing shares (Class A). Typically 3-6% of the investment. Reduces the amount actually invested.",
                    "back_end_load": "Sales charge paid when selling shares (Class B). Often decreases over time (contingent deferred sales charge). May convert to Class A after several years.",
                    "no_load": "No sales charge on purchase or redemption. Investors can buy directly from the fund company. Generally recommended for cost-conscious investors.",
                    "level_load": "Annual charge (Class C). Typically 1% per year. No front-end or back-end load but higher ongoing expenses.",
                },
                "nav_calculation": {
                    "formula": "NAV = (Total Assets - Total Liabilities) / Total Outstanding Shares",
                    "timing": "Calculated once per day at market close (4:00 PM ET). All buy and sell orders are executed at this price.",
                    "example": "Fund with $500 million in assets, $5 million in liabilities, and 20 million shares: NAV = ($500M - $5M) / 20M = $24.75 per share.",
                },
                "example": "An investor puts $10,000 into a no-load S&P 500 index fund with a 0.04% expense ratio. Annual cost: $4. The same $10,000 in an actively managed fund with a 5% front-end load starts at only $9,500 invested, with a 1.2% annual expense ratio costing $114/year.",
                "common_mistakes": [
                    "Chasing past performance — most top-performing funds fail to repeat",
                    "Ignoring expense ratios — seemingly small differences compound significantly over time",
                    "Paying sales loads when comparable no-load alternatives exist",
                    "Owning too many overlapping funds, creating hidden concentration",
                    "Not considering the tax implications of fund distributions in taxable accounts",
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
