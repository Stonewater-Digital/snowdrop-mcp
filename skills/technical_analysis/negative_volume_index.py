"""
Execuve Summary: Calculates the Negative Volume Index (NVI) to infer smart-money participation on low volume days.
Inputs: closes (list[float]), volumes (list[float])
Outputs: nvi_series (list[float]), nvi_signal_line (list[float]), current_nvi (float), bull_market_probability (str)
MCP Tool Name: negative_volume_index
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "negative_volume_index",
    "description": "Computes the Negative Volume Index with a 255-day EMA signal line per Norman Fosback.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "closes": {"type": "array", "description": "Close prices."},
            "volumes": {"type": "array", "description": "Volume per session."}
        },
        "required": ["closes", "volumes"]
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

SIGNAL_PERIOD = 255


def negative_volume_index(**kwargs: Any) -> dict:
    """Updates NVI only when volume declines and compares against Fosback's 255-day EMA threshold."""
    try:
        closes = kwargs.get("closes")
        volumes = kwargs.get("volumes")
        if not isinstance(closes, list) or not isinstance(volumes, list) or len(closes) != len(volumes):
            raise ValueError("closes and volumes must be equal-length lists")
        if len(closes) < 2:
            raise ValueError("need at least two observations for NVI")

        closes_f = []
        volumes_f = []
        for c, v in zip(closes, volumes):
            if not isinstance(c, (int, float)) or not isinstance(v, (int, float)):
                raise TypeError("closes and volumes must be numeric")
            closes_f.append(float(c))
            volumes_f.append(float(v))

        nvi_series = [1000.0]
        for idx in range(1, len(closes_f)):
            prev_nvi = nvi_series[-1]
            if volumes_f[idx] < volumes_f[idx - 1] and closes_f[idx - 1] != 0:
                ret = (closes_f[idx] - closes_f[idx - 1]) / closes_f[idx - 1]
                nvi_series.append(prev_nvi * (1 + ret))
            else:
                nvi_series.append(prev_nvi)

        signal_line = _ema(nvi_series, SIGNAL_PERIOD)
        current_nvi = nvi_series[-1]
        current_signal = signal_line[-1]
        if math.isnan(current_signal):
            bull_prob = "signal_unavailable"
        else:
            bull_prob = "bullish_bias" if current_nvi > current_signal else "defensive_bias"

        return {
            "status": "success",
            "data": {
                "nvi_series": nvi_series,
                "nvi_signal_line": signal_line,
                "current_nvi": current_nvi,
                "bull_market_probability": bull_prob
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"negative_volume_index failed: {e}")
        _log_lesson(f"negative_volume_index: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _ema(values: list[float], period: int) -> list[float]:
    ema = [math.nan] * len(values)
    if len(values) < period:
        return ema
    alpha = 2 / (period + 1)
    seed = sum(values[:period]) / period
    ema[period - 1] = seed
    prev = seed
    for idx in range(period, len(values)):
        prev = alpha * values[idx] + (1 - alpha) * prev
        ema[idx] = prev
    return ema


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
