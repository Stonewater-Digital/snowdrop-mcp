"""
Execuve Summary: Computes the five Ichimoku lines to evaluate trend, momentum, and support zones.
Inputs: highs (list[float]), lows (list[float]), closes (list[float]), tenkan (int), kijun (int), senkou_b (int), chikou (int)
Outputs: tenkan_sen (list[float]), kijun_sen (list[float]), senkou_span_a (list[float]), senkou_span_b (list[float]), chikou_span (list[float])
MCP Tool Name: ichimoku_cloud
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "ichimoku_cloud",
    "description": "Generates Ichimoku Kinko Hyo components (Tenkan, Kijun, Senkou A/B, Chikou) for full cloud analysis.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "highs": {"type": "array", "description": "High prices."},
            "lows": {"type": "array", "description": "Low prices."},
            "closes": {"type": "array", "description": "Closing prices."},
            "tenkan": {"type": "integer", "description": "Tenkan-sen lookback (default 9)."},
            "kijun": {"type": "integer", "description": "Kijun-sen lookback (default 26)."},
            "senkou_b": {"type": "integer", "description": "Senkou Span B lookback (default 52)."},
            "chikou": {"type": "integer", "description": "Chikou span offset (default 26)."}
        },
        "required": ["highs", "lows", "closes", "tenkan", "kijun", "senkou_b", "chikou"]
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


def ichimoku_cloud(**kwargs: Any) -> dict:
    """Implements Goichi Hosoda's Ichimoku method to visualize equilibrium and cloud dynamics."""
    try:
        highs = kwargs.get("highs")
        lows = kwargs.get("lows")
        closes = kwargs.get("closes")
        tenkan_period = kwargs.get("tenkan")
        kijun_period = kwargs.get("kijun")
        senkou_b_period = kwargs.get("senkou_b")
        chikou_shift = kwargs.get("chikou")

        for series_name, series in (("highs", highs), ("lows", lows), ("closes", closes)):
            if not isinstance(series, list) or len(series) < 2:
                raise ValueError(f"{series_name} must be a list with at least two points")
        if not (len(highs) == len(lows) == len(closes)):
            raise ValueError("highs, lows, and closes must match length")

        for label, value in (("tenkan", tenkan_period), ("kijun", kijun_period), ("senkou_b", senkou_b_period), ("chikou", chikou_shift)):
            if not isinstance(value, int) or value <= 0:
                raise ValueError(f"{label} must be a positive integer")

        highs_f = []
        lows_f = []
        closes_f = []
        for idx in range(len(highs)):
            h = highs[idx]
            l = lows[idx]
            c = closes[idx]
            if not isinstance(h, (int, float)) or not isinstance(l, (int, float)) or not isinstance(c, (int, float)):
                raise TypeError("price series must be numeric")
            highs_f.append(float(h))
            lows_f.append(float(l))
            closes_f.append(float(c))

        def _midpoint(series_high: list[float], series_low: list[float], period: int) -> list[float]:
            result = []
            for idx in range(len(series_high)):
                if idx + 1 < period:
                    result.append(math.nan)
                    continue
                window_high = max(series_high[idx - period + 1: idx + 1])
                window_low = min(series_low[idx - period + 1: idx + 1])
                result.append((window_high + window_low) / 2)
            return result

        tenkan_sen = _midpoint(highs_f, lows_f, tenkan_period)
        kijun_sen = _midpoint(highs_f, lows_f, kijun_period)
        senkou_span_a = [math.nan] * len(highs_f)
        for idx in range(len(highs_f)):
            if math.isnan(tenkan_sen[idx]) or math.isnan(kijun_sen[idx]):
                continue
            forward_index = idx + chikou_shift
            if forward_index < len(highs_f):
                senkou_span_a[forward_index] = (tenkan_sen[idx] + kijun_sen[idx]) / 2
        senkou_span_b = [math.nan] * len(highs_f)
        span_b_series = _midpoint(highs_f, lows_f, senkou_b_period)
        for idx, value in enumerate(span_b_series):
            forward_index = idx + chikou_shift
            if forward_index < len(highs_f):
                senkou_span_b[forward_index] = value

        chikou_span = [math.nan] * len(highs_f)
        for idx, close in enumerate(closes_f):
            back_index = idx - chikou_shift
            if back_index >= 0:
                chikou_span[back_index] = close

        latest_close = closes_f[-1]
        span_a_current = senkou_span_a[-1]
        span_b_current = senkou_span_b[-1]
        if math.isnan(span_a_current) or math.isnan(span_b_current):
            cloud_color = "undefined"
            price_vs_cloud = "insufficient"
        else:
            cloud_color = "green" if span_a_current > span_b_current else "red"
            upper = max(span_a_current, span_b_current)
            lower = min(span_a_current, span_b_current)
            if latest_close > upper:
                price_vs_cloud = "above"
            elif latest_close < lower:
                price_vs_cloud = "below"
            else:
                price_vs_cloud = "inside"

        tk_cross_signal = "neutral"
        if not math.isnan(tenkan_sen[-1]) and not math.isnan(kijun_sen[-1]) and not math.isnan(tenkan_sen[-2]) and not math.isnan(kijun_sen[-2]):
            prev_diff = tenkan_sen[-2] - kijun_sen[-2]
            curr_diff = tenkan_sen[-1] - kijun_sen[-1]
            if curr_diff > 0 and prev_diff <= 0:
                tk_cross_signal = "bullish"
            elif curr_diff < 0 and prev_diff >= 0:
                tk_cross_signal = "bearish"

        return {
            "status": "success",
            "data": {
                "tenkan_sen": tenkan_sen,
                "kijun_sen": kijun_sen,
                "senkou_span_a": senkou_span_a,
                "senkou_span_b": senkou_span_b,
                "chikou_span": chikou_span,
                "cloud_color": cloud_color,
                "price_vs_cloud": price_vs_cloud,
                "tk_cross_signal": tk_cross_signal
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"ichimoku_cloud failed: {e}")
        _log_lesson(f"ichimoku_cloud: {e}")
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
