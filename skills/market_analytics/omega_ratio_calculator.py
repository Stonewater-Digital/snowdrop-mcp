"""
Execuve Summary: Computes the Omega ratio, weighting gains above threshold versus losses below.
Inputs: returns (list[float]), threshold_return (float)
Outputs: omega_ratio (float), probability_of_gain (float), expected_gain (float), expected_loss (float), interpretation (str)
MCP Tool Name: omega_ratio_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "omega_ratio_calculator",
    "description": "Computes Omega = sum(max(r-threshold,0)) / sum(max(threshold-r,0)).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "returns": {"type": "array", "description": "Return series."},
            "threshold_return": {"type": "number", "description": "Target or hurdle return (decimal)."}
        },
        "required": ["returns", "threshold_return"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def omega_ratio_calculator(**kwargs: Any) -> dict:
    """Calculates Omega ratio and supporting stats."""
    try:
        returns = kwargs.get("returns")
        threshold = kwargs.get("threshold_return")
        if not isinstance(returns, list) or len(returns) == 0:
            raise ValueError("returns must be non-empty list")
        if not isinstance(threshold, (int, float)):
            raise ValueError("threshold_return must be numeric")

        gains = []
        losses = []
        win_count = 0
        for ret in returns:
            if not isinstance(ret, (int, float)):
                raise TypeError("returns must be numeric")
            diff = float(ret) - float(threshold)
            if diff >= 0:
                gains.append(diff)
                win_count += 1
            else:
                losses.append(-diff)
        expected_gain = sum(gains) / len(gains) if gains else 0.0
        expected_loss = sum(losses) / len(losses) if losses else 0.0
        denominator = sum(losses) if losses else math.inf
        omega_ratio = sum(gains) / denominator if denominator not in {0, math.inf} else math.inf
        probability_of_gain = win_count / len(returns)
        interpretation = "favorable" if omega_ratio > 1 else "unfavorable"

        return {
            "status": "success",
            "data": {
                "omega_ratio": omega_ratio,
                "probability_of_gain": probability_of_gain,
                "expected_gain": expected_gain,
                "expected_loss": expected_loss,
                "interpretation": interpretation
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"omega_ratio_calculator failed: {e}")
        _log_lesson(f"omega_ratio_calculator: {e}")
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
