"""
Executive Summary: Measures carry and roll cost when moving between on-the-run and off-the-run CDS indices.
Inputs: on_the_run_spread_bp (float), off_the_run_spread_bp (float), time_to_maturity_years (float), roll_period_years (float), notional (float), discount_rate (float)
Outputs: status (str), timestamp (str), data (dict)
MCP Tool Name: cds_index_roll_cost
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "cds_index_roll_cost",
    "description": (
        "Computes CDS index roll cost by comparing on/off-the-run spreads and PV01 carry over "
        "the roll period, following standard index arbitrage analytics."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "on_the_run_spread_bp": {
                "type": "number",
                "description": "Current on-the-run index spread in basis points."
            },
            "off_the_run_spread_bp": {
                "type": "number",
                "description": "Off-the-run index spread in basis points."
            },
            "time_to_maturity_years": {
                "type": "number",
                "description": "Remaining maturity for the off-the-run contract in years."
            },
            "roll_period_years": {
                "type": "number",
                "description": "Time until the next roll date in years."
            },
            "notional": {
                "type": "number",
                "description": "Index notional in currency units."
            },
            "discount_rate": {
                "type": "number",
                "description": "Continuously compounded discount rate for PV."
            }
        },
        "required": [
            "on_the_run_spread_bp",
            "off_the_run_spread_bp",
            "time_to_maturity_years",
            "roll_period_years",
            "notional",
            "discount_rate"
        ]
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


def cds_index_roll_cost(**kwargs: Any) -> dict[str, Any]:
    try:
        on_spread = float(kwargs["on_the_run_spread_bp"])
        off_spread = float(kwargs["off_the_run_spread_bp"])
        maturity = float(kwargs["time_to_maturity_years"])
        roll_period = float(kwargs["roll_period_years"])
        notional = float(kwargs["notional"])
        discount_rate = float(kwargs["discount_rate"])
        if roll_period <= 0 or maturity <= 0:
            raise ValueError("time inputs must be positive")

        spread_diff = off_spread - on_spread
        annualized_roll = spread_diff * roll_period / maturity
        pv01 = roll_period * math.exp(-discount_rate * roll_period)
        carry_pnl = pv01 * spread_diff / 10000.0 * notional
        discount_factor = math.exp(-discount_rate * roll_period)

        data = {
            "spread_difference_bp": spread_diff,
            "annualized_roll_bp": annualized_roll,
            "carry_pnl": carry_pnl,
            "discount_factor": discount_factor,
            "pv01_years": pv01,
            "net_roll_cost_bp": annualized_roll - spread_diff
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError, KeyError) as e:
        logger.error("cds_index_roll_cost failed: %s", e)
        _log_lesson(f"cds_index_roll_cost: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as file:
            file.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
