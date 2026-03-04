"""Calculate historical Value at Risk (VaR) from a return series.

MCP Tool Name: value_at_risk_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "value_at_risk_calculator",
    "description": (
        "Calculates historical Value at Risk (VaR) at a given confidence level, "
        "representing the maximum expected loss over a period."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "returns": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of periodic returns as decimals.",
            },
            "confidence": {
                "type": "number",
                "description": "Confidence level (default 0.95 for 95%).",
            },
        },
        "required": ["returns"],
    },
}


def value_at_risk_calculator(
    returns: list[float], confidence: float = 0.95
) -> dict[str, Any]:
    """Calculate historical Value at Risk."""
    try:
        returns = [float(r) for r in returns]
        confidence = float(confidence)

        if len(returns) == 0:
            raise ValueError("returns must not be empty.")
        if not (0 < confidence < 1):
            raise ValueError("confidence must be between 0 and 1 (exclusive).")

        sorted_returns = sorted(returns)
        index = int((1 - confidence) * len(sorted_returns))
        index = max(0, min(index, len(sorted_returns) - 1))
        var = sorted_returns[index]

        return {
            "status": "ok",
            "data": {
                "var": round(var, 6),
                "var_pct": round(var * 100, 4),
                "confidence": confidence,
                "n_observations": len(returns),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
