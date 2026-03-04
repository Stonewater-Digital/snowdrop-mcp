"""
Executive Summary: Marks total return swaps by comparing asset performance and funding legs over the accrual period.
Inputs: previous_price (float), current_price (float), notional (float), funding_rate (float), funding_spread_bp (float), days_in_period (float), dividend_yield (float)
Outputs: status (str), timestamp (str), data (dict)
MCP Tool Name: total_return_swap_pricer
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "total_return_swap_pricer",
    "description": (
        "Computes total-return swap mark-to-market using standard equity TRS conventions: "
        "asset return minus funded leg with spread and dividends."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "previous_price": {
                "type": "number",
                "description": "Reference asset price at the start of the accrual period."
            },
            "current_price": {
                "type": "number",
                "description": "Reference asset price at valuation."
            },
            "notional": {
                "type": "number",
                "description": "Swap notional representing the financed position."
            },
            "funding_rate": {
                "type": "number",
                "description": "Annualized floating funding rate (decimal)."
            },
            "funding_spread_bp": {
                "type": "number",
                "description": "Dealer spread over funding curve in basis points."
            },
            "days_in_period": {
                "type": "number",
                "description": "Accrual days used for day-count conversion (ACT/360)."
            },
            "dividend_yield": {
                "type": "number",
                "description": "Continuous dividend yield of the reference asset (decimal)."
            }
        },
        "required": [
            "previous_price",
            "current_price",
            "notional",
            "funding_rate",
            "funding_spread_bp",
            "days_in_period",
            "dividend_yield"
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


def total_return_swap_pricer(**kwargs: Any) -> dict[str, Any]:
    try:
        prev_price = float(kwargs["previous_price"])
        current_price = float(kwargs["current_price"])
        notional = float(kwargs["notional"])
        funding_rate = float(kwargs["funding_rate"])
        spread = float(kwargs["funding_spread_bp"]) / 10000.0
        accrual_days = float(kwargs["days_in_period"])
        dividend_yield = float(kwargs["dividend_yield"])

        if prev_price <= 0 or accrual_days <= 0:
            raise ValueError("previous_price and days_in_period must be positive")

        accrual_fraction = accrual_days / 360.0
        asset_return = (current_price - prev_price) / prev_price + dividend_yield * accrual_fraction
        equity_leg = asset_return * notional
        funding_leg = notional * (funding_rate + spread) * accrual_fraction
        net_pv = equity_leg - funding_leg
        breakeven_spread = (asset_return / max(accrual_fraction, 1e-8) - funding_rate) * 10000.0

        data = {
            "asset_return": asset_return,
            "equity_leg_cashflow": equity_leg,
            "funding_leg_cashflow": funding_leg,
            "net_present_value": net_pv,
            "breakeven_spread_bp": breakeven_spread,
            "accrual_fraction": accrual_fraction
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError, KeyError) as e:
        logger.error("total_return_swap_pricer failed: %s", e)
        _log_lesson(f"total_return_swap_pricer: {e}")
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
