
"""
Executive Summary: Evaluates valuation stretch by comparing network value with transaction throughput.
Inputs: market_cap (float), daily_transaction_volume_usd (float), smoothing_period (int)
Outputs: nvt_ratio (float), nvt_signal (float), valuation_zone (str), historical_percentile_note (str)
MCP Tool Name: nvt_ratio_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "nvt_ratio_calculator",
    "description": "Computes Willy Woo's Network Value to Transactions ratio with smoothing to classify valuation zones.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "market_cap": {
                "type": "number",
                "description": "Total network market capitalization in USD."
            },
            "daily_transaction_volume_usd": {
                "type": "number",
                "description": "Daily on-chain transaction volume settled on the network, denominated in USD."
            },
            "smoothing_period": {
                "type": "number",
                "description": "Number of days for the exponential smoothing factor (minimum 1)."
            }
        },
        "required": ["market_cap", "daily_transaction_volume_usd", "smoothing_period"]
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


def nvt_ratio_calculator(**kwargs: Any) -> dict:
    """Computes NVT and smoothed signals following Willy Woo's methodology."""
    try:
        for field in ("market_cap", "daily_transaction_volume_usd", "smoothing_period"):
            if field not in kwargs:
                raise ValueError(f"Missing required field {field}")
        market_cap = float(kwargs["market_cap"])
        tx_volume = float(kwargs["daily_transaction_volume_usd"])
        smoothing_period = int(kwargs["smoothing_period"])
        if market_cap <= 0 or tx_volume <= 0:
            raise ValueError("market_cap and daily_transaction_volume_usd must be positive")
        if smoothing_period <= 0:
            raise ValueError("smoothing_period must be positive")
        nvt_ratio = market_cap / tx_volume
        alpha = 2 / (smoothing_period + 1)
        nvt_signal = nvt_ratio * alpha
        if nvt_ratio < 30:
            valuation_zone = "undervalued"
        elif nvt_ratio < 70:
            valuation_zone = "fair"
        else:
            valuation_zone = "overvalued"
        percentiles = [15, 35, 60, 100]
        bands = [20, 50, 90]
        for pct, band in zip(percentiles, bands):
            if nvt_ratio < band:
                historical_percentile_note = f"Approximately top {pct}% of historical NVT readings."
                break
        else:
            historical_percentile_note = "Extreme valuation territory historically (<10% of observations)."
        return {
            "status": "success",
            "data": {
                "nvt_ratio": nvt_ratio,
                "nvt_signal": nvt_signal,
                "valuation_zone": valuation_zone,
                "historical_percentile_note": historical_percentile_note
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"nvt_ratio_calculator failed: {e}")
        _log_lesson(f"nvt_ratio_calculator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as file:
            file.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\\n")
    except OSError:
        pass
