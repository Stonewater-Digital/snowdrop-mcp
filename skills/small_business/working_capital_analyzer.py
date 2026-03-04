"""
Executive Smary: Calculates working capital metrics and the cash conversion cycle.
Inputs: accounts_receivable (float), inventory (float), accounts_payable (float), daily_revenue (float), daily_cogs (float)
Outputs: dso (float), dio (float), dpo (float), cash_conversion_cycle (float), working_capital (float), working_capital_ratio (float), improvement_suggestions (list)
MCP Tool Name: working_capital_analyzer
"""
import logging
from datetime import datetime, timezone
from typing import Any, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "working_capital_analyzer",
    "description": (
        "Computes days sales outstanding, inventory days, days payable outstanding, cash "
        "conversion cycle, and highlights improvement opportunities."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "accounts_receivable": {
                "type": "number",
                "description": "Current accounts receivable balance.",
            },
            "inventory": {"type": "number", "description": "Inventory balance."},
            "accounts_payable": {"type": "number", "description": "Accounts payable balance."},
            "daily_revenue": {"type": "number", "description": "Average daily revenue."},
            "daily_cogs": {"type": "number", "description": "Average daily cost of goods sold."},
        },
        "required": [
            "accounts_receivable",
            "inventory",
            "accounts_payable",
            "daily_revenue",
            "daily_cogs",
        ],
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


def working_capital_analyzer(**kwargs: Any) -> dict:
    """Compute working capital metrics and improvement recommendations."""
    try:
        ar = float(kwargs["accounts_receivable"])
        inventory = float(kwargs["inventory"])
        ap = float(kwargs["accounts_payable"])
        daily_revenue = float(kwargs["daily_revenue"])
        daily_cogs = float(kwargs["daily_cogs"])

        dso = ar / daily_revenue if daily_revenue else float("inf")
        dio = inventory / daily_cogs if daily_cogs else float("inf")
        dpo = ap / daily_cogs if daily_cogs else float("inf")
        ccc = dso + dio - dpo
        working_capital = ar + inventory - ap
        working_capital_ratio = (ar + inventory) / ap if ap else float("inf")

        suggestions: List[str] = []
        if dso > 45:
            suggestions.append("Tighten receivables collections to reduce DSO.")
        if dio > 60:
            suggestions.append("Optimize inventory turns via demand planning.")
        if dpo < 30:
            suggestions.append("Extend supplier payment terms to improve DPO.")

        return {
            "status": "success",
            "data": {
                "dso": dso,
                "dio": dio,
                "dpo": dpo,
                "cash_conversion_cycle": ccc,
                "working_capital": working_capital,
                "working_capital_ratio": working_capital_ratio,
                "improvement_suggestions": suggestions,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"working_capital_analyzer failed: {e}")
        _log_lesson(f"working_capital_analyzer: {e}")
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
