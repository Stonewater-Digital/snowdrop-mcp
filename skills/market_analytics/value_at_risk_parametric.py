"""
Execuve Summary: Calculates parametric (Gaussian) Value at Risk.
Inputs: returns (list[float]), confidence_level (float), horizon_days (int)
Outputs: var_amount (float), var_pct (float), expected_shortfall (float), interpretation (str)
MCP Tool Name: value_at_risk_parametric
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

Z_LOOKUP = {
    0.90: 1.2816,
    0.95: 1.6449,
    0.975: 1.96,
    0.99: 2.3263,
    0.995: 2.5758
}

TOOL_META = {
    "name": "value_at_risk_parametric",
    "description": "Computes Gaussian VaR and expected shortfall over a specified horizon.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "returns": {"type": "array", "description": "Historical returns (decimal)."},
            "confidence_level": {"type": "number", "description": "Confidence level between 0 and 1."},
            "horizon_days": {"type": "integer", "description": "VaR horizon in days."}
        },
        "required": ["returns", "confidence_level", "horizon_days"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def value_at_risk_parametric(**kwargs: Any) -> dict:
    """Applies the Gaussian VaR formula VaR = -(μ * H - z * σ * sqrt(H))."""
    try:
        returns = kwargs.get("returns")
        confidence = kwargs.get("confidence_level")
        horizon = kwargs.get("horizon_days")
        if not isinstance(returns, list) or len(returns) < 2:
            raise ValueError("returns must be list with at least two observations")
        if not isinstance(confidence, (int, float)) or not 0.5 < confidence < 0.999:
            raise ValueError("confidence_level must be between 0.5 and 0.999")
        if not isinstance(horizon, int) or horizon <= 0:
            raise ValueError("horizon_days must be positive integer")

        returns_clean = [float(r) for r in returns]
        mean_return = sum(returns_clean) / len(returns_clean)
        variance = sum((r - mean_return) ** 2 for r in returns_clean) / (len(returns_clean) - 1)
        std_dev = math.sqrt(variance)

        z_score = _z_for_confidence(confidence)
        var_pct = -(mean_return * horizon - z_score * std_dev * math.sqrt(horizon))
        var_amount = var_pct
        pdf_at_z = (1 / math.sqrt(2 * math.pi)) * math.exp(-0.5 * z_score ** 2)
        expected_shortfall = var_pct + (std_dev * math.sqrt(horizon) * pdf_at_z) / (1 - confidence)

        if var_pct <= 0:
            interpretation = "insufficient_volatility"
        elif var_pct < 0.02:
            interpretation = "low_risk"
        elif var_pct < 0.05:
            interpretation = "moderate_risk"
        else:
            interpretation = "high_risk"

        return {
            "status": "success",
            "data": {
                "var_amount": var_amount,
                "var_pct": var_pct,
                "expected_shortfall": expected_shortfall,
                "interpretation": interpretation
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"value_at_risk_parametric failed: {e}")
        _log_lesson(f"value_at_risk_parametric: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _z_for_confidence(confidence: float) -> float:
    closest = min(Z_LOOKUP.keys(), key=lambda key: abs(key - confidence))
    return Z_LOOKUP[closest]


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
