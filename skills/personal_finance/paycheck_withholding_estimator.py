"""
Executive Smary: Estimates paycheck net pay after federal, state, and payroll taxes.
Inputs: gross_pay (float), pay_frequency (str), filing_status (str), allowances (int), pre_tax_deductions (dict), state (str)
Outputs: federal_tax (float), state_tax (float), social_security (float), medicare (float), net_pay (float), annual_projection (dict)
MCP Tool Name: paycheck_withholding_estimator
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict

logger = logging.getLogger("snowdrop.skills")

PAY_PERIODS = {
    "weekly": 52,
    "biweekly": 26,
    "semimonthly": 24,
    "monthly": 12,
    "annual": 1,
}

FEDERAL_BRACKETS = {
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

STATE_NO_TAX = {"ak", "fl", "nv", "sd", "tx", "wa", "wy"}


def _estimate_annual_tax(taxable_income: float, filing_status: str) -> float:
    brackets = FEDERAL_BRACKETS[filing_status]
    tax = 0.0
    for idx, (threshold, rate) in enumerate(brackets):
        next_threshold = brackets[idx + 1][0] if idx + 1 < len(brackets) else None
        if taxable_income <= threshold:
            break
        upper = next_threshold if next_threshold is not None else taxable_income
        amount = min(taxable_income, upper) - threshold
        if amount <= 0:
            continue
        tax += amount * rate
    return tax


TOOL_META = {
    "name": "paycheck_withholding_estimator",
    "description": (
        "Estimates paycheck taxes for federal, state, Social Security, and Medicare "
        "with net pay and annualized projections based on pay frequency."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "gross_pay": {
                "type": "number",
                "description": "Gross wages per pay period before deductions.",
            },
            "pay_frequency": {
                "type": "string",
                "description": "weekly, biweekly, semimonthly, monthly, or annual.",
            },
            "filing_status": {
                "type": "string",
                "description": "single or mfj for withholding assumptions.",
            },
            "allowances": {
                "type": "number",
                "description": "Number of withholding allowances, reduce taxable wages.",
            },
            "pre_tax_deductions": {
                "type": "object",
                "description": "Dictionary of pre-tax deductions such as 401k, HSA.",
            },
            "state": {
                "type": "string",
                "description": "Two-letter state code for state income tax estimate.",
            },
        },
        "required": ["gross_pay", "pay_frequency", "filing_status", "allowances", "pre_tax_deductions", "state"],
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


def paycheck_withholding_estimator(**kwargs: Any) -> dict:
    """Estimate net paycheck after federal, state, and payroll taxes."""
    try:
        gross_pay = float(kwargs["gross_pay"])
        pay_frequency = str(kwargs["pay_frequency"]).strip().lower()
        filing_status = str(kwargs["filing_status"]).strip().lower()
        allowances = int(kwargs["allowances"])
        pre_tax = kwargs["pre_tax_deductions"]
        state = str(kwargs["state"]).strip().lower()

        if gross_pay <= 0 or allowances < 0:
            raise ValueError("gross_pay must be positive and allowances non-negative")
        if pay_frequency not in PAY_PERIODS:
            raise ValueError("Unsupported pay_frequency")
        if filing_status not in FEDERAL_BRACKETS:
            raise ValueError("filing_status must be single or mfj")
        if not isinstance(pre_tax, dict):
            raise ValueError("pre_tax_deductions must be a dict")

        periods = PAY_PERIODS[pay_frequency]
        allowance_value = allowances * 4300 / periods
        pre_tax_total = sum(float(v) for v in pre_tax.values())
        taxable_wages = max(gross_pay - pre_tax_total - allowance_value, 0.0)
        annual_taxable = taxable_wages * periods
        annual_tax = _estimate_annual_tax(annual_taxable, filing_status)
        federal_tax = annual_tax / periods

        # Social Security and Medicare
        ss_wage_base = 168600
        ss_taxable = min(taxable_wages * periods, ss_wage_base)
        social_security = (ss_taxable / periods) * 0.062
        medicare_base = taxable_wages * 0.0145
        additional_medicare = (
            (annual_taxable - 200000) * 0.009 / periods if annual_taxable > 200000 else 0.0
        )
        medicare = medicare_base + additional_medicare

        # State tax (flat 5% unless no income tax state)
        if state in STATE_NO_TAX:
            state_tax_rate = 0.0
        else:
            state_tax_rate = 0.05
        state_tax = taxable_wages * state_tax_rate

        total_taxes = federal_tax + state_tax + social_security + medicare
        net_pay = gross_pay - total_taxes - pre_tax_total

        annual_projection = {
            "gross": gross_pay * periods,
            "net": net_pay * periods,
            "federal_tax": federal_tax * periods,
            "state_tax": state_tax * periods,
        }

        return {
            "status": "success",
            "data": {
                "federal_tax": federal_tax,
                "state_tax": state_tax,
                "social_security": social_security,
                "medicare": medicare,
                "net_pay": net_pay,
                "annual_projection": annual_projection,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"paycheck_withholding_estimator failed: {e}")
        _log_lesson(f"paycheck_withholding_estimator: {e}")
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
