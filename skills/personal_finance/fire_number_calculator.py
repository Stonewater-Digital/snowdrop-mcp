"""
Executive Smary: Calculates FIRE, Coast FIRE, and Barista FIRE targets with savings timeline.
Inputs: annual_expenses (float), withdrawal_rate (float), current_savings (float), annual_savings (float), investment_return (float)
Outputs: fire_number (float), years_to_fire (float), savings_rate (float), coast_fire_number (float), barista_fire_number (float)
MCP Tool Name: fire_number_calculator
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "fire_number_calculator",
    "description": (
        "Computes the FIRE nest egg based on expenses and withdrawal rate, simulates years "
        "to reach it with contributions, and reports Coast/Barista FIRE thresholds."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "annual_expenses": {
                "type": "number",
                "description": "Target annual spending in retirement.",
            },
            "withdrawal_rate": {
                "type": "number",
                "description": "Safe withdrawal rate as decimal (e.g., 0.04).",
            },
            "current_savings": {
                "type": "number",
                "description": "Existing investable assets.",
            },
            "annual_savings": {
                "type": "number",
                "description": "Annual contributions to the portfolio.",
            },
            "investment_return": {
                "type": "number",
                "description": "Expected annual investment return as decimal.",
            },
        },
        "required": [
            "annual_expenses",
            "withdrawal_rate",
            "current_savings",
            "annual_savings",
            "investment_return",
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


def fire_number_calculator(**kwargs: Any) -> dict:
    """Estimate FIRE target and time horizon along with Coast and Barista variants."""
    try:
        annual_expenses = float(kwargs["annual_expenses"])
        withdrawal_rate = float(kwargs["withdrawal_rate"])
        current_savings = float(kwargs["current_savings"])
        annual_savings = float(kwargs["annual_savings"])
        investment_return = float(kwargs["investment_return"])

        if annual_expenses <= 0 or withdrawal_rate <= 0:
            raise ValueError("annual_expenses and withdrawal_rate must be positive")
        if current_savings < 0 or annual_savings < 0:
            raise ValueError("current_savings and annual_savings must be non-negative")

        fire_number = annual_expenses / withdrawal_rate
        savings_rate = (
            annual_savings / (annual_savings + annual_expenses)
            if (annual_savings + annual_expenses) > 0
            else 0.0
        )
        years_to_fire = _years_to_target(
            current_savings, annual_savings, investment_return, fire_number
        )
        coast_fire_number = fire_number / ((1 + investment_return) ** max(years_to_fire, 1))
        barista_fire_number = (annual_expenses * 0.7) / withdrawal_rate

        return {
            "status": "success",
            "data": {
                "fire_number": fire_number,
                "years_to_fire": years_to_fire,
                "savings_rate": savings_rate,
                "coast_fire_number": coast_fire_number,
                "barista_fire_number": barista_fire_number,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"fire_number_calculator failed: {e}")
        _log_lesson(f"fire_number_calculator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _years_to_target(
    current: float, contribution: float, rate: float, target: float, max_years: int = 80
) -> float:
    balance = current
    for year in range(1, max_years + 1):
        balance = balance * (1 + rate) + contribution
        if balance >= target:
            return year
    return float("inf") if rate > 0 else max_years


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
