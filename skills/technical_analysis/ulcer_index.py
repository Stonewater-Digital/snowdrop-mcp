"""
Execuve Summary: Calculates Ulcer Index to measure downside risk from drawdowns.
Inputs: prices (list[float]), period (int), risk_free_rate (float|None)
Outputs: ulcer_index (float), max_drawdown_in_period (float), ulcer_performance_index (float|None), pain_index (float)
MCP Tool Name: ulcer_index
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "ulcer_index",
    "description": "Computes the Ulcer Index and related drawdown metrics to capture downside pain.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "prices": {"type": "array", "description": "Price or NAV series."},
            "period": {"type": "integer", "description": "Lookback for drawdown window."},
            "risk_free_rate": {"type": "number", "description": "Optional annual risk-free rate in percent."}
        },
        "required": ["prices", "period"]
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


def ulcer_index(**kwargs: Any) -> dict:
    """Implements Peter Martin's Ulcer Index using square root of mean squared drawdowns."""
    try:
        prices = kwargs.get("prices")
        period = kwargs.get("period")
        risk_free_rate = kwargs.get("risk_free_rate")

        if not isinstance(prices, list) or len(prices) < period or len(prices) < 2:
            raise ValueError("prices must be list with length >= period")
        if not isinstance(period, int) or period <= 1:
            raise ValueError("period must be integer > 1")
        if risk_free_rate is not None and not isinstance(risk_free_rate, (int, float)):
            raise ValueError("risk_free_rate must be numeric when provided")

        prices_f = []
        for price in prices:
            if not isinstance(price, (int, float)):
                raise TypeError("prices must be numeric")
            if price <= 0:
                raise ValueError("prices must be positive for drawdown calculations")
            prices_f.append(float(price))

        window = prices_f[-period:]
        current_peak = window[0]
        drawdowns = []
        for price in window:
            current_peak = max(current_peak, price)
            drawdown_pct = (price - current_peak) / current_peak * 100
            drawdowns.append(drawdown_pct)

        squared = [(dd) ** 2 for dd in drawdowns]
        ulcer_index_value = math.sqrt(sum(squared) / len(squared))
        max_drawdown = min(drawdowns)
        pain_index = sum(abs(dd) for dd in drawdowns) / len(drawdowns)

        ulcer_performance = None
        if risk_free_rate is not None:
            total_return = (window[-1] / window[0]) - 1
            annualized_return = ((1 + total_return) ** (252 / len(window))) - 1 if len(window) > 0 else total_return
            ulcer_performance = ((annualized_return * 100) - risk_free_rate) / ulcer_index_value if ulcer_index_value != 0 else None

        return {
            "status": "success",
            "data": {
                "ulcer_index": ulcer_index_value,
                "max_drawdown_in_period": max_drawdown,
                "ulcer_performance_index": ulcer_performance,
                "pain_index": pain_index
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"ulcer_index failed: {e}")
        _log_lesson(f"ulcer_index: {e}")
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
