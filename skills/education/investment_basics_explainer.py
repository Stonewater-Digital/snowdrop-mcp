"""Explain core investing concepts for goodwill."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

EXPLANATIONS = {
    "compound_interest": (
        "Compound interest",
        "Your money earns interest on both the original amount and the interest already earned.",
        "If you invest $1,000 at 8% annually, next year's interest is on $1,080, not just $1,000.",
        "Start early so time can do the heavy lifting.",
        ["diversification", "time_value_of_money"],
    ),
    "diversification": (
        "Diversification",
        "Spreading investments across assets reduces the impact of one loser.",
        "Holding stocks, bonds, and cash cushions the blow if one market dips.",
        "Don't let a single position decide your future.",
        ["asset_allocation", "risk_return"],
    ),
    "dollar_cost_averaging": (
        "Dollar-cost averaging",
        "Investing equal amounts at regular intervals to smooth out volatility.",
        "Buying $500 of an index fund each month buys more shares when prices drop.",
        "Consistency beats trying to time the market.",
        ["compound_interest", "risk_return"],
    ),
    "risk_return": (
        "Risk/return tradeoff",
        "Higher potential reward usually requires accepting more ups and downs.",
        "Stocks tend to return more than bonds because they can swing wildly.",
        "Match risk to your timeline and sleep level.",
        ["asset_allocation", "diversification"],
    ),
    "index_funds": (
        "Index funds",
        "Funds designed to track a market benchmark with low cost and automation.",
        "An S&P 500 index fund owns the same companies as the index.",
        "Fees matter: lower drag means more compounding.",
        ["etf_vs_mutual_fund", "diversification"],
    ),
    "bonds": (
        "Bonds",
        "Loans you make to governments or companies with scheduled interest payments.",
        "A 3-year Treasury pays semiannual coupons and returns principal at maturity.",
        "When rates rise, bond prices typically fall.",
        ["risk_return", "asset_allocation"],
    ),
    "etf_vs_mutual_fund": (
        "ETF vs mutual fund",
        "ETFs trade like stocks all day; mutual funds price once after market close.",
        "An ETF can be bought at 11am; a mutual fund order executes at 4pm.",
        "Focus on costs, tracking error, and liquidity.",
        ["index_funds", "diversification"],
    ),
    "inflation": (
        "Inflation",
        "Prices gradually rise, eroding purchasing power if cash sits idle.",
        "A basket of groceries costing $100 today might be $103 next year.",
        "Invest to outpace inflation over long horizons.",
        ["time_value_of_money", "risk_return"],
    ),
    "time_value_of_money": (
        "Time value of money",
        "Money today is worth more than the same amount tomorrow because it can grow.",
        "Receiving $1,000 now lets you invest immediately versus waiting a year.",
        "Discount future cash flows when comparing opportunities.",
        ["compound_interest", "inflation"],
    ),
    "asset_allocation": (
        "Asset allocation",
        "Mixing asset classes (stocks, bonds, cash) to target risk and return.",
        "A 70/30 stock/bond split may suit growth-focused investors.",
        "Revisit allocation as life goals shift.",
        ["diversification", "risk_return"],
    ),
}

TOOL_META: dict[str, Any] = {
    "name": "investment_basics_explainer",
    "description": "Returns plain-language explanations for foundational investing topics.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "concept": {"type": "string"},
        },
        "required": ["concept"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
    },
}


def investment_basics_explainer(concept: str, **_: Any) -> dict[str, Any]:
    """Return educational content for the requested investing concept."""
    try:
        if concept not in EXPLANATIONS:
            raise ValueError("Concept not available")
        title, explanation, example, takeaway, related = EXPLANATIONS[concept]
        data = {
            "concept": title,
            "explanation": explanation,
            "example": example,
            "key_takeaway": takeaway,
            "common_mistake": "Ignoring time horizon and risk tolerance.",
            "related_concepts": related,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("investment_basics_explainer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
