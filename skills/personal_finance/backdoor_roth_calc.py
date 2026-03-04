"""
Executive Smary: Evaluates tax impact of executing a backdoor Roth contribution.
Inputs: traditional_ira_balance (float), contribution_amount (float), tax_bracket (float), pro_rata_basis (float)
Outputs: taxable_amount (float), tax_cost (float), backdoor_feasibility (str), mega_backdoor_eligible (bool)
MCP Tool Name: backdoor_roth_calc
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "backdoor_roth_calc",
    "description": (
        "Applies the IRS pro-rata rule to a backdoor Roth IRA conversion and reports the "
        "taxable portion, estimated tax bill, and feasibility guidance."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "traditional_ira_balance": {
                "type": "number",
                "description": "Aggregate value of traditional IRAs on December 31.",
            },
            "contribution_amount": {
                "type": "number",
                "description": "Nondeductible contribution slated for conversion.",
            },
            "tax_bracket": {
                "type": "number",
                "description": "Marginal federal tax rate as decimal.",
            },
            "pro_rata_basis": {
                "type": "number",
                "description": "After-tax basis already tracked on Form 8606.",
            },
        },
        "required": [
            "traditional_ira_balance",
            "contribution_amount",
            "tax_bracket",
            "pro_rata_basis",
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


def backdoor_roth_calc(**kwargs: Any) -> dict:
    """Quantify taxes due on a backdoor Roth conversion and flag mega-backdoor potential."""
    try:
        ira_balance = float(kwargs["traditional_ira_balance"])
        contribution = float(kwargs["contribution_amount"])
        tax_bracket = float(kwargs["tax_bracket"])
        basis = float(kwargs["pro_rata_basis"])

        if contribution <= 0:
            raise ValueError("contribution_amount must be positive")
        if ira_balance < 0 or basis < 0:
            raise ValueError("Balances and basis must be non-negative")

        total_balance = ira_balance + contribution
        basis_total = basis + contribution
        after_tax_ratio = basis_total / total_balance if total_balance > 0 else 1.0
        taxable_amount = contribution * (1 - after_tax_ratio)
        tax_cost = taxable_amount * tax_bracket
        feasibility = "clean" if ira_balance == 0 else "consider_rollover"
        mega_backdoor = ira_balance == 0 and contribution >= 6500

        return {
            "status": "success",
            "data": {
                "taxable_amount": taxable_amount,
                "tax_cost": tax_cost,
                "backdoor_feasibility": feasibility,
                "mega_backdoor_eligible": mega_backdoor,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"backdoor_roth_calc failed: {e}")
        _log_lesson(f"backdoor_roth_calc: {e}")
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
