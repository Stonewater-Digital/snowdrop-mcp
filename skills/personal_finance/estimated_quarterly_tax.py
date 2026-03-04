"""
Executive Smary: Estimates quarterly federal tax payments for variable income.
Inputs: annual_income (float), expected_withholding (float), filing_status (str), self_employment_income (float), deductions (float)
Outputs: total_tax_liability (float), quarterly_payment (float), safe_harbor_amount (float), penalty_risk (bool)
MCP Tool Name: estimated_quarterly_tax
"""
import logging
from datetime import datetime, timezone
from typing import Any, List, Tuple

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


def _tax(brackets: List[Tuple[float, float]], taxable: float) -> float:
    tax = 0.0
    for idx, (threshold, rate) in enumerate(brackets):
        next_thr = brackets[idx + 1][0] if idx + 1 < len(brackets) else None
        if taxable <= threshold:
            break
        upper = next_thr if next_thr is not None else taxable
        amount = min(taxable, upper) - threshold
        if amount <= 0:
            continue
        tax += amount * rate
    return tax


def _se_tax(income: float) -> float:
    if income <= 0:
        return 0.0
    earnings = income * 0.9235
    ss_tax = min(earnings, 168600) * 0.124
    medicare = earnings * 0.029
    additional = max(earnings - 200000, 0) * 0.009
    return ss_tax + medicare + additional


TOOL_META = {
    "name": "estimated_quarterly_tax",
    "description": (
        "Combines income tax and self-employment tax to suggest quarterly estimated "
        "payments and safe harbor amounts to minimize penalties."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "annual_income": {
                "type": "number",
                "description": "Projected total income subject to federal tax.",
            },
            "expected_withholding": {
                "type": "number",
                "description": "Taxes expected to be withheld from paychecks.",
            },
            "filing_status": {
                "type": "string",
                "description": "single or mfj.",
            },
            "self_employment_income": {
                "type": "number",
                "description": "Portion of income subject to self-employment tax.",
            },
            "deductions": {
                "type": "number",
                "description": "Estimated deductions (standard + itemized) reducing taxable income.",
            },
        },
        "required": [
            "annual_income",
            "expected_withholding",
            "filing_status",
            "self_employment_income",
            "deductions",
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


def estimated_quarterly_tax(**kwargs: Any) -> dict:
    """Estimate quarterly tax obligations to avoid IRS underpayment penalties."""
    try:
        annual_income = float(kwargs["annual_income"])
        expected_withholding = float(kwargs["expected_withholding"])
        filing_status = str(kwargs["filing_status"]).strip().lower()
        self_employment_income = float(kwargs["self_employment_income"])
        deductions = float(kwargs["deductions"])

        if filing_status not in BRACKETS:
            raise ValueError("filing_status must be single or mfj")
        if annual_income < 0 or deductions < 0:
            raise ValueError("income and deductions must be non-negative")

        taxable_income = max(annual_income - deductions, 0.0)
        income_tax = _tax(BRACKETS[filing_status], taxable_income)
        se_tax = _se_tax(self_employment_income)
        total_tax = income_tax + se_tax
        remaining_due = max(total_tax - expected_withholding, 0.0)
        quarterly_payment = remaining_due / 4
        safe_harbor = total_tax * 0.9
        penalty_risk = expected_withholding + quarterly_payment * 4 < safe_harbor

        return {
            "status": "success",
            "data": {
                "total_tax_liability": total_tax,
                "quarterly_payment": quarterly_payment,
                "safe_harbor_amount": safe_harbor,
                "penalty_risk": penalty_risk,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"estimated_quarterly_tax failed: {e}")
        _log_lesson(f"estimated_quarterly_tax: {e}")
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
