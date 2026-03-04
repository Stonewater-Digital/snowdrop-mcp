"""
Executive Smary: Evaluates safe withdrawal amounts versus retirement spending needs.
Inputs: portfolio_balance (float), annual_expenses (float), inflation_rate (float), retirement_years (int)
Outputs: safe_withdrawal (float), adjusted_withdrawal (float), portfolio_longevity_years (float), success_probability_estimate (float)
MCP Tool Name: four_percent_rule_calculator
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "four_percent_rule_calculator",
    "description": (
        "Applies the 4% rule to approximate sustainable withdrawals, adjusts for desired "
        "horizon and inflation, and scores success probability heuristically."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "portfolio_balance": {
                "type": "number",
                "description": "Current investable retirement portfolio in dollars.",
            },
            "annual_expenses": {
                "type": "number",
                "description": "Desired annual retirement spending in dollars.",
            },
            "inflation_rate": {
                "type": "number",
                "description": "Expected annual inflation rate as decimal.",
            },
            "retirement_years": {
                "type": "number",
                "description": "Planning horizon in years, typically 25-35.",
            },
        },
        "required": ["portfolio_balance", "annual_expenses", "inflation_rate", "retirement_years"],
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


def four_percent_rule_calculator(**kwargs: Any) -> dict:
    """Assess sustainable withdrawal rate, longevity, and success odds."""
    try:
        portfolio_balance = float(kwargs["portfolio_balance"])
        annual_expenses = float(kwargs["annual_expenses"])
        inflation_rate = float(kwargs["inflation_rate"])
        retirement_years = int(kwargs["retirement_years"])

        if portfolio_balance <= 0:
            raise ValueError("portfolio_balance must be positive")
        if annual_expenses <= 0:
            raise ValueError("annual_expenses must be positive")
        if retirement_years <= 0:
            raise ValueError("retirement_years must be positive")

        safe_withdrawal = portfolio_balance * 0.04
        inflation_adjustment = (1 + inflation_rate) ** (retirement_years / 30)
        adjusted_withdrawal = safe_withdrawal / inflation_adjustment
        portfolio_longevity_years = portfolio_balance / annual_expenses
        coverage_ratio = safe_withdrawal / annual_expenses
        success_probability = min(max(coverage_ratio / 1.25, 0.0), 1.0)

        return {
            "status": "success",
            "data": {
                "safe_withdrawal": safe_withdrawal,
                "adjusted_withdrawal": adjusted_withdrawal,
                "portfolio_longevity_years": portfolio_longevity_years,
                "success_probability_estimate": success_probability,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"four_percent_rule_calculator failed: {e}")
        _log_lesson(f"four_percent_rule_calculator: {e}")
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
