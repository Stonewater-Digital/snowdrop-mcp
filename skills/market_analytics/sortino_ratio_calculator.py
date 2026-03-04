"""
Execuve Summary: Computes Sortino ratio focusing on downside volatility.
Inputs: returns (list[float]), risk_free_rate (float), target_return (float|None)
Outputs: sortino_ratio (float), downside_deviation (float), upside_capture (float), vs_sharpe_comparison (str)
MCP Tool Name: sortino_ratio_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TRADING_DAYS = 252

TOOL_META = {
    "name": "sortino_ratio_calculator",
    "description": "Computes Sortino ratio with downside deviation and contextualizes relative to Sharpe.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "returns": {"type": "array", "description": "Periodic returns (decimal)."},
            "risk_free_rate": {"type": "number", "description": "Annual risk-free rate."},
            "target_return": {"type": "number", "description": "Optional target return per period."}
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


def sortino_ratio_calculator(**kwargs: Any) -> dict:
    """Calculates Sortino ratio by isolating returns below a user-defined target."""
    try:
        returns = kwargs.get("returns")
        risk_free_rate = kwargs.get("risk_free_rate")
        target_return = kwargs.get("target_return")

        if not isinstance(returns, list) or len(returns) < 2:
            raise ValueError("returns must be a list with at least two points")
        if not isinstance(risk_free_rate, (int, float)):
            raise ValueError("risk_free_rate must be numeric")
        returns_clean = []
        for value in returns:
            if not isinstance(value, (int, float)):
                raise TypeError("returns must be numeric")
            returns_clean.append(float(value))

        rf_daily = risk_free_rate / TRADING_DAYS
        target = target_return if isinstance(target_return, (int, float)) else rf_daily
        downside_returns = [max(target - ret, 0) for ret in returns_clean]
        downside_variance = sum(val ** 2 for val in downside_returns) / len(downside_returns)
        downside_deviation = math.sqrt(downside_variance)
        if downside_deviation == 0:
            raise ZeroDivisionError("downside deviation is zero; Sortino undefined")

        avg_return = sum(returns_clean) / len(returns_clean)
        excess_return = avg_return - target
        sortino_ratio = (excess_return * TRADING_DAYS) / (downside_deviation * math.sqrt(TRADING_DAYS))

        positive_returns = [ret for ret in returns_clean if ret > 0]
        upside_capture = (sum(positive_returns) / len(positive_returns)) if positive_returns else 0.0
        vs_sharpe = "better_than_sharpe" if sortino_ratio > 1 else "needs_improvement"

        return {
            "status": "success",
            "data": {
                "sortino_ratio": sortino_ratio,
                "downside_deviation": downside_deviation,
                "upside_capture": upside_capture,
                "vs_sharpe_comparison": vs_sharpe
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"sortino_ratio_calculator failed: {e}")
        _log_lesson(f"sortino_ratio_calculator: {e}")
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
