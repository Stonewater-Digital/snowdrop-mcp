"""Educational guide to stock valuation methods and when to use each.

MCP Tool Name: stock_valuation_guide
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "stock_valuation_guide",
    "description": "Returns educational content on stock valuation methods: DCF, P/E, P/B, DDM with usage guidance and limitations.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def stock_valuation_guide() -> dict[str, Any]:
    """Returns educational content on stock valuation methods."""
    try:
        return {
            "status": "ok",
            "data": {
                "definition": "Stock valuation is the process of determining the intrinsic value of a company's shares using fundamental analysis, comparing that value to the market price to identify undervalued or overvalued stocks.",
                "key_concepts": [
                    "Intrinsic value is an estimate, not a precise number",
                    "No single valuation method is definitive — use multiple approaches",
                    "Valuation is relative to industry peers and market conditions",
                    "Growth expectations are the biggest driver of valuation differences",
                ],
                "methods": {
                    "dcf": {
                        "name": "Discounted Cash Flow",
                        "formula": "Intrinsic Value = Sum of [FCF_t / (1 + WACC)^t] + Terminal Value / (1 + WACC)^n",
                        "when_to_use": "Best for mature companies with predictable free cash flows. Ideal when you have confidence in revenue and margin forecasts.",
                        "limitations": [
                            "Highly sensitive to discount rate and growth assumptions",
                            "Terminal value often dominates the calculation (60-80% of total value)",
                            "Difficult to apply to early-stage or unprofitable companies",
                            "Requires detailed financial projections",
                        ],
                    },
                    "pe_ratio": {
                        "name": "Price-to-Earnings Ratio",
                        "formula": "P/E = Market Price per Share / Earnings per Share",
                        "when_to_use": "Quick relative valuation comparing companies in the same sector. Use trailing P/E for current earnings and forward P/E for expected earnings.",
                        "limitations": [
                            "Earnings can be manipulated through accounting choices",
                            "Not useful for companies with negative earnings",
                            "Does not account for debt levels or capital structure",
                            "Varies significantly across industries and growth stages",
                        ],
                    },
                    "pb_ratio": {
                        "name": "Price-to-Book Ratio",
                        "formula": "P/B = Market Price per Share / Book Value per Share",
                        "when_to_use": "Best for asset-heavy companies like banks, insurance, and real estate. Useful for identifying deep value opportunities when P/B < 1.",
                        "limitations": [
                            "Book value may not reflect true asset values (historical cost accounting)",
                            "Less meaningful for asset-light businesses (tech, services)",
                            "Intangible assets often understated on balance sheet",
                            "Can be distorted by share buybacks",
                        ],
                    },
                    "ddm": {
                        "name": "Dividend Discount Model",
                        "formula": "Intrinsic Value = D1 / (r - g), where D1 = next year's dividend, r = required rate of return, g = constant growth rate",
                        "when_to_use": "Best for stable, dividend-paying companies with predictable payout growth (utilities, REITs, blue chips). Uses the Gordon Growth Model for constant growth.",
                        "limitations": [
                            "Only works for dividend-paying companies",
                            "Assumes constant growth rate in perpetuity",
                            "Very sensitive to the spread between r and g",
                            "Does not capture value from retained earnings or buybacks",
                        ],
                    },
                },
                "example": "A company with $5 EPS trading at $100 has a P/E of 20x. If the sector average is 15x, it may be overvalued unless its growth rate justifies the premium. A DCF model projecting $8 FCF growing at 5% with a 10% WACC would give a different intrinsic value to compare against.",
                "common_mistakes": [
                    "Relying on a single valuation method instead of triangulating with multiple approaches",
                    "Using trailing metrics for cyclical companies at peak earnings",
                    "Ignoring the quality and sustainability of earnings",
                    "Comparing P/E ratios across different industries without adjustment",
                    "Assuming the market price is always wrong when your model disagrees",
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
