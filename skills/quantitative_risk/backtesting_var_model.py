"""
Executive Summary: Basel traffic-light VaR backtesting with Kupiec proportion of failures test.
Inputs: predicted_var (list[float]), actual_pnl (list[float]), confidence_level (float)
Outputs: exceptions (int), traffic_light_zone (str), kupiec_statistic (float), p_value (float)
MCP Tool Name: backtesting_var_model
"""
import logging
from datetime import datetime, timezone
from math import comb, log
from typing import Any, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "backtesting_var_model",
    "description": "Evaluates VaR performance using Basel traffic light thresholds and Kupiec LR test.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "predicted_var": {
                "type": "array",
                "description": "Daily VaR predictions (positive numbers).",
                "items": {"type": "number"},
            },
            "actual_pnl": {
                "type": "array",
                "description": "Actual P&L observations aligned with predicted VaR (negative=loss).",
                "items": {"type": "number"},
            },
            "confidence_level": {
                "type": "number",
                "description": "Confidence level used in VaR calibration.",
            },
        },
        "required": ["predicted_var", "actual_pnl", "confidence_level"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "Backtest metrics"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def backtesting_var_model(
    predicted_var: List[float],
    actual_pnl: List[float],
    confidence_level: float,
    **_: Any,
) -> dict[str, Any]:
    try:
        if len(predicted_var) != len(actual_pnl):
            raise ValueError("predicted_var and actual_pnl lengths must match")
        if not (0 < confidence_level < 1):
            raise ValueError("confidence_level must be in (0,1)")
        violations = [1 for var, pnl in zip(predicted_var, actual_pnl) if pnl < -abs(var)]
        num_exceptions = sum(violations)
        n = len(predicted_var)
        if num_exceptions <= 4:
            zone = "green"
        elif num_exceptions <= 9:
            zone = "yellow"
        else:
            zone = "red"
        expected_rate = 1 - confidence_level
        failures = num_exceptions
        successes = n - failures
        if failures == 0 or failures == n:
            likelihood_ratio = 0.0
        else:
            likelihood_ratio = -2 * (
                log(((1 - expected_rate) ** successes) * (expected_rate ** failures))
                - log(((1 - failures / n) ** successes) * ((failures / n) ** failures))
            )
        p_value = 1 - min(1, comb(n, failures) * (expected_rate**failures) * ((1 - expected_rate) ** successes))
        data = {
            "exceptions": num_exceptions,
            "total_observations": n,
            "traffic_light_zone": zone,
            "kupiec_statistic": round(likelihood_ratio, 4),
            "kupiec_p_value": round(p_value, 6),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"backtesting_var_model failed: {e}")
        _log_lesson(f"backtesting_var_model: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as handle:
            handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
