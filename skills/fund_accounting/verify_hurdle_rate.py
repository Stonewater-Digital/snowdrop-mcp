"""
Executive Summary: Validates whether LP preferred return hurdle has been met and computes a simple IRR approximation.

Inputs: committed_capital (float), distributions_to_date (float), hurdle_rate (float), time_period (float, years)
Outputs: dict with hurdle_met (bool), shortfall (float), irr (float)
MCP Tool Name: verify_hurdle_rate
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "verify_hurdle_rate",
    "description": "Validates whether LP preferred return hurdle has been met and computes a simple IRR approximation.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "committed_capital": {"type": "number", "description": "Total LP capital committed in dollars"},
            "distributions_to_date": {"type": "number", "description": "Total distributions paid to LPs in dollars"},
            "hurdle_rate": {"type": "number", "description": "Preferred return rate (e.g. 0.08 for 8%)"},
            "time_period": {"type": "number", "description": "Investment period in years"},
        },
        "required": ["committed_capital", "distributions_to_date", "hurdle_rate", "time_period"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "hurdle_met": {"type": "boolean"},
            "shortfall": {"type": "number"},
            "irr": {"type": "number"},
            "required_return": {"type": "number"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": ["hurdle_met", "shortfall", "irr", "required_return", "status", "timestamp"],
    },
}


def _simple_irr(committed_capital: float, distributions: float, years: float) -> float:
    """Computes simple IRR approximation using CAGR formula.

    For IRR: committed_capital * (1 + irr)^years = distributions
    => irr = (distributions / committed_capital)^(1/years) - 1

    Args:
        committed_capital: Initial capital outlay.
        distributions: Total distributions received.
        years: Number of years elapsed.

    Returns:
        float: Annualized IRR approximation. Returns -1.0 if inputs are invalid.
    """
    if committed_capital <= 0 or years <= 0 or distributions < 0:
        return -1.0
    multiple = distributions / committed_capital
    if multiple <= 0:
        return -1.0
    return (multiple ** (1.0 / years)) - 1.0


def verify_hurdle_rate(
    committed_capital: float,
    distributions_to_date: float,
    hurdle_rate: float,
    time_period: float,
    **kwargs: Any,
) -> dict:
    """Validates whether LP preferred return hurdle has been met.

    Computes the required distributions to satisfy the hurdle using simple
    compounding: required = committed_capital * (1 + hurdle_rate)^time_period.
    Then compares to actual distributions_to_date to determine shortfall and
    computes an IRR approximation via CAGR.

    Args:
        committed_capital: Total LP capital committed in dollars.
        distributions_to_date: Total distributions paid to LPs in dollars.
        hurdle_rate: Preferred return rate (e.g. 0.08).
        time_period: Investment period in fractional years.
        **kwargs: Ignored extra keyword arguments.

    Returns:
        dict: Keys include hurdle_met (bool), shortfall (float), irr (float),
              required_return (float), status, and timestamp.
    """
    try:
        if committed_capital <= 0:
            raise ValueError("committed_capital must be positive")
        if time_period <= 0:
            raise ValueError("time_period must be positive")
        if not (0.0 <= hurdle_rate <= 1.0):
            raise ValueError("hurdle_rate must be between 0 and 1")

        # Required distributions to clear the hurdle (compound)
        required_return = committed_capital * ((1.0 + hurdle_rate) ** time_period)
        shortfall = max(0.0, required_return - distributions_to_date)
        hurdle_met = distributions_to_date >= required_return

        irr = _simple_irr(committed_capital, distributions_to_date, time_period)

        result = {
            "hurdle_met": hurdle_met,
            "shortfall": round(shortfall, 2),
            "irr": round(irr, 6),
            "required_return": round(required_return, 2),
            "actual_distributions": round(distributions_to_date, 2),
            "committed_capital": round(committed_capital, 2),
            "hurdle_rate": hurdle_rate,
            "time_period_years": time_period,
        }
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as e:
        logger.error(f"verify_hurdle_rate failed: {e}")
        _log_lesson(f"verify_hurdle_rate: {e}")
        return {"status": "error", "error": str(e), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    """Appends an error lesson to the lessons log.

    Args:
        message: The lesson message to log.
    """
    os.makedirs("logs", exist_ok=True)
    with open("logs/lessons.md", "a") as f:
        f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
