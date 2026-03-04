"""
Execuve Summary: Computes the Volume Price Trend (VPT) indicator for trend confirmation.
Inputs: closes (list[float]), volumes (list[float]), sma_period (int)
Outputs: vpt_series (list[float]), current_vpt (float), vpt_sma (list[float]), signal (str), divergence (str)
MCP Tool Name: volume_price_trend
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "volume_price_trend",
    "description": "Calculates cumulative Volume Price Trend and compares against SMA to detect divergences.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "closes": {"type": "array", "description": "Close prices."},
            "volumes": {"type": "array", "description": "Volumes aligned with closes."},
            "sma_period": {"type": "integer", "description": "SMA period for VPT smoothing."}
        },
        "required": ["closes", "volumes", "sma_period"]
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


def volume_price_trend(**kwargs: Any) -> dict:
    """Cumulates VPT and compares to its SMA to highlight confirmation or divergence."""
    try:
        closes = kwargs.get("closes")
        volumes = kwargs.get("volumes")
        sma_period = kwargs.get("sma_period")

        if not isinstance(closes, list) or not isinstance(volumes, list) or len(closes) != len(volumes):
            raise ValueError("closes and volumes must be equal-length lists")
        if len(closes) < 2:
            raise ValueError("need at least two points for VPT")
        if not isinstance(sma_period, int) or sma_period <= 1:
            raise ValueError("sma_period must be integer > 1")

        closes_f = []
        volumes_f = []
        for c, v in zip(closes, volumes):
            if not isinstance(c, (int, float)) or not isinstance(v, (int, float)):
                raise TypeError("inputs must be numeric")
            closes_f.append(float(c))
            volumes_f.append(float(v))

        vpt_series = [0.0]
        for idx in range(1, len(closes_f)):
            prev_close = closes_f[idx - 1]
            if prev_close == 0:
                raise ZeroDivisionError("previous close cannot be zero")
            value = vpt_series[-1] + volumes_f[idx] * ((closes_f[idx] - prev_close) / prev_close)
            vpt_series.append(value)

        vpt_sma = []
        for idx in range(len(vpt_series)):
            if idx + 1 < sma_period:
                vpt_sma.append(math.nan)
            else:
                vpt_sma.append(sum(vpt_series[idx - sma_period + 1: idx + 1]) / sma_period)

        current_vpt = vpt_series[-1]
        current_sma = vpt_sma[-1]
        if math.isnan(current_sma):
            raise ValueError("insufficient data for VPT SMA")
        signal = "bullish" if current_vpt > current_sma else ("bearish" if current_vpt < current_sma else "neutral")

        divergence = "none"
        price_change = closes_f[-1] - closes_f[-2]
        vpt_change = current_vpt - vpt_series[-2]
        if price_change > 0 and vpt_change < 0:
            divergence = "bearish"
        elif price_change < 0 and vpt_change > 0:
            divergence = "bullish"

        return {
            "status": "success",
            "data": {
                "vpt_series": vpt_series,
                "current_vpt": current_vpt,
                "vpt_sma": vpt_sma,
                "signal": signal,
                "divergence": divergence
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"volume_price_trend failed: {e}")
        _log_lesson(f"volume_price_trend: {e}")
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
