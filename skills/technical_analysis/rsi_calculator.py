"""
Execuve Summary: Calculates Wilder's Relative Strength Index to gauge momentum extremes.
Inputs: prices (list[float]), period (int)
Outputs: rsi_series (list[float]), current_rsi (float), zone (str), avg_gain (float), avg_loss (float), divergence_warning (str)
MCP Tool Name: rsi_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "rsi_calculator",
    "description": "Computes RSI using J. Welles Wilder's smoothing to spot overbought or oversold conditions.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "prices": {"type": "array", "description": "Close prices (oldest first)."},
            "period": {"type": "integer", "description": "RSI lookback period (default 14)."}
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


def rsi_calculator(**kwargs: Any) -> dict:
    """Applies Wilder's 1978 formula averaging gains and losses via exponential smoothing."""
    try:
        prices_raw = kwargs.get("prices")
        period = kwargs.get("period")

        if not isinstance(period, int) or period <= 1:
            raise ValueError("period must be an integer greater than 1")
        if not isinstance(prices_raw, list) or len(prices_raw) <= period:
            raise ValueError("prices list must longer than the RSI period")

        prices = []
        for price in prices_raw:
            if not isinstance(price, (int, float)):
                raise TypeError("prices must contain numeric values")
            prices.append(float(price))

        gains = [0.0]
        losses = [0.0]
        for idx in range(1, len(prices)):
            delta = prices[idx] - prices[idx - 1]
            gains.append(max(delta, 0.0))
            losses.append(abs(min(delta, 0.0)))

        avg_gain = sum(gains[1:period + 1]) / period
        avg_loss = sum(losses[1:period + 1]) / period
        rsi_series = [math.nan] * len(prices)
        rs = avg_gain / avg_loss if avg_loss != 0 else math.inf
        rsi_series[period] = 100 - (100 / (1 + rs)) if math.isfinite(rs) else 100.0

        for idx in range(period + 1, len(prices)):
            avg_gain = ((avg_gain * (period - 1)) + gains[idx]) / period
            avg_loss = ((avg_loss * (period - 1)) + losses[idx]) / period
            if avg_loss == 0:
                rsi_value = 100.0
            else:
                rs = avg_gain / avg_loss
                rsi_value = 100 - (100 / (1 + rs))
            rsi_series[idx] = rsi_value

        current_rsi = rsi_series[-1]
        if math.isnan(current_rsi):
            raise ValueError("unable to compute RSI for final point")

        if current_rsi >= 70:
            zone = "overbought"
        elif current_rsi <= 30:
            zone = "oversold"
        else:
            zone = "neutral"

        divergence_warning = "none"
        if len(prices) >= 2 * period:
            recent_high_price = max(prices[-period:])
            prior_high_price = max(prices[-2 * period:-period])
            recent_low_price = min(prices[-period:])
            prior_low_price = min(prices[-2 * period:-period])
            recent_high_rsi = max([value for value in rsi_series[-period:] if not math.isnan(value)])
            prior_high_rsi = max([value for value in rsi_series[-2 * period:-period] if not math.isnan(value)])
            recent_low_rsi = min([value for value in rsi_series[-period:] if not math.isnan(value)])
            prior_low_rsi = min([value for value in rsi_series[-2 * period:-period] if not math.isnan(value)])
            if recent_high_price > prior_high_price and recent_high_rsi < prior_high_rsi:
                divergence_warning = "bearish_divergence"
            elif recent_low_price < prior_low_price and recent_low_rsi > prior_low_rsi:
                divergence_warning = "bullish_divergence"

        return {
            "status": "success",
            "data": {
                "rsi_series": rsi_series,
                "current_rsi": current_rsi,
                "zone": zone,
                "avg_gain": avg_gain,
                "avg_loss": avg_loss,
                "divergence_warning": divergence_warning
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"rsi_calculator failed: {e}")
        _log_lesson(f"rsi_calculator: {e}")
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
