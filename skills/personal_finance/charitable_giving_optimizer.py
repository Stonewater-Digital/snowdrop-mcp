"""
Executive Smary: Optimizes charitable deductions for cash vs appreciated assets limits.
Inputs: cash_donations (float), appreciated_assets (list), agi (float), filing_status (str)
Outputs: total_deduction (float), tax_savings (float), agi_limitation (dict), carryforward (float), optimal_strategy (str)
MCP Tool Name: charitable_giving_optimizer
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

logger = logging.getLogger("snowdrop.skills")

BRACKETS = {
    "single": [
        (0, 0.10),
        (11600, 0.12),
        (47150, 0.22),
        (100525, 0.24),
        (191950, 0.32),
        (243725, 0.35),
        (609350, 0.37),
    ],
    "mfj": [
        (0, 0.10),
        (23200, 0.12),
        (94300, 0.22),
        (201050, 0.24),
        (383900, 0.32),
        (487450, 0.35),
        (731200, 0.37),
    ],
}


def _marginal_rate(filing_status: str, income: float) -> float:
    for threshold, rate in reversed(BRACKETS[filing_status]):
        if income >= threshold:
            return rate
    return BRACKETS[filing_status][0][1]


TOOL_META = {
    "name": "charitable_giving_optimizer",
    "description": (
        "Applies IRS AGI limits for cash (60%) and appreciated asset (30%) donations and "
        "advises whether gifting stock yields higher tax savings."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "cash_donations": {
                "type": "number",
                "description": "Planned cash contributions to qualified charities.",
            },
            "appreciated_assets": {
                "type": "array",
                "description": "List of assets with fmv, cost_basis, holding_period (months).",
                "items": {"type": "object"},
            },
            "agi": {
                "type": "number",
                "description": "Adjusted gross income for the tax year.",
            },
            "filing_status": {
                "type": "string",
                "description": "single or mfj.",
            },
        },
        "required": ["cash_donations", "appreciated_assets", "agi", "filing_status"],
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


def charitable_giving_optimizer(**kwargs: Any) -> dict:
    """Optimize deduction mix between cash and appreciated asset donations."""
    try:
        cash = float(kwargs["cash_donations"])
        assets_input = kwargs["appreciated_assets"]
        agi = float(kwargs["agi"])
        filing_status = str(kwargs["filing_status"]).strip().lower()

        if filing_status not in BRACKETS:
            raise ValueError("filing_status must be single or mfj")
        if agi <= 0:
            raise ValueError("agi must be positive")
        if not isinstance(assets_input, list):
            raise ValueError("appreciated_assets must be a list")

        appreciated_value = 0.0
        for asset in assets_input:
            fmv = float(asset["fmv"])
            holding_period = int(asset.get("holding_period", 0))
            if holding_period < 12:
                continue
            appreciated_value += fmv

        cash_cap = agi * 0.60
        stock_cap = agi * 0.30
        deductible_cash = min(cash, cash_cap)
        deductible_stock = min(appreciated_value, stock_cap)
        total_deduction = deductible_cash + deductible_stock
        carryforward = (cash - deductible_cash) + (appreciated_value - deductible_stock)
        marginal_rate = _marginal_rate(filing_status, agi)
        tax_savings = total_deduction * marginal_rate
        strategy = (
            "gift_appreciated_assets_first"
            if appreciated_value > 0 and deductible_stock > 0
            else "cash_only"
        )

        return {
            "status": "success",
            "data": {
                "total_deduction": total_deduction,
                "tax_savings": tax_savings,
                "agi_limitation": {
                    "cash_cap": cash_cap,
                    "stock_cap": stock_cap,
                    "deductible_cash": deductible_cash,
                    "deductible_stock": deductible_stock,
                },
                "carryforward": carryforward,
                "optimal_strategy": strategy,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"charitable_giving_optimizer failed: {e}")
        _log_lesson(f"charitable_giving_optimizer: {e}")
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
