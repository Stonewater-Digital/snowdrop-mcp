"""
Executive Smary: Breaks down gross, operating, EBITDA, pretax, and net profit margins.
Inputs: revenue (float), cogs (float), operating_expenses (dict), interest_expense (float), tax_rate (float)
Outputs: gross_margin (float), operating_margin (float), ebitda_margin (float), pretax_margin (float), net_margin (float), margin_waterfall (list)
MCP Tool Name: profit_margin_analyzer
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "profit_margin_analyzer",
    "description": (
        "Builds a margin waterfall starting at revenue to show gross, operating, EBITDA, "
        "pretax, and net profit percentages."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "revenue": {"type": "number", "description": "Total revenue."},
            "cogs": {"type": "number", "description": "Cost of goods sold."},
            "operating_expenses": {
                "type": "object",
                "description": "Dictionary of operating expense categories and dollar amounts.",
            },
            "interest_expense": {"type": "number", "description": "Interest expense."},
            "tax_rate": {"type": "number", "description": "Effective tax rate as decimal."},
        },
        "required": ["revenue", "cogs", "operating_expenses", "interest_expense", "tax_rate"],
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


def profit_margin_analyzer(**kwargs: Any) -> dict:
    """Compute margin stack and provide a margin waterfall summary."""
    try:
        revenue = float(kwargs["revenue"])
        cogs = float(kwargs["cogs"])
        operating_expenses: Dict[str, float] = {
            k: float(v) for k, v in kwargs["operating_expenses"].items()
        }
        interest_expense = float(kwargs["interest_expense"])
        tax_rate = float(kwargs["tax_rate"])

        gross_profit = revenue - cogs
        gross_margin = gross_profit / revenue if revenue else 0.0
        operating_expense_total = sum(operating_expenses.values())
        operating_income = gross_profit - operating_expense_total
        operating_margin = operating_income / revenue if revenue else 0.0
        ebitda = operating_income  # assuming expenses exclude depreciation
        ebitda_margin = ebitda / revenue if revenue else 0.0
        pretax_income = operating_income - interest_expense
        pretax_margin = pretax_income / revenue if revenue else 0.0
        net_income = pretax_income * (1 - tax_rate)
        net_margin = net_income / revenue if revenue else 0.0

        waterfall: List[Dict[str, Any]] = [
            {"stage": "Revenue", "amount": revenue, "margin": 1.0},
            {"stage": "COGS", "amount": -cogs, "margin": gross_margin},
        ]
        for name, amount in operating_expenses.items():
            waterfall.append({"stage": name, "amount": -amount, "margin": None})
        waterfall.extend(
            [
                {"stage": "Operating Income", "amount": operating_income, "margin": operating_margin},
                {"stage": "Interest", "amount": -interest_expense, "margin": pretax_margin},
                {"stage": "Taxes", "amount": -pretax_income * tax_rate, "margin": net_margin},
                {"stage": "Net Income", "amount": net_income, "margin": net_margin},
            ]
        )

        return {
            "status": "success",
            "data": {
                "gross_margin": gross_margin,
                "operating_margin": operating_margin,
                "ebitda_margin": ebitda_margin,
                "pretax_margin": pretax_margin,
                "net_margin": net_margin,
                "margin_waterfall": waterfall,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError, KeyError) as e:
        logger.error(f"profit_margin_analyzer failed: {e}")
        _log_lesson(f"profit_margin_analyzer: {e}")
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
