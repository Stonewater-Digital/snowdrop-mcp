"""
Execuve Summary: Calculates Sharpe ratio and return statistics for a strategy.
Inputs: returns (list[float]), risk_free_rate (float)
Outputs: sharpe_ratio (float), annualized_return (float), annualized_vol (float), excess_return (float), interpretation (str)
MCP Tool Name: sharpe_ratio_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TRADING_DAYS = 252

TOOL_META = {
    "name": "sharpe_ratio_calculator",
    "description": "Computes annualized Sharpe ratio, return, and volatility for a return series.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "returns": {"type": "array", "description": "Periodic strategy returns (decimal)."},
            "risk_free_rate": {"type": "number", "description": "Annual risk-free rate in decimal form."}
        },
        "required": ["returns", "risk_free_rate"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"}
        },
        "required": ["status", "timestamp"]
    }
}


def sharpe_ratio_calculator(**kwargs: Any) -> dict:
    """Computes mean excess return divided by standard deviation (Sharpe) with annualization."""
    try:
        returns = kwargs.get("returns")
        risk_free_rate = kwargs.get("risk_free_rate")
        if not isinstance(returns, list) or len(returns) < 2:
            raise ValueError("returns must be a list with at least two observations")
        if not isinstance(risk_free_rate, (int, float)):
            raise ValueError("risk_free_rate must be numeric")

        returns_clean = []
        for value in returns:
            if not isinstance(value, (int, float)):
                raise TypeError("returns must be numeric")
            returns_clean.append(float(value))

        mean_return = sum(returns_clean) / len(returns_clean)
        variance = sum((value - mean_return) ** 2 for value in returns_clean) / (len(returns_clean) - 1)
        std_dev = math.sqrt(variance)
        if std_dev == 0:
            raise ZeroDivisionError("standard deviation is zero; Sharpe undefined")

        rf_daily = risk_free_rate / TRADING_DAYS
        excess_return = mean_return - rf_daily
        sharpe_ratio = (excess_return / std_dev) * math.sqrt(TRADING_DAYS)
        cumulative_return = 1.0
        for ret in returns_clean:
            cumulative_return *= (1 + ret)
        annualized_return = cumulative_return ** (TRADING_DAYS / len(returns_clean)) - 1
        annualized_vol = std_dev * math.sqrt(TRADING_DAYS)

        interpretation = "acceptable"
        if sharpe_ratio >= 2:
            interpretation = "excellent"
        elif sharpe_ratio >= 1:
            interpretation = "good"
        elif sharpe_ratio <= 0:
            interpretation = "poor"

        return {
            "status": "success",
            "data": {
                "sharpe_ratio": sharpe_ratio,
                "annualized_return": annualized_return,
                "annualized_vol": annualized_vol,
                "excess_return": excess_return * TRADING_DAYS,
                "interpretation": interpretation
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"sharpe_ratio_calculator failed: {e}")
        _log_lesson(f"sharpe_ratio_calculator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
