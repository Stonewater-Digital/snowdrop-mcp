"""
Executive Smary: Computes core liquidity, leverage, and profitability ratios from financial statements.
Inputs: balance_sheet (dict), income_statement (dict)
Outputs: current_ratio (float), quick_ratio (float), debt_to_equity (float), gross_margin (float), net_margin (float), roe (float), roa (float), asset_turnover (float), inventory_turnover (float)
MCP Tool Name: financial_ratio_analyzer
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "financial_ratio_analyzer",
    "description": (
        "Calculates common liquidity, leverage, and profitability ratios using provided "
        "balance sheet and income statement figures."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "balance_sheet": {
                "type": "object",
                "description": "Dictionary containing current_assets, inventory, current_liabilities, total_liabilities, shareholders_equity, total_assets.",
            },
            "income_statement": {
                "type": "object",
                "description": "Dictionary containing revenue, gross_profit, net_income, cogs.",
            },
        },
        "required": ["balance_sheet", "income_statement"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"},
        },
        "required": ["status", "timestamp"],
    },
}


def financial_ratio_analyzer(**kwargs: Any) -> dict:
    """Compute standard liquidity, leverage, and profitability ratios."""
    try:
        bs: Dict[str, float] = kwargs["balance_sheet"]
        isheet: Dict[str, float] = kwargs["income_statement"]

        current_assets = float(bs["current_assets"])
        inventory = float(bs.get("inventory", 0.0))
        current_liabilities = float(bs["current_liabilities"])
        total_liabilities = float(bs["total_liabilities"])
        shareholders_equity = float(bs["shareholders_equity"])
        total_assets = float(bs["total_assets"])

        revenue = float(isheet["revenue"])
        gross_profit = float(isheet.get("gross_profit", revenue - float(isheet.get("cogs", 0.0))))
        net_income = float(isheet["net_income"])
        cogs = float(isheet.get("cogs", revenue - gross_profit))

        current_ratio = current_assets / current_liabilities if current_liabilities else float("inf")
        quick_ratio = (current_assets - inventory) / current_liabilities if current_liabilities else float("inf")
        debt_to_equity = total_liabilities / shareholders_equity if shareholders_equity else float("inf")
        gross_margin = gross_profit / revenue if revenue else 0.0
        net_margin = net_income / revenue if revenue else 0.0
        roe = net_income / shareholders_equity if shareholders_equity else 0.0
        roa = net_income / total_assets if total_assets else 0.0
        asset_turnover = revenue / total_assets if total_assets else 0.0
        inventory_turnover = cogs / inventory if inventory else float("inf")

        return {
            "status": "success",
            "data": {
                "current_ratio": current_ratio,
                "quick_ratio": quick_ratio,
                "debt_to_equity": debt_to_equity,
                "gross_margin": gross_margin,
                "net_margin": net_margin,
                "roe": roe,
                "roa": roa,
                "asset_turnover": asset_turnover,
                "inventory_turnover": inventory_turnover,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError, KeyError) as e:
        logger.error(f"financial_ratio_analyzer failed: {e}")
        _log_lesson(f"financial_ratio_analyzer: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
