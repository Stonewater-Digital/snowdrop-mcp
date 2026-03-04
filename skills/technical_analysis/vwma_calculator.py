"""
Execuve Summary: Calculates volume-weighted moving averages to reward high-volume prices.
Inputs: prices (list[float]), volumes (list[float]), period (int)
Outputs: vwma_series (list[float]), current_vwma (float), vs_sma_divergence (float), volume_confirmation (str)
MCP Tool Name: vwma_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "vwma_calculator",
    "description": "Computes the volume-weighted moving average to compare price trends against standard SMA and confirm with volume.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "prices": {"type": "array", "description": "Closing prices (oldest first)."},
            "volumes": {"type": "array", "description": "Volume per period aligned with prices."},
            "period": {"type": "integer", "description": "Lookback window for VWMA."}
        },
        "required": ["prices", "volumes", "period"]
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


def vwma_calculator(**kwargs: Any) -> dict:
    """Weights prices by traded volume to emphasize conviction behind moves."""
    try:
        prices = kwargs.get("prices")
        volumes = kwargs.get("volumes")
        period = kwargs.get("period")

        if not isinstance(prices, list) or not isinstance(volumes, list):
            raise ValueError("prices and volumes must be lists")
        if len(prices) != len(volumes):
            raise ValueError("prices and volumes must align in length")
        if len(prices) < 2:
            raise ValueError("price series too short")
        if not isinstance(period, int) or period <= 0:
            raise ValueError("period must be positive integer")
        if period > len(prices):
            raise ValueError("period cannot exceed length")

        prices_f = []
        volumes_f = []
        for p, v in zip(prices, volumes):
            if not isinstance(p, (int, float)) or not isinstance(v, (int, float)):
                raise TypeError("prices and volumes must be numeric")
            if v < 0:
                raise ValueError("volumes cannot be negative")
            prices_f.append(float(p))
            volumes_f.append(float(v))

        vwma_series = []
        volume_window: list[float] = []
        price_volume_window: list[float] = []
        sum_volume = 0.0
        sum_price_volume = 0.0
        sma_series = []
        price_window: list[float] = []
        sum_price = 0.0
        for idx in range(len(prices_f)):
            price = prices_f[idx]
            volume = volumes_f[idx]
            volume_window.append(volume)
            price_volume_window.append(price * volume)
            sum_volume += volume
            sum_price_volume += price * volume
            price_window.append(price)
            sum_price += price

            if len(volume_window) > period:
                sum_volume -= volume_window.pop(0)
                sum_price_volume -= price_volume_window.pop(0)
            if len(price_window) > period:
                sum_price -= price_window.pop(0)

            if len(volume_window) == period and sum_volume > 0:
                vwma_series.append(sum_price_volume / sum_volume)
                sma_series.append(sum_price / period)
            else:
                vwma_series.append(math.nan)
                sma_series.append(math.nan)

        current_vwma = vwma_series[-1]
        if math.isnan(current_vwma):
            raise ValueError("insufficient data for VWMA")
        current_sma = sma_series[-1]
        divergence = current_vwma - current_sma if not math.isnan(current_sma) else math.nan
        if math.isnan(divergence):
            vs_text = "insufficient"
        elif divergence > 0:
            vs_text = "vwma_above_sma"
        elif divergence < 0:
            vs_text = "vwma_below_sma"
        else:
            vs_text = "aligned"

        recent_volume = sum(volumes_f[-period:]) / period
        baseline_volume = sum(volumes_f[:period]) / period if len(volumes_f) >= period else recent_volume
        volume_confirmation = "rising" if recent_volume > baseline_volume else ("falling" if recent_volume < baseline_volume else "flat")

        return {
            "status": "success",
            "data": {
                "vwma_series": vwma_series,
                "current_vwma": current_vwma,
                "vs_sma_divergence": divergence,
                "volume_confirmation": volume_confirmation,
                "price_vs_vwma": vs_text
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"vwma_calculator failed: {e}")
        _log_lesson(f"vwma_calculator: {e}")
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
