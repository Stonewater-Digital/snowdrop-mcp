"""
Execuve Summary: Fits a linear regression to price and projects standard deviation channels.
Inputs: prices (list[float]), period (int), num_std (float)
Outputs: regression_line (list[float]), upper_channel (list[float]), lower_channel (list[float]), slope (float), r_squared (float), price_position (str)
MCP Tool Name: standard_deviation_channel
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "standard_deviation_channel",
    "description": "Performs least-squares regression on prices and offsets by standard deviation bands.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "prices": {"type": "array", "description": "Price series."},
            "period": {"type": "integer", "description": "Number of observations used for regression."},
            "num_std": {"type": "number", "description": "Standard deviation multiplier for channel width."}
        },
        "required": ["prices", "period", "num_std"]
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


def standard_deviation_channel(**kwargs: Any) -> dict:
    """Fits y = a + b*x over the last N prices and sets channels at ±num_std standard deviations."""
    try:
        prices = kwargs.get("prices")
        period = kwargs.get("period")
        num_std = kwargs.get("num_std")

        if not isinstance(prices, list) or len(prices) < period:
            raise ValueError("prices must be list with length >= period")
        if not isinstance(period, int) or period <= 1:
            raise ValueError("period must be integer > 1")
        if not isinstance(num_std, (int, float)) or num_std <= 0:
            raise ValueError("num_std must be positive number")

        prices_f = []
        for price in prices:
            if not isinstance(price, (int, float)):
                raise TypeError("prices must be numeric")
            prices_f.append(float(price))

        window = prices_f[-period:]
        x_values = list(range(period))
        mean_x = sum(x_values) / period
        mean_y = sum(window) / period
        cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(x_values, window))
        var_x = sum((x - mean_x) ** 2 for x in x_values)
        if var_x == 0:
            raise ZeroDivisionError("variance of x is zero")
        slope = cov / var_x
        intercept = mean_y - slope * mean_x

        regression_line = [math.nan] * len(prices_f)
        upper_channel = [math.nan] * len(prices_f)
        lower_channel = [math.nan] * len(prices_f)
        residuals = [0.0] * period
        for idx, price in enumerate(window):
            predicted = intercept + slope * idx
            residuals[idx] = price - predicted
            overall_idx = len(prices_f) - period + idx
            regression_line[overall_idx] = predicted
        std_dev = math.sqrt(sum(res ** 2 for res in residuals) / period)
        for idx in range(period):
            overall_idx = len(prices_f) - period + idx
            base = regression_line[overall_idx]
            if math.isnan(base):
                continue
            upper_channel[overall_idx] = base + num_std * std_dev
            lower_channel[overall_idx] = base - num_std * std_dev

        total_ss = sum((price - mean_y) ** 2 for price in window)
        residual_ss = sum(res ** 2 for res in residuals)
        r_squared = 1 - (residual_ss / total_ss) if total_ss != 0 else 0.0
        current_price = prices_f[-1]
        current_regression = regression_line[-1]
        if math.isnan(current_regression):
            raise ValueError("insufficient regression points")
        if current_price > upper_channel[-1]:
            price_position = "above"
        elif current_price < lower_channel[-1]:
            price_position = "below"
        else:
            price_position = "inside"

        return {
            "status": "success",
            "data": {
                "regression_line": regression_line,
                "upper_channel": upper_channel,
                "lower_channel": lower_channel,
                "slope": slope,
                "r_squared": r_squared,
                "price_position": price_position
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"standard_deviation_channel failed: {e}")
        _log_lesson(f"standard_deviation_channel: {e}")
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
