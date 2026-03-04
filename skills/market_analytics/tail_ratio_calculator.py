"""
Execuve Summary: Measures tail ratio and distribution shape metrics.
Inputs: returns (list[float]), percentile (float)
Outputs: tail_ratio (float), right_tail (float), left_tail (float), skewness (float), kurtosis (float), fat_tail_warning (str)
MCP Tool Name: tail_ratio_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "tail_ratio_calculator",
    "description": "Calculates right-tail/left-tail ratio plus skewness and kurtosis for fat-tail detection.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "returns": {"type": "array", "description": "Return series."},
            "percentile": {"type": "number", "description": "Tail percentile (e.g., 5 for 5%%)."}
        },
        "required": ["returns", "percentile"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def tail_ratio_calculator(**kwargs: Any) -> dict:
    """Evaluates tail behavior via percentile comparisons and higher moments."""
    try:
        returns = kwargs.get("returns")
        percentile = kwargs.get("percentile")
        if not isinstance(returns, list) or len(returns) < 10:
            raise ValueError("returns must contain at least 10 observations")
        if not isinstance(percentile, (int, float)) or not 0 < percentile < 50:
            raise ValueError("percentile must be between 0 and 50")

        sorted_returns = sorted(float(r) for r in returns)
        lower_idx = max(0, int((percentile / 100) * len(sorted_returns)) - 1)
        upper_idx = min(len(sorted_returns) - 1, int((1 - percentile / 100) * len(sorted_returns)) - 1)
        left_tail = sorted_returns[lower_idx]
        right_tail = sorted_returns[upper_idx]
        tail_ratio = abs(right_tail) / abs(left_tail) if left_tail != 0 else math.inf

        mean_return = sum(sorted_returns) / len(sorted_returns)
        variance = sum((r - mean_return) ** 2 for r in sorted_returns) / len(sorted_returns)
        std_dev = math.sqrt(variance)
        skewness = (sum((r - mean_return) ** 3 for r in sorted_returns) / len(sorted_returns)) / (std_dev ** 3 if std_dev else 1)
        kurtosis = (sum((r - mean_return) ** 4 for r in sorted_returns) / len(sorted_returns)) / (std_dev ** 4 if std_dev else 1)
        excess_kurtosis = kurtosis - 3
        fat_tail_warning = "present" if excess_kurtosis > 1 else "normal"

        return {
            "status": "success",
            "data": {
                "tail_ratio": tail_ratio,
                "right_tail": right_tail,
                "left_tail": left_tail,
                "skewness": skewness,
                "kurtosis": kurtosis,
                "fat_tail_warning": fat_tail_warning
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"tail_ratio_calculator failed: {e}")
        _log_lesson(f"tail_ratio_calculator: {e}")
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
