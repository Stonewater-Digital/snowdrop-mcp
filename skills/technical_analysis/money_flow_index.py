"""
Execuve Summary: Computes the Money Flow Index (MFI) combining price and volume.
Inputs: highs (list[float]), lows (list[float]), closes (list[float]), volumes (list[float]), period (int)
Outputs: mfi_series (list[float]), current_mfi (float), zone (str), divergence_with_price (str)
MCP Tool Name: money_flow_index
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "money_flow_index",
    "description": "Calculates the volume-weighted RSI known as Money Flow Index (MFI).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "highs": {"type": "array", "description": "High prices."},
            "lows": {"type": "array", "description": "Low prices."},
            "closes": {"type": "array", "description": "Close prices."},
            "volumes": {"type": "array", "description": "Volume per bar."},
            "period": {"type": "integer", "description": "Lookback period (default 14)."}
        },
        "required": ["highs", "lows", "closes", "volumes", "period"]
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


def money_flow_index(**kwargs: Any) -> dict:
    """Computes MFI by categorizing positive/negative money flows and forming an RSI-style ratio."""
    try:
        highs = kwargs.get("highs")
        lows = kwargs.get("lows")
        closes = kwargs.get("closes")
        volumes = kwargs.get("volumes")
        period = kwargs.get("period")

        for series in (highs, lows, closes, volumes):
            if not isinstance(series, list) or len(series) < 2:
                raise ValueError("all inputs must be lists with at least two elements")
        if not (len(highs) == len(lows) == len(closes) == len(volumes)):
            raise ValueError("series must align")
        if not isinstance(period, int) or period <= 1:
            raise ValueError("period must be > 1")
        if period >= len(highs):
            raise ValueError("period must be less than data length")

        typical_prices = []
        raw_flows = []
        for h, l, c, v in zip(highs, lows, closes, volumes):
            if not isinstance(h, (int, float)) or not isinstance(l, (int, float)) or not isinstance(c, (int, float)) or not isinstance(v, (int, float)):
                raise TypeError("inputs must be numeric")
            tp = (float(h) + float(l) + float(c)) / 3
            typical_prices.append(tp)
            raw_flows.append(tp * float(v))

        positive_flow = []
        negative_flow = []
        for idx in range(1, len(typical_prices)):
            if typical_prices[idx] > typical_prices[idx - 1]:
                positive_flow.append(raw_flows[idx])
                negative_flow.append(0.0)
            elif typical_prices[idx] < typical_prices[idx - 1]:
                positive_flow.append(0.0)
                negative_flow.append(raw_flows[idx])
            else:
                positive_flow.append(0.0)
                negative_flow.append(0.0)

        mfi_series = [math.nan]
        for idx in range(period - 1, len(positive_flow)):
            pos_sum = sum(positive_flow[idx - period + 1: idx + 1])
            neg_sum = sum(negative_flow[idx - period + 1: idx + 1])
            money_flow_ratio = pos_sum / neg_sum if neg_sum != 0 else math.inf
            mfi = 100 - (100 / (1 + money_flow_ratio)) if math.isfinite(money_flow_ratio) else 100.0
            mfi_series.append(mfi)

        while len(mfi_series) < len(closes):
            mfi_series.insert(0, math.nan)
        current_mfi = mfi_series[-1]
        if math.isnan(current_mfi):
            raise ValueError("insufficient data for MFI")

        if current_mfi >= 80:
            zone = "overbought"
        elif current_mfi <= 20:
            zone = "oversold"
        else:
            zone = "neutral"

        divergence = "none"
        if len(closes) >= 2 * period:
            price_recent_high = max(closes[-period:])
            price_prior_high = max(closes[-2 * period:-period])
            mfi_recent_high = max(value for value in mfi_series[-period:] if not math.isnan(value))
            mfi_prior_high = max(value for value in mfi_series[-2 * period:-period] if not math.isnan(value))
            if price_recent_high > price_prior_high and mfi_recent_high < mfi_prior_high:
                divergence = "bearish"
            price_recent_low = min(closes[-period:])
            price_prior_low = min(closes[-2 * period:-period])
            mfi_recent_low = min(value for value in mfi_series[-period:] if not math.isnan(value))
            mfi_prior_low = min(value for value in mfi_series[-2 * period:-period] if not math.isnan(value))
            if price_recent_low < price_prior_low and mfi_recent_low > mfi_prior_low:
                divergence = "bullish"

        return {
            "status": "success",
            "data": {
                "mfi_series": mfi_series,
                "current_mfi": current_mfi,
                "zone": zone,
                "divergence_with_price": divergence
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"money_flow_index failed: {e}")
        _log_lesson(f"money_flow_index: {e}")
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
