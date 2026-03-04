"""Educational guide to dollar-cost averaging investment strategy.

MCP Tool Name: dollar_cost_averaging_guide
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "dollar_cost_averaging_guide",
    "description": "Returns educational content on dollar-cost averaging: strategy, advantages, comparison to lump sum, and examples.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def dollar_cost_averaging_guide() -> dict[str, Any]:
    """Returns educational content on dollar-cost averaging."""
    try:
        return {
            "status": "ok",
            "data": {
                "definition": "Dollar-cost averaging (DCA) is an investment strategy where a fixed dollar amount is invested at regular intervals (weekly, monthly, quarterly) regardless of the asset's price. By investing consistently, you automatically buy more shares when prices are low and fewer shares when prices are high, reducing the impact of volatility on the average cost per share.",
                "key_concepts": [
                    "DCA removes the need to time the market — you invest mechanically on a schedule",
                    "It reduces the risk of investing a large sum at a market peak",
                    "DCA is the strategy behind 401(k) contributions — automatic payroll deductions",
                    "Mathematically, lump sum beats DCA about 2/3 of the time, but DCA reduces regret risk",
                ],
                "strategy": {
                    "how_it_works": "Choose a fixed dollar amount and a regular interval. Invest that amount regardless of market conditions. Continue for the long term.",
                    "step_1": "Determine the total amount to invest and the investment timeframe.",
                    "step_2": "Divide the total into equal periodic investments (e.g., $500/month for 24 months).",
                    "step_3": "Invest on schedule without trying to predict market direction.",
                    "step_4": "Continue through market ups and downs — discipline is key.",
                },
                "advantages": [
                    "Eliminates the pressure of market timing — no need to decide the 'right' time to invest",
                    "Reduces the emotional impact of investing — automated and systematic",
                    "Averages out the purchase price over time, smoothing volatility effects",
                    "Builds disciplined saving and investing habits",
                    "Reduces the risk of investing all capital at a market top",
                    "Works well with regular income (paycheck-to-paycheck investing)",
                ],
                "dca_vs_lump_sum": {
                    "lump_sum_advantage": "Historically, investing the full amount immediately produces higher returns about 67% of the time because markets tend to rise over time. Every day not invested is a day of missed potential returns.",
                    "dca_advantage": "DCA wins the other 33% — particularly when markets decline after the investment would have been made. DCA also reduces maximum drawdown and regret risk.",
                    "behavioral_benefit": "Many investors with a lump sum hesitate and never invest at all. DCA provides a comfortable entry path that overcomes analysis paralysis.",
                    "recommendation": "If you can stomach volatility, lump sum investing is mathematically optimal. If the risk of a large immediate loss would cause you to panic-sell, DCA is behaviorally optimal.",
                },
                "example": {
                    "scenario": "An investor puts $1,000/month into an index fund over 6 months.",
                    "months": [
                        {"month": 1, "price": 50.00, "shares_bought": 20.00},
                        {"month": 2, "price": 40.00, "shares_bought": 25.00},
                        {"month": 3, "price": 30.00, "shares_bought": 33.33},
                        {"month": 4, "price": 35.00, "shares_bought": 28.57},
                        {"month": 5, "price": 45.00, "shares_bought": 22.22},
                        {"month": 6, "price": 50.00, "shares_bought": 20.00},
                    ],
                    "total_invested": 6000,
                    "total_shares": 149.12,
                    "average_cost_per_share": 40.24,
                    "average_market_price": 41.67,
                    "result": "The average cost per share ($40.24) is lower than the simple average price ($41.67) because more shares were purchased at lower prices. At $50/share, holdings are worth $7,456 on a $6,000 investment.",
                },
                "common_mistakes": [
                    "Stopping contributions during market downturns (this is exactly when DCA benefits you most)",
                    "Using DCA as an excuse to delay investing money you could invest now",
                    "Applying DCA to regular income that arrives periodically anyway (just invest each paycheck)",
                    "Not having a long enough time horizon — DCA needs time to smooth out volatility",
                    "Ignoring transaction costs if making frequent small purchases (less relevant with commission-free brokers)",
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
