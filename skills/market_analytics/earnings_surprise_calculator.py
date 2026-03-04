"""
Execuve Summary: Quantifies earnings surprise magnitude and post-announcement drift signal.
Inputs: actual_eps (float), consensus_estimate (float), stock_price_before (float), stock_price_after (float)
Outputs: surprise_pct (float), surprise_direction (str), standardized_unexpected_earnings (float), implied_drift_signal (str)
MCP Tool Name: earnings_surprise_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "earnings_surprise_calculator",
    "description": "Calculates EPS surprise percentage, SUE proxy, and price-drift implications (PEAD).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "actual_eps": {"type": "number", "description": "Reported EPS."},
            "consensus_estimate": {"type": "number", "description": "Consensus EPS estimate."},
            "stock_price_before": {"type": "number", "description": "Price before earnings."},
            "stock_price_after": {"type": "number", "description": "Price after earnings."}
        },
        "required": ["actual_eps", "consensus_estimate", "stock_price_before", "stock_price_after"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def earnings_surprise_calculator(**kwargs: Any) -> dict:
    """Evaluates EPS surprise and post-earnings drift signal."""
    try:
        actual = kwargs.get("actual_eps")
        estimate = kwargs.get("consensus_estimate")
        price_before = kwargs.get("stock_price_before")
        price_after = kwargs.get("stock_price_after")
        for label, value in (("actual_eps", actual), ("consensus_estimate", estimate), ("stock_price_before", price_before), ("stock_price_after", price_after)):
            if not isinstance(value, (int, float)):
                raise ValueError(f"{label} must be numeric")
        if estimate == 0:
            raise ZeroDivisionError("consensus_estimate cannot be zero")

        surprise_pct = (actual - estimate) / abs(estimate)
        direction = "positive" if surprise_pct > 0 else ("negative" if surprise_pct < 0 else "inline")
        sue = surprise_pct / 0.05  # assume 5% SD baseline
        drift = (price_after - price_before) / price_before if price_before else 0
        if direction == "positive" and drift > 0:
            pead_signal = "momentum_follow_through"
        elif direction == "positive" and drift < 0:
            pead_signal = "mean_reversion_risk"
        elif direction == "negative" and drift < 0:
            pead_signal = "downside_confirmation"
        else:
            pead_signal = "uncertain"

        return {
            "status": "success",
            "data": {
                "surprise_pct": surprise_pct,
                "surprise_direction": direction,
                "standardized_unexpected_earnings": sue,
                "implied_drift_signal": pead_signal
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"earnings_surprise_calculator failed: {e}")
        _log_lesson(f"earnings_surprise_calculator: {e}")
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
