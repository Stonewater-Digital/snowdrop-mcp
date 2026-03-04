"""
Execuve Summary: Converts local asset returns into base-currency performance.
Inputs: local_returns (list[float]), fx_rates (list[dict]), base_currency (str)
Outputs: local_return (float), fx_return (float), total_return_in_base (float), fx_contribution_pct (float), hedged_vs_unhedged (dict)
MCP Tool Name: currency_adjusted_return
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "currency_adjusted_return",
    "description": "Adjusts local returns for FX moves to measure base-currency performance.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "local_returns": {"type": "array", "description": "Local currency returns (decimal)."},
            "fx_rates": {"type": "array", "description": "FX rates as list of {date_idx, rate}."},
            "base_currency": {"type": "string", "description": "Reporting currency."}
        },
        "required": ["local_returns", "fx_rates", "base_currency"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def currency_adjusted_return(**kwargs: Any) -> dict:
    """Calculates base-currency total return and FX contribution."""
    try:
        local_returns = kwargs.get("local_returns")
        fx_rates = kwargs.get("fx_rates")
        base_currency = kwargs.get("base_currency")
        if not isinstance(local_returns, list) or len(local_returns) == 0:
            raise ValueError("local_returns must be non-empty list")
        if not isinstance(fx_rates, list) or len(fx_rates) < 2:
            raise ValueError("fx_rates must include at least start and end rates")
        if not isinstance(base_currency, str):
            raise ValueError("base_currency must be string")

        local_growth = 1.0
        for ret in local_returns:
            if not isinstance(ret, (int, float)):
                raise TypeError("local_returns must be numeric")
            local_growth *= (1 + ret)
        local_return = local_growth - 1

        rates = [float(entry.get("rate")) if isinstance(entry, dict) else float(entry) for entry in fx_rates]
        fx_return = rates[-1] / rates[0] - 1
        total_return = (1 + local_return) * (1 + fx_return) - 1
        fx_contribution = fx_return / (1 + total_return) if (1 + total_return) != 0 else 0
        hedged_vs_unhedged = {
            "hedged": local_return,
            "unhedged": total_return
        }

        return {
            "status": "success",
            "data": {
                "local_return": local_return,
                "fx_return": fx_return,
                "total_return_in_base": total_return,
                "fx_contribution_pct": fx_contribution,
                "hedged_vs_unhedged": hedged_vs_unhedged,
                "base_currency": base_currency
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"currency_adjusted_return failed: {e}")
        _log_lesson(f"currency_adjusted_return: {e}")
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
