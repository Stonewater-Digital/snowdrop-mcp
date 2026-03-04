
"""
Executive Summary: Measures how stretched prices are versus realized value to flag profit-taking zones.
Inputs: market_cap (float), realized_cap (float)
Outputs: mvrv_ratio (float), zone (str), profit_loss_pct (float), cycle_position (str)
MCP Tool Name: mvrv_ratio_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "mvrv_ratio_calculator",
    "description": "Computes Market Value to Realized Value ratio to identify accumulation or euphoria regimes.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "market_cap": {
                "type": "number",
                "description": "Spot market capitalization for the asset in USD."
            },
            "realized_cap": {
                "type": "number",
                "description": "Realized capitalization derived from UTXO or cost-basis ledgers in USD."
            }
        },
        "required": ["market_cap", "realized_cap"]
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


def mvrv_ratio_calculator(**kwargs: Any) -> dict:
    """Calculates the MVRV ratio and classifies the market phase."""
    try:
        for field in ("market_cap", "realized_cap"):
            if field not in kwargs:
                raise ValueError(f"Missing required field {field}")
        market_cap = float(kwargs["market_cap"])
        realized_cap = float(kwargs["realized_cap"])
        if market_cap <= 0 or realized_cap <= 0:
            raise ValueError("market_cap and realized_cap must be positive numbers")
        mvrv_ratio = market_cap / realized_cap
        profit_loss_pct = max(-100.0, (market_cap - realized_cap) / realized_cap * 100)
        if mvrv_ratio < 1:
            zone = "accumulation"
        elif mvrv_ratio < 1.5:
            zone = "fair"
        elif mvrv_ratio < 3:
            zone = "distribution"
        else:
            zone = "euphoria"
        if mvrv_ratio < 0.8:
            cycle_position = "deep value"
        elif mvrv_ratio < 1.2:
            cycle_position = "early bull"
        elif mvrv_ratio < 2.5:
            cycle_position = "late bull"
        else:
            cycle_position = "blow-off risk"
        return {
            "status": "success",
            "data": {
                "mvrv_ratio": mvrv_ratio,
                "zone": zone,
                "profit_loss_pct": profit_loss_pct,
                "cycle_position": cycle_position
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"mvrv_ratio_calculator failed: {e}")
        _log_lesson(f"mvrv_ratio_calculator: {e}")
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
