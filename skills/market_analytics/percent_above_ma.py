"""
Execuve Summary: Computes the percentage of stocks trading above a chosen moving average.
Inputs: stock_closes_matrix (list[list[float]]), ma_period (int)
Outputs: pct_above_ma (float), breadth_signal (str), thrust_detected (bool), historical_percentile (float)
MCP Tool Name: percent_above_ma
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "percent_above_ma",
    "description": "Calculates % of symbols above their moving average to gauge breadth thrusts.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "stock_closes_matrix": {"type": "array", "description": "List of closing-price series per stock."},
            "ma_period": {"type": "integer", "description": "Moving-average lookback (e.g., 200)."}
        },
        "required": ["stock_closes_matrix", "ma_period"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def percent_above_ma(**kwargs: Any) -> dict:
    """Counts stocks above/below their moving average."""
    try:
        matrix = kwargs.get("stock_closes_matrix")
        ma_period = kwargs.get("ma_period")
        if not isinstance(matrix, list) or len(matrix) == 0:
            raise ValueError("stock_closes_matrix must be non-empty list")
        if not isinstance(ma_period, int) or ma_period <= 1:
            raise ValueError("ma_period must be integer > 1")

        above = 0
        valid = 0
        for series in matrix:
            if not isinstance(series, list) or len(series) < ma_period:
                continue
            valid += 1
            ma = sum(series[-ma_period:]) / ma_period
            if series[-1] > ma:
                above += 1
        if valid == 0:
            raise ValueError("no series long enough for ma_period")
        pct_above = above / valid
        thrust_detected = pct_above >= 0.9 or pct_above <= 0.1
        if pct_above >= 0.8:
            signal = "breadth_thrust"
        elif pct_above <= 0.2:
            signal = "breadth_washout"
        else:
            signal = "neutral"
        historical_percentile = pct_above * 100

        return {
            "status": "success",
            "data": {
                "pct_above_ma": pct_above,
                "breadth_signal": signal,
                "thrust_detected": thrust_detected,
                "historical_percentile": historical_percentile
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"percent_above_ma failed: {e}")
        _log_lesson(f"percent_above_ma: {e}")
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
