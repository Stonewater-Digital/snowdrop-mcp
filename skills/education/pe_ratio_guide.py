"""Educational guide to the Price-to-Earnings ratio.

MCP Tool Name: pe_ratio_guide
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "pe_ratio_guide",
    "description": "Returns educational content on P/E ratio: formula, forward vs trailing, sector averages, and PEG ratio.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def pe_ratio_guide() -> dict[str, Any]:
    """Returns educational content on the Price-to-Earnings ratio."""
    try:
        return {
            "status": "ok",
            "data": {
                "definition": "The Price-to-Earnings (P/E) ratio is one of the most widely used valuation metrics, measuring how much investors are willing to pay per dollar of a company's earnings. It indicates market expectations about a company's future growth and profitability.",
                "key_concepts": [
                    "P/E is a relative valuation metric — compare within industries, not across them",
                    "Higher P/E suggests investors expect higher future earnings growth",
                    "P/E is meaningless for companies with no earnings (use P/S or EV/Revenue instead)",
                    "Earnings quality matters — one-time items can distort the ratio",
                ],
                "formula": "P/E Ratio = Market Price per Share / Earnings per Share (EPS)",
                "trailing_vs_forward": {
                    "trailing_pe": "Uses actual earnings from the last 12 months (TTM). Based on historical data. Available for any company with positive earnings. Found on most financial data sites.",
                    "forward_pe": "Uses analyst consensus earnings estimates for the next 12 months. Forward-looking. Reflects expected growth. More useful for fast-growing companies but relies on estimates that may be wrong.",
                    "shiller_pe": "Cyclically Adjusted P/E (CAPE). Uses average inflation-adjusted earnings over the past 10 years. Smooths out business cycle effects. Used for market-level valuation assessment.",
                },
                "sector_averages": {
                    "technology": "25-40x (high growth expectations, scalable business models)",
                    "healthcare": "20-30x (innovation pipeline, regulatory moats)",
                    "financials": "10-15x (regulated industry, cyclical earnings)",
                    "utilities": "15-20x (stable but slow growth, high dividend yields)",
                    "consumer_staples": "20-25x (defensive, steady demand, premium for stability)",
                    "energy": "8-15x (cyclical, commodity-dependent, capital intensive)",
                    "industrials": "15-20x (cyclical, tied to economic growth)",
                    "real_estate": "30-50x (REITs — use Funds From Operations instead of EPS for better valuation)",
                    "note": "Averages shift over time with interest rates, growth expectations, and market conditions.",
                },
                "peg_ratio": {
                    "definition": "The PEG ratio adjusts the P/E for growth, providing a more complete picture. PEG = P/E / Annual EPS Growth Rate (%).",
                    "interpretation": {
                        "peg_below_1": "May indicate the stock is undervalued relative to its growth rate.",
                        "peg_equal_1": "Suggests the stock is fairly valued given its growth rate.",
                        "peg_above_1": "May indicate the stock is overvalued relative to its growth rate, or the market expects acceleration.",
                    },
                    "example": "Company A: P/E of 30, EPS growth of 25%. PEG = 30/25 = 1.2. Company B: P/E of 15, EPS growth of 5%. PEG = 15/5 = 3.0. Despite a lower P/E, Company B is more expensive relative to its growth.",
                    "limitations": "PEG assumes a linear relationship between P/E and growth. Does not work well for companies with negative or zero growth.",
                },
                "example": "Stock trading at $150/share with EPS of $6 has a trailing P/E of 25x. If the sector average is 20x, the stock may be overvalued unless it has above-average growth. If analysts estimate next year's EPS at $8, the forward P/E is 150/8 = 18.75x, suggesting the growth may justify the price.",
                "common_mistakes": [
                    "Comparing P/E ratios across different sectors (tech P/E of 30 is not equivalent to bank P/E of 30)",
                    "Using trailing P/E for high-growth companies where past earnings understate future potential",
                    "Ignoring earnings quality — one-time gains inflate EPS and deflate P/E artificially",
                    "Assuming a low P/E always means a stock is cheap (it may reflect fundamental problems)",
                    "Treating P/E as the only valuation metric — use it alongside P/B, EV/EBITDA, and DCF",
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
