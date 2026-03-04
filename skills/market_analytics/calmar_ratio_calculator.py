"""
Execuve Summary: Calculates the Calmar ratio (return divided by max drawdown).
Inputs: returns (list[float]), period_years (float)
Outputs: calmar_ratio (float), annualized_return (float), max_drawdown (float), recovery_time (int)
MCP Tool Name: calmar_ratio_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "calmar_ratio_calculator",
    "description": "Computes the Calmar ratio using cumulative returns and drawdown analysis.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "returns": {"type": "array", "description": "Periodic returns (decimal)."},
            "period_years": {"type": "number", "description": "Total time span of the series in years."}
        },
        "required": ["returns", "period_years"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"}
        },
        "required": ["status", "timestamp"]
    }
}


def calmar_ratio_calculator(**kwargs: Any) -> dict:
    """Calculates Calmar ratio = annualized return / max drawdown magnitude."""
    try:
        returns = kwargs.get("returns")
        period_years = kwargs.get("period_years")
        if not isinstance(returns, list) or len(returns) == 0:
            raise ValueError("returns must be non-empty list")
        if not isinstance(period_years, (int, float)) or period_years <= 0:
            raise ValueError("period_years must be positive number")

        equity_curve = [1.0]
        for ret in returns:
            if not isinstance(ret, (int, float)):
                raise TypeError("returns must be numeric")
            equity_curve.append(equity_curve[-1] * (1 + float(ret)))

        peaks = [equity_curve[0]]
        drawdowns = [0.0]
        recovery_time = 0
        current_recovery = 0
        max_drawdown = 0.0
        for value in equity_curve[1:]:
            peak = max(peaks[-1], value)
            peaks.append(peak)
            dd = (value - peak) / peak
            drawdowns.append(dd)
            if dd < 0:
                current_recovery += 1
            else:
                recovery_time = max(recovery_time, current_recovery)
                current_recovery = 0
            max_drawdown = min(max_drawdown, dd)
        recovery_time = max(recovery_time, current_recovery)

        total_return = equity_curve[-1] - 1
        annualized_return = (equity_curve[-1]) ** (1 / period_years) - 1
        if max_drawdown == 0:
            raise ZeroDivisionError("max drawdown is zero; Calmar undefined")
        calmar_ratio = annualized_return / abs(max_drawdown)

        return {
            "status": "success",
            "data": {
                "calmar_ratio": calmar_ratio,
                "annualized_return": annualized_return,
                "max_drawdown": max_drawdown,
                "recovery_time": recovery_time
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"calmar_ratio_calculator failed: {e}")
        _log_lesson(f"calmar_ratio_calculator: {e}")
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
