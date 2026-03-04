"""
Executive Summary: Basel III leverage ratio comparing Tier 1 capital to total exposure measure including derivatives and SFTs.
Inputs: tier1_capital (float), on_balance_exposures (float), derivative_exposures (float), sft_exposures (float), off_balance_items (float)
Outputs: leverage_ratio (float), exposure_measure (float), compliance (str)
MCP Tool Name: leverage_ratio_calculator
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "leverage_ratio_calculator",
    "description": "Computes Basel leverage ratio including SA-CCR derivative add-ons and securities financing exposures.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "tier1_capital": {"type": "number", "description": "Tier 1 capital in base currency."},
            "on_balance_exposures": {"type": "number", "description": "Total assets net of regulatory adjustments."},
            "derivative_exposures": {"type": "number", "description": "Replacement cost plus PFE from SA-CCR."},
            "sft_exposures": {"type": "number", "description": "Exposure measure for securities financing transactions."},
            "off_balance_items": {"type": "number", "description": "Credit conversion amount for off-balance sheet items."},
        },
        "required": [
            "tier1_capital",
            "on_balance_exposures",
            "derivative_exposures",
            "sft_exposures",
            "off_balance_items",
        ],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "Leverage ratio outputs"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def leverage_ratio_calculator(
    tier1_capital: float,
    on_balance_exposures: float,
    derivative_exposures: float,
    sft_exposures: float,
    off_balance_items: float,
    minimum_ratio_pct: float = 3.0,
    **_: Any,
) -> dict[str, Any]:
    try:
        exposure_measure = (
            on_balance_exposures + derivative_exposures + sft_exposures + off_balance_items
        )
        if exposure_measure <= 0:
            raise ValueError("Exposure measure must be positive")
        ratio = tier1_capital / exposure_measure
        compliance = "compliant" if ratio * 100 >= minimum_ratio_pct else "breach"
        data = {
            "leverage_ratio_pct": round(ratio * 100, 2),
            "exposure_measure": round(exposure_measure, 2),
            "tier1_capital": round(tier1_capital, 2),
            "minimum_ratio_pct": minimum_ratio_pct,
            "compliance": compliance,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"leverage_ratio_calculator failed: {e}")
        _log_lesson(f"leverage_ratio_calculator: {e}")
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
