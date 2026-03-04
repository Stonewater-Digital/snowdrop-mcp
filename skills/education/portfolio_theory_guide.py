"""Educational guide to Modern Portfolio Theory and asset allocation.

MCP Tool Name: portfolio_theory_guide
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "portfolio_theory_guide",
    "description": "Returns educational content on Modern Portfolio Theory: efficient frontier, diversification, and asset allocation.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def portfolio_theory_guide() -> dict[str, Any]:
    """Returns educational content on Modern Portfolio Theory."""
    try:
        return {
            "status": "ok",
            "data": {
                "definition": "Modern Portfolio Theory (MPT), introduced by Harry Markowitz in 1952, is a mathematical framework for constructing portfolios that maximize expected return for a given level of risk, based on the principle that diversification can reduce portfolio risk without sacrificing returns.",
                "key_concepts": [
                    "Investors are risk-averse — they prefer less risk for the same return",
                    "Portfolio risk depends on individual asset risk AND the correlations between assets",
                    "Diversification reduces unsystematic risk but cannot eliminate systematic (market) risk",
                    "The optimal portfolio lies on the efficient frontier",
                ],
                "formula": "Portfolio Variance = w1^2*sigma1^2 + w2^2*sigma2^2 + 2*w1*w2*sigma1*sigma2*rho(1,2), where w = weight, sigma = std dev, rho = correlation",
                "efficient_frontier": {
                    "definition": "The set of portfolios that offer the highest expected return for each level of risk (standard deviation). Portfolios below the frontier are suboptimal.",
                    "tangency_portfolio": "The portfolio on the efficient frontier that, when combined with the risk-free asset, offers the highest Sharpe ratio (best risk-adjusted return).",
                    "capital_market_line": "The line from the risk-free rate tangent to the efficient frontier. All investors should hold a combination of the risk-free asset and the tangency portfolio.",
                },
                "diversification": {
                    "how_it_works": "Combining assets with low or negative correlations reduces portfolio volatility. When one asset falls, others may hold steady or rise, dampening overall swings.",
                    "systematic_vs_unsystematic": "Diversification eliminates unsystematic (company-specific) risk but cannot remove systematic (market-wide) risk. Approximately 20-30 stocks can eliminate most unsystematic risk.",
                    "correlation": "The key metric: +1 = perfect positive correlation (no diversification benefit), 0 = uncorrelated (good benefit), -1 = perfect negative correlation (maximum benefit).",
                    "diminishing_returns": "Most diversification benefit comes from the first 15-20 holdings. Beyond that, adding more positions has minimal risk reduction.",
                },
                "asset_allocation": {
                    "strategic": "Long-term target allocation based on goals, risk tolerance, and time horizon. Example: 60% stocks / 30% bonds / 10% alternatives.",
                    "tactical": "Short-term deviations from strategic allocation to capitalize on market opportunities. Requires skill in market timing.",
                    "age_based_rule": "Common rule of thumb: bond allocation = your age (e.g., 30-year-old holds 30% bonds, 70% stocks). Overly simplistic but directionally useful.",
                    "rebalancing": "Periodically returning to target weights. Can be calendar-based (quarterly/annually) or threshold-based (rebalance when allocation drifts 5%+ from target).",
                },
                "example": "A portfolio of 60% S&P 500 (expected return 10%, std dev 15%) and 40% bonds (expected return 4%, std dev 5%) with 0.2 correlation has a portfolio expected return of 7.6% but portfolio std dev of about 9.8% — lower than the weighted average of 11% due to diversification.",
                "common_mistakes": [
                    "Assuming past correlations will persist in future market conditions",
                    "Over-diversifying to the point of 'diworsification' — owning too many overlapping funds",
                    "Ignoring that correlations tend to increase during market crises (when diversification is needed most)",
                    "Using MPT without considering non-normal return distributions and fat tails",
                    "Neglecting to rebalance, allowing portfolio drift to change risk profile",
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
