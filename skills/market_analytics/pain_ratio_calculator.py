"""
Execuve Summary: Calculates Pain Index and Pain Ratio for downside assessment.
Inputs: prices (list[float])
Outputs: pain_index (float), pain_ratio (float), mean_drawdown (float), drawdown_duration_avg (float)
MCP Tool Name: pain_ratio_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "pain_ratio_calculator",
    "description": "Computes the Pain Index (average drawdown magnitude) and Pain Ratio (return/Pain).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "prices": {"type": "array", "description": "Equity curve or NAV series."}
        },
        "required": ["prices"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def pain_ratio_calculator(**kwargs: Any) -> dict:
    """Derives Pain Index and Pain Ratio based on drawdown depth and duration."""
    try:
        prices = kwargs.get("prices")
        if not isinstance(prices, list) or len(prices) < 2:
            raise ValueError("prices must be list with at least two observations")
        equity = []
        for price in prices:
            if not isinstance(price, (int, float)) or price <= 0:
                raise ValueError("prices must be positive numbers")
            equity.append(float(price))

        peak = equity[0]
        drawdowns = []
        drawdown_lengths = []
        current_length = 0
        for price in equity:
            if price > peak:
                peak = price
                if current_length:
                    drawdown_lengths.append(current_length)
                    current_length = 0
            else:
                current_length += 1
            drawdowns.append(price / peak - 1)
        if current_length:
            drawdown_lengths.append(current_length)
        negative_drawdowns = [abs(dd) for dd in drawdowns if dd < 0]
        pain_index = sum(negative_drawdowns) / len(drawdowns)
        mean_drawdown = sum(abs(dd) for dd in drawdowns if dd < 0) / len(negative_drawdowns) if negative_drawdowns else 0.0
        duration_avg = sum(drawdown_lengths) / len(drawdown_lengths) if drawdown_lengths else 0.0
        total_return = equity[-1] / equity[0] - 1
        years = len(prices) / 252
        annualized_return = (1 + total_return) ** (1 / years) - 1 if years > 0 else total_return
        pain_ratio = annualized_return / pain_index if pain_index != 0 else math.inf

        return {
            "status": "success",
            "data": {
                "pain_index": pain_index,
                "pain_ratio": pain_ratio,
                "mean_drawdown": mean_drawdown,
                "drawdown_duration_avg": duration_avg
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"pain_ratio_calculator failed: {e}")
        _log_lesson(f"pain_ratio_calculator: {e}")
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
