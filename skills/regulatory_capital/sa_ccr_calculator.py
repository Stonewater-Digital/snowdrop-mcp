"""
Executive Summary: SA-CCR exposure at default calculation using replacement cost and PFE add-ons.
Inputs: trades (list[dict]), collateral (float), alpha_multiplier (float)
Outputs: ead (float), replacement_cost (float), pfe_add_on (float), alpha (float)
MCP Tool Name: sa_ccr_calculator
"""
import logging
from datetime import datetime, timezone
from typing import Any, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "sa_ccr_calculator",
    "description": "Simplified SA-CCR calculation: EAD = alpha * (RC + PFE).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "trades": {
                "type": "array",
                "description": "Trades with MtM and add-on parameters.",
                "items": {
                    "type": "object",
                    "properties": {
                        "mtm": {"type": "number", "description": "Mark-to-market of the trade"},
                        "notional": {"type": "number", "description": "Trade notional"},
                        "add_on_factor_pct": {"type": "number", "description": "Asset-class add-on factor %"},
                    },
                    "required": ["mtm", "notional", "add_on_factor_pct"],
                },
            },
            "collateral": {"type": "number", "description": "Collateral held against the netting set."},
            "alpha_multiplier": {
                "type": "number",
                "description": "Basel alpha multiplier (default 1.4).",
                "default": 1.4,
            },
        },
        "required": ["trades", "collateral"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "SA-CCR outputs"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def sa_ccr_calculator(
    trades: List[dict[str, Any]],
    collateral: float,
    alpha_multiplier: float = 1.4,
    **_: Any,
) -> dict[str, Any]:
    try:
        if not trades:
            raise ValueError("trades required")
        replacement_cost = sum(max(trade["mtm"], 0.0) for trade in trades) - collateral
        replacement_cost = max(replacement_cost, 0.0)
        pfe = sum(trade["notional"] * trade["add_on_factor_pct"] / 100.0 for trade in trades)
        ead = alpha_multiplier * (replacement_cost + pfe)
        data = {
            "replacement_cost": round(replacement_cost, 2),
            "pfe_add_on": round(pfe, 2),
            "ead": round(ead, 2),
            "alpha": alpha_multiplier,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"sa_ccr_calculator failed: {e}")
        _log_lesson(f"sa_ccr_calculator: {e}")
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
