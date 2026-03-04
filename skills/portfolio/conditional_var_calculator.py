"""Calculate Conditional Value at Risk (CVaR / Expected Shortfall).

MCP Tool Name: conditional_var_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "conditional_var_calculator",
    "description": (
        "Calculates Conditional Value at Risk (CVaR), also known as Expected "
        "Shortfall, the average loss beyond the VaR threshold."
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


def conditional_var_calculator(
    returns: list[float], confidence: float = 0.95
) -> dict[str, Any]:
    """Calculate Conditional Value at Risk (CVaR)."""
    try:
        import statistics

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

        tail = [r for r in sorted_returns if r <= var]
        if len(tail) == 0:
            cvar = var
        else:
            cvar = statistics.mean(tail)

        return {
            "status": "ok",
            "data": {
                "var": round(var, 6),
                "cvar": round(cvar, 6),
                "cvar_pct": round(cvar * 100, 4),
                "confidence": confidence,
                "n_tail_observations": len(tail),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
