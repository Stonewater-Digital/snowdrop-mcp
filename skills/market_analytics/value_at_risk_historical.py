"""
Execuve Summary: Computes historical simulation VaR and expected shortfall.
Inputs: returns (list[float]), confidence_level (float), horizon_days (int)
Outputs: var_amount (float), var_pct (float), expected_shortfall (float), worst_n_days (list[float]), backtest_violations (int)
MCP Tool Name: value_at_risk_historical
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "value_at_risk_historical",
    "description": "Computes historical VaR by sampling past returns and scaling by the desired horizon.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "returns": {"type": "array", "description": "Historical returns (decimal)."},
            "confidence_level": {"type": "number", "description": "Confidence level (0-1)."},
            "horizon_days": {"type": "integer", "description": "Holding period in days."}
        },
        "required": ["returns", "confidence_level", "horizon_days"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def value_at_risk_historical(**kwargs: Any) -> dict:
    """Takes empirical quantile of returns to estimate VaR and ES."""
    try:
        returns = kwargs.get("returns")
        confidence = kwargs.get("confidence_level")
        horizon = kwargs.get("horizon_days")
        if not isinstance(returns, list) or len(returns) < 10:
            raise ValueError("returns must be list with at least 10 observations")
        if not isinstance(confidence, (int, float)) or not 0.5 < confidence < 0.999:
            raise ValueError("confidence_level must be between 0.5 and 0.999")
        if not isinstance(horizon, int) or horizon <= 0:
            raise ValueError("horizon_days must be positive integer")

        sorted_returns = sorted(float(r) for r in returns)
        index = max(0, int((1 - confidence) * len(sorted_returns)) - 1)
        quantile_return = sorted_returns[index]
        var_pct = -quantile_return * math.sqrt(horizon)
        tail_losses = sorted_returns[: index + 1]
        expected_shortfall = -sum(tail_losses) / len(tail_losses) * math.sqrt(horizon)
        worst_n_days = sorted_returns[: min(5, len(sorted_returns))]
        backtest_violations = sum(1 for r in returns if r < -var_pct)

        return {
            "status": "success",
            "data": {
                "var_amount": var_pct,
                "var_pct": var_pct,
                "expected_shortfall": expected_shortfall,
                "worst_n_days": worst_n_days,
                "backtest_violations": backtest_violations
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"value_at_risk_historical failed: {e}")
        _log_lesson(f"value_at_risk_historical: {e}")
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
