"""Educational guide to dividends and dividend investing.

MCP Tool Name: dividend_guide
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "dividend_guide",
    "description": "Returns educational content on dividends: types, key dates, yield, payout ratio, and DRIP.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def dividend_guide() -> dict[str, Any]:
    """Returns educational content on dividends and dividend investing."""
    try:
        return {
            "status": "ok",
            "data": {
                "definition": "A dividend is a distribution of a portion of a company's earnings to its shareholders, decided by the board of directors. Dividends reward shareholders for owning the stock and represent a return of profits to the owners of the business.",
                "key_concepts": [
                    "Dividends are not guaranteed — the board can reduce or eliminate them at any time",
                    "Dividend-paying stocks tend to be mature, profitable companies with stable cash flows",
                    "Dividend income can be qualified (taxed at capital gains rates) or ordinary (taxed at income rates)",
                    "Total return = Price appreciation + Dividend income",
                ],
                "types": {
                    "cash_dividends": "The most common type. Regular cash payments to shareholders, usually quarterly in the U.S.",
                    "stock_dividends": "Additional shares given to shareholders instead of cash. Increases share count but does not change total ownership percentage.",
                    "special_dividends": "One-time cash payments, often after exceptional profits, asset sales, or accumulation of excess cash. Not recurring.",
                    "preferred_dividends": "Fixed dividend payments to preferred shareholders. Paid before common dividends. More similar to bond coupon payments.",
                },
                "key_dates": {
                    "declaration_date": "The date the board of directors announces the dividend amount, record date, and payment date.",
                    "ex_dividend_date": "The first day the stock trades without the dividend. Buyers on or after this date do NOT receive the upcoming dividend. The stock price typically drops by approximately the dividend amount on this date.",
                    "record_date": "The date the company reviews its records to determine eligible shareholders. Usually one business day after the ex-dividend date.",
                    "payment_date": "The date the dividend is actually paid to eligible shareholders. Typically 2-4 weeks after the record date.",
                },
                "dividend_yield": {
                    "formula": "Dividend Yield = Annual Dividend per Share / Current Stock Price * 100",
                    "example": "A stock paying $4.00 annual dividend at $100/share has a 4.0% yield. If the price drops to $80, the yield rises to 5.0% (assuming the dividend is maintained).",
                    "yield_trap": "Very high yields (>6-8%) often signal that the market expects a dividend cut. The stock price may have fallen sharply, inflating the yield artificially.",
                    "typical_ranges": "S&P 500 average: ~1.5-2.0%. Utilities: 3-5%. REITs: 3-6%. Growth stocks: 0-1%.",
                },
                "payout_ratio": {
                    "formula": "Payout Ratio = Dividends per Share / Earnings per Share * 100",
                    "interpretation": "Shows what percentage of earnings is distributed as dividends. Lower ratio = more earnings retained for growth and safety cushion.",
                    "healthy_range": "30-60% is typical for most companies. Utilities may be 60-80%. REITs are required to distribute 90%+ of taxable income.",
                    "sustainability": "Payout ratios consistently above 100% mean the company is paying more than it earns — unsustainable without borrowing or drawing down cash.",
                },
                "drip": {
                    "definition": "Dividend Reinvestment Plan (DRIP). Automatically reinvests dividends to purchase additional shares (or fractional shares) instead of receiving cash.",
                    "benefits": [
                        "Compounds returns by putting dividends to work immediately",
                        "Often commission-free",
                        "Dollar-cost averaging effect",
                        "Some companies offer DRIP shares at a discount (1-5%)",
                    ],
                    "tax_note": "Reinvested dividends are still taxable in the year received, even though no cash is taken. Tax-advantaged accounts (IRA, 401k) avoid this issue.",
                },
                "example": "An investor owns 1,000 shares of a stock paying $1.00 quarterly dividend ($4.00 annual). Quarterly income: $1,000. Annual income: $4,000. With DRIP at $50/share, each quarterly dividend buys 20 additional shares, growing the position and future dividend income automatically.",
                "common_mistakes": [
                    "Chasing high dividend yields without investigating sustainability (yield traps)",
                    "Ignoring dividend growth rate — a 2% yield growing at 10%/year beats a static 4% yield over time",
                    "Forgetting that dividends are taxed in taxable accounts, reducing the net benefit",
                    "Assuming dividends are risk-free — they can be cut during financial stress",
                    "Concentrating too heavily in dividend stocks and missing growth opportunities",
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
