"""
Execuve Summary: Computes various downside-focused metrics relative to a MAR.
Inputs: returns (list[float]), mar (float)
Outputs: downside_deviation (float), upside_potential_ratio (float), gain_loss_ratio (float), bernardo_ledoit_ratio (float)
MCP Tool Name: downside_risk_metrics
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "downside_risk_metrics",
    "description": "Computes downside deviation, upside potential ratio, gain/loss ratio, and Bernardo-Ledoit ratio.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "returns": {"type": "array", "description": "Return series."},
            "mar": {"type": "number", "description": "Minimum acceptable return (MAR)."}
        },
        "required": ["returns", "mar"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def downside_risk_metrics(**kwargs: Any) -> dict:
    """Calculates multiple downside-oriented performance ratios."""
    try:
        returns = kwargs.get("returns")
        mar = kwargs.get("mar")
        if not isinstance(returns, list) or len(returns) == 0:
            raise ValueError("returns must be non-empty list")
        if not isinstance(mar, (int, float)):
            raise ValueError("mar must be numeric")

        downside_diff = [max(mar - float(r), 0) for r in returns]
        upside_diff = [max(float(r) - mar, 0) for r in returns]
        downside_deviation = math.sqrt(sum(val ** 2 for val in downside_diff) / len(downside_diff))
        upside_potential = sum(upside_diff) / len(upside_diff)
        upside_potential_ratio = upside_potential / downside_deviation if downside_deviation else math.inf
        gains = [max(float(r), 0) for r in returns]
        losses = [min(float(r), 0) for r in returns]
        gain_loss_ratio = (sum(gains) / abs(sum(losses))) if sum(losses) != 0 else math.inf
        avg_gain = sum(gains) / max(1, len([g for g in gains if g > 0]))
        avg_loss = abs(sum(losses) / max(1, len([l for l in losses if l < 0])))
        bernardo_ledoit_ratio = avg_gain / avg_loss if avg_loss != 0 else math.inf

        return {
            "status": "success",
            "data": {
                "downside_deviation": downside_deviation,
                "upside_potential_ratio": upside_potential_ratio,
                "gain_loss_ratio": gain_loss_ratio,
                "bernardo_ledoit_ratio": bernardo_ledoit_ratio
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"downside_risk_metrics failed: {e}")
        _log_lesson(f"downside_risk_metrics: {e}")
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
