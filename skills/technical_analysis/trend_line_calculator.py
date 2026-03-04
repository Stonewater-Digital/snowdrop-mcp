"""
Execuve Summary: Fits trendlines via regression or peak/trough connections and evaluates breaks.
Inputs: prices (list[float]), lookback (int), method (str)
Outputs: trendline_slope (float), trendline_intercept (float), r_squared (float), support_trendline (list[float]), resistance_trendline (list[float]), break_detected (str)
MCP Tool Name: trend_line_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "trend_line_calculator",
    "description": "Constructs trendlines using linear regression or peak/trough anchors to monitor price breaks.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "prices": {"type": "array", "description": "Price series."},
            "lookback": {"type": "integer", "description": "Number of bars used for the analysis."},
            "method": {"type": "string", "description": "linear_regression or peak_trough."}
        },
        "required": ["prices", "lookback", "method"]
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


def trend_line_calculator(**kwargs: Any) -> dict:
    """Generates support/resistance trendlines and reports recent breakouts."""
    try:
        prices = kwargs.get("prices")
        lookback = kwargs.get("lookback")
        method = kwargs.get("method")

        if not isinstance(prices, list) or len(prices) < lookback:
            raise ValueError("prices list must be at least as long as lookback")
        if not isinstance(lookback, int) or lookback <= 1:
            raise ValueError("lookback must be integer > 1")
        if not isinstance(method, str) or method.lower() not in {"linear_regression", "peak_trough"}:
            raise ValueError("method must be linear_regression or peak_trough")

        method = method.lower()
        window = [float(price) for price in prices[-lookback:]]
        x_vals = list(range(lookback))
        latest_price = window[-1]
        regression_line: list[float] = []
        support_line: list[float] = []
        resistance_line: list[float] = []
        slope = 0.0
        intercept = 0.0
        r_squared = math.nan

        if method == "linear_regression":
            mean_x = sum(x_vals) / lookback
            mean_y = sum(window) / lookback
            cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(x_vals, window))
            var_x = sum((x - mean_x) ** 2 for x in x_vals)
            if var_x == 0:
                raise ZeroDivisionError("variance of x is zero")
            slope = cov / var_x
            intercept = mean_y - slope * mean_x
            regression_line = [intercept + slope * x for x in x_vals]
            residuals = [price - line for price, line in zip(window, regression_line)]
            std_dev = math.sqrt(sum(res ** 2 for res in residuals) / lookback)
            support_line = [line - std_dev for line in regression_line]
            resistance_line = [line + std_dev for line in regression_line]
            total_ss = sum((price - mean_y) ** 2 for price in window)
            residual_ss = sum(res ** 2 for res in residuals)
            r_squared = 1 - (residual_ss / total_ss) if total_ss != 0 else 0.0
        else:
            slope, intercept = _peak_trough_lines(window, lookback)
            regression_line = [intercept + slope * x for x in x_vals]
            support_line = _anchor_line(window, lookback, mode="support")
            resistance_line = _anchor_line(window, lookback, mode="resistance")
            r_squared = math.nan

        last_support = support_line[-1] if support_line else regression_line[-1]
        last_resistance = resistance_line[-1] if resistance_line else regression_line[-1]
        break_detected = "none"
        if latest_price > last_resistance:
            break_detected = "bullish_break"
        elif latest_price < last_support:
            break_detected = "bearish_break"

        return {
            "status": "success",
            "data": {
                "trendline_slope": slope,
                "trendline_intercept": intercept,
                "r_squared": r_squared,
                "support_trendline": support_line,
                "resistance_trendline": resistance_line,
                "break_detected": break_detected
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"trend_line_calculator failed: {e}")
        _log_lesson(f"trend_line_calculator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _peak_trough_lines(window: list[float], lookback: int) -> tuple[float, float]:
    x_vals = list(range(lookback))
    peaks = [(idx, window[idx]) for idx in range(1, lookback - 1) if window[idx] > window[idx - 1] and window[idx] > window[idx + 1]]
    troughs = [(idx, window[idx]) for idx in range(1, lookback - 1) if window[idx] < window[idx - 1] and window[idx] < window[idx + 1]]
    if len(peaks) >= 2:
        x1, y1 = peaks[0]
        x2, y2 = peaks[-1]
        slope_res = (y2 - y1) / (x2 - x1) if x2 != x1 else 0.0
        intercept_res = y1 - slope_res * x1
    else:
        slope_res = 0.0
        intercept_res = window[-1]
    if len(troughs) >= 2:
        x1, y1 = troughs[0]
        x2, y2 = troughs[-1]
        slope_sup = (y2 - y1) / (x2 - x1) if x2 != x1 else 0.0
        intercept_sup = y1 - slope_sup * x1
    else:
        slope_sup = 0.0
        intercept_sup = window[-1]
    slope = (slope_res + slope_sup) / 2
    intercept = (intercept_res + intercept_sup) / 2
    return slope, intercept


def _anchor_line(window: list[float], lookback: int, mode: str) -> list[float]:
    x_vals = list(range(lookback))
    pivots = []
    if mode == "support":
        pivots = [(idx, window[idx]) for idx in range(1, lookback - 1) if window[idx] <= window[idx - 1] and window[idx] <= window[idx + 1]]
    else:
        pivots = [(idx, window[idx]) for idx in range(1, lookback - 1) if window[idx] >= window[idx - 1] and window[idx] >= window[idx + 1]]
    if len(pivots) < 2:
        baseline = window[0]
        slope = 0.0
    else:
        (x1, y1), (x2, y2) = pivots[0], pivots[-1]
        slope = (y2 - y1) / (x2 - x1) if x2 != x1 else 0.0
        baseline = y1
    intercept = baseline - slope * pivots[0][0] if pivots else baseline
    return [intercept + slope * x for x in x_vals]


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
