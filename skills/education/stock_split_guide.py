"""Educational guide to stock splits.

MCP Tool Name: stock_split_guide
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "stock_split_guide",
    "description": "Returns educational content on stock splits: forward/reverse splits, reasons, and effects on value.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def stock_split_guide() -> dict[str, Any]:
    """Returns educational content on stock splits."""
    try:
        return {
            "status": "ok",
            "data": {
                "definition": "A stock split is a corporate action that increases (forward split) or decreases (reverse split) the number of a company's outstanding shares while proportionally adjusting the share price. The total market capitalization remains unchanged immediately after the split.",
                "key_concepts": [
                    "Stock splits do not change the total value of an investor's holdings",
                    "Forward splits make shares more affordable; reverse splits increase share price",
                    "Splits affect share count, price per share, and per-share metrics (EPS, DPS) proportionally",
                    "Market cap = shares outstanding x price per share — unchanged by the split itself",
                ],
                "forward_splits": {
                    "definition": "Increases the number of shares while proportionally reducing the price per share.",
                    "common_ratios": {
                        "2_for_1": "Each share becomes 2 shares at half the price. 100 shares at $200 becomes 200 shares at $100.",
                        "3_for_1": "Each share becomes 3 shares at one-third the price. 100 shares at $300 becomes 300 shares at $100.",
                        "4_for_1": "Each share becomes 4 shares at one-quarter the price. 100 shares at $400 becomes 400 shares at $100.",
                        "10_for_1": "Each share becomes 10 shares at one-tenth the price. Used for very high-priced stocks.",
                    },
                    "why_companies_split": [
                        "Make shares more affordable for retail investors (lower price per share)",
                        "Increase trading liquidity by having more shares at a lower price",
                        "Signal confidence — companies split after significant price appreciation",
                        "Qualify for price-weighted indices (like the Dow Jones, which favors moderate prices)",
                        "Psychological effect — investors may perceive lower-priced shares as having more room to grow",
                    ],
                },
                "reverse_splits": {
                    "definition": "Reduces the number of shares while proportionally increasing the price per share.",
                    "common_ratios": {
                        "1_for_5": "Every 5 shares becomes 1 share at 5x the price. 500 shares at $2 becomes 100 shares at $10.",
                        "1_for_10": "Every 10 shares becomes 1 share at 10x the price. 1,000 shares at $1 becomes 100 shares at $10.",
                    },
                    "why_companies_reverse_split": [
                        "Avoid delisting from exchanges that require minimum share prices (e.g., $1 on Nasdaq)",
                        "Attract institutional investors who may have minimum price policies",
                        "Improve perceived legitimacy (penny stock stigma)",
                        "Reduce the number of shares outstanding for administrative efficiency",
                    ],
                    "warning_sign": "Reverse splits are often a negative signal. Companies that reverse split are frequently struggling financially and trying to maintain exchange listing requirements.",
                },
                "effect_on_value": {
                    "market_cap": "Unchanged. If 1M shares at $100 ($100M market cap) splits 2-for-1, result is 2M shares at $50 ($100M market cap).",
                    "percentage_ownership": "Unchanged. All shareholders maintain the same proportional ownership.",
                    "dividends": "Per-share dividend is adjusted proportionally. Total dividend income is unchanged. A $2/share dividend becomes $1/share after a 2-for-1 split.",
                    "options": "Strike prices and contract multipliers are adjusted. A call with $100 strike becomes two calls with $50 strike after a 2-for-1 split.",
                    "historical_prices": "Financial data providers adjust historical prices to reflect splits, so charts show consistent returns.",
                },
                "example": "Company XYZ stock has risen from $50 to $500 over several years. The board announces a 5-for-1 split. An investor holding 200 shares at $500 ($100,000 value) will have 1,000 shares at $100 ($100,000 value) after the split. Nothing changes in value — only the number of shares and price per share adjust.",
                "common_mistakes": [
                    "Believing a stock split creates value (it does not — it is purely cosmetic)",
                    "Buying a stock just because it is splitting (the split itself has no impact on fundamentals)",
                    "Interpreting a reverse split as neutral (it is usually a negative signal about the company)",
                    "Forgetting to adjust per-share metrics (EPS, DPS) when comparing pre-split and post-split data",
                    "Confusing stock splits with stock dividends (similar mechanics but different accounting treatment)",
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
