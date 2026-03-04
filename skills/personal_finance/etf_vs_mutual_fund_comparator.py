"""
Executive Smary: Compares ETF and mutual fund holding costs including taxes and commissions.
Inputs: investment_amount (float), etf_expense_ratio (float), mf_expense_ratio (float), etf_commission (float), trading_frequency (int), tax_bracket (float), turnover_rates (dict)
Outputs: annual_cost_etf (float), annual_cost_mf (float), 10yr_cost_comparison (dict), tax_efficiency_advantage (float)
MCP Tool Name: etf_vs_mutual_fund_comparator
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "etf_vs_mutual_fund_comparator",
    "description": (
        "Aggregates expense ratios, commissions, and tax drag to compare ETF and mutual "
        "fund costs annually and across a 10-year horizon."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "investment_amount": {
                "type": "number",
                "description": "Capital invested in dollars.",
            },
            "etf_expense_ratio": {
                "type": "number",
                "description": "ETF annual expense ratio as decimal.",
            },
            "mf_expense_ratio": {
                "type": "number",
                "description": "Mutual fund expense ratio as decimal.",
            },
            "etf_commission": {
                "type": "number",
                "description": "Commission per ETF trade in dollars.",
            },
            "trading_frequency": {
                "type": "number",
                "description": "Number of ETF trades per year.",
            },
            "tax_bracket": {
                "type": "number",
                "description": "Marginal capital gains tax rate for distributions.",
            },
            "turnover_rates": {
                "type": "object",
                "description": "Dictionary with 'etf' and 'mf' turnover assumptions (0-1).",
            },
        },
        "required": [
            "investment_amount",
            "etf_expense_ratio",
            "mf_expense_ratio",
            "etf_commission",
            "trading_frequency",
            "tax_bracket",
            "turnover_rates",
        ],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"},
        },
        "required": ["status", "timestamp"],
    },
}


def etf_vs_mutual_fund_comparator(**kwargs: Any) -> dict:
    """Compare ETF vs mutual fund ongoing costs."""
    try:
        investment_amount = float(kwargs["investment_amount"])
        etf_expense_ratio = float(kwargs["etf_expense_ratio"])
        mf_expense_ratio = float(kwargs["mf_expense_ratio"])
        etf_commission = float(kwargs["etf_commission"])
        trading_frequency = int(kwargs["trading_frequency"])
        tax_bracket = float(kwargs["tax_bracket"])
        turnover_rates: Dict[str, Any] = kwargs["turnover_rates"]

        if investment_amount <= 0 or trading_frequency < 0:
            raise ValueError("Investment amount must be positive and trading frequency non-negative")
        if not isinstance(turnover_rates, dict):
            raise ValueError("turnover_rates must be a dict with etf/mf keys")

        etf_turnover = float(turnover_rates.get("etf", 0.1))
        mf_turnover = float(turnover_rates.get("mf", 0.6))
        etf_tax_drag = investment_amount * etf_turnover * tax_bracket * 0.5
        mf_tax_drag = investment_amount * mf_turnover * tax_bracket * 0.5

        annual_cost_etf = (
            investment_amount * etf_expense_ratio + etf_commission * trading_frequency + etf_tax_drag
        )
        annual_cost_mf = investment_amount * mf_expense_ratio + mf_tax_drag
        ten_year_etf = annual_cost_etf * 10
        ten_year_mf = annual_cost_mf * 10
        tax_efficiency_advantage = mf_tax_drag - etf_tax_drag

        return {
            "status": "success",
            "data": {
                "annual_cost_etf": annual_cost_etf,
                "annual_cost_mf": annual_cost_mf,
                "10yr_cost_comparison": {"etf": ten_year_etf, "mutual_fund": ten_year_mf},
                "tax_efficiency_advantage": tax_efficiency_advantage,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"etf_vs_mutual_fund_comparator failed: {e}")
        _log_lesson(f"etf_vs_mutual_fund_comparator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
