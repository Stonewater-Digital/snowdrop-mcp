"""
Executive Summary: Internal models approach (Basel 2.5) market risk capital using VaR, stressed VaR, IRC, and CRM.
Inputs: var_10day (float), stressed_var_10day (float), incremental_risk_charge (float), comprehensive_risk_measure (float), multiplier (float)
Outputs: ima_capital (float), var_charge (float), stressed_charge (float), incremental_add_ons (dict)
MCP Tool Name: market_risk_ima_capital
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "market_risk_ima_capital",
    "description": "Calculates IMA capital: max(m * VaR, m * sVaR) + IRC + CRM per Basel 2.5.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "var_10day": {"type": "number", "description": "10-day VaR."},
            "stressed_var_10day": {"type": "number", "description": "10-day stressed VaR."},
            "incremental_risk_charge": {"type": "number", "description": "IRC add-on."},
            "comprehensive_risk_measure": {"type": "number", "description": "CRM add-on."},
            "multiplier": {"type": "number", "description": "Regulatory VaR multiplier (default 3).", "default": 3.0},
        },
        "required": [
            "var_10day",
            "stressed_var_10day",
            "incremental_risk_charge",
            "comprehensive_risk_measure",
        ],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "IMA capital output"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def market_risk_ima_capital(
    var_10day: float,
    stressed_var_10day: float,
    incremental_risk_charge: float,
    comprehensive_risk_measure: float,
    multiplier: float = 3.0,
    **_: Any,
) -> dict[str, Any]:
    try:
        var_charge = multiplier * var_10day
        stressed_charge = multiplier * stressed_var_10day
        base_charge = max(var_charge, stressed_charge)
        capital = base_charge + incremental_risk_charge + comprehensive_risk_measure
        data = {
            "ima_capital": round(capital, 2),
            "var_charge": round(var_charge, 2),
            "stressed_var_charge": round(stressed_charge, 2),
            "incremental_add_ons": {
                "irc": round(incremental_risk_charge, 2),
                "crm": round(comprehensive_risk_measure, 2),
            },
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"market_risk_ima_capital failed: {e}")
        _log_lesson(f"market_risk_ima_capital: {e}")
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
