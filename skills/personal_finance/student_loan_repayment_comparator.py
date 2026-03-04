"""
Executive Smary: Compares federal student loan repayment plans including forgiveness.
Inputs: loan_balance (float), interest_rate (float), annual_income (float), income_growth_rate (float), filing_status (str), family_size (int)
Outputs: monthly_payment (dict), total_paid (dict), forgiveness_amount (dict), recommended_plan (str)
MCP Tool Name: student_loan_repayment_comparator
"""
import logging
from datetime import datetime, timezone
from typing import Any, Callable, Dict, Tuple

logger = logging.getLogger("snowdrop.skills")

PLAN_TERMS = {
    "standard": 120,
    "graduated": 120,
    "ibr": 300,
    "paye": 240,
    "repaye": 300,
}


def _poverty_guideline(filing_status: str, family_size: int) -> float:
    base = 14580 + max(family_size - 1, 0) * 5140
    if filing_status == "mfj":
        base *= 1.25
    return base


def _simulate(
    loan_balance: float,
    monthly_rate: float,
    term_months: int,
    payment_func: Callable[[int, float], float],
    cap_payment: float | None = None,
) -> Tuple[float, float, float]:
    balance = loan_balance
    total_paid = 0.0
    first_payment = None
    for month in range(1, term_months + 1):
        interest = balance * monthly_rate
        payment = payment_func(month, balance + interest)
        if cap_payment is not None:
            payment = min(payment, cap_payment)
        payment = min(payment, balance + interest)
        if first_payment is None:
            first_payment = payment
        total_paid += payment
        balance = balance + interest - payment
        if balance <= 0:
            return first_payment or 0.0, total_paid, 0.0
    forgiveness = max(balance, 0.0)
    return first_payment or 0.0, total_paid, forgiveness


def _income_based_payment(
    annual_income: float,
    income_growth_rate: float,
    filing_status: str,
    family_size: int,
    pct_of_discretionary: float,
    cap: float | None,
) -> Callable[[int, float], float]:
    poverty_line = _poverty_guideline(filing_status, family_size)

    def payment(month: int, _balance_plus_interest: float) -> float:
        years_elapsed = (month - 1) // 12
        income = annual_income * (1 + income_growth_rate) ** years_elapsed
        discretionary = max(0.0, income - 1.5 * poverty_line)
        monthly = discretionary * pct_of_discretionary / 12
        if cap is not None:
            monthly = min(monthly, cap)
        return monthly

    return payment


TOOL_META = {
    "name": "student_loan_repayment_comparator",
    "description": (
        "Models standard, graduated, IBR, PAYE, and REPAYE student loan plans to expose "
        "monthly payments, total paid, and potential forgiveness along with a recommendation."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "loan_balance": {
                "type": "number",
                "description": "Total outstanding federal student loan balance.",
            },
            "interest_rate": {
                "type": "number",
                "description": "Annual loan interest rate as decimal.",
            },
            "annual_income": {
                "type": "number",
                "description": "Current adjusted gross income for payment calculations.",
            },
            "income_growth_rate": {
                "type": "number",
                "description": "Expected annual income growth as decimal.",
            },
            "filing_status": {
                "type": "string",
                "description": "single or mfj to estimate discretionary income.",
            },
            "family_size": {
                "type": "number",
                "description": "Household size used for poverty guideline.",
            },
        },
        "required": [
            "loan_balance",
            "interest_rate",
            "annual_income",
            "income_growth_rate",
            "filing_status",
            "family_size",
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


def student_loan_repayment_comparator(**kwargs: Any) -> dict:
    """Compare major federal student loan repayment options."""
    try:
        loan_balance = float(kwargs["loan_balance"])
        interest_rate = float(kwargs["interest_rate"])
        annual_income = float(kwargs["annual_income"])
        income_growth_rate = float(kwargs["income_growth_rate"])
        filing_status = str(kwargs["filing_status"]).strip().lower()
        family_size = int(kwargs["family_size"])

        if loan_balance <= 0 or family_size <= 0:
            raise ValueError("loan_balance and family_size must be positive")
        if filing_status not in {"single", "mfj"}:
            raise ValueError("filing_status must be single or mfj")

        monthly_rate = interest_rate / 12
        standard_payment = (
            loan_balance * monthly_rate * (1 + monthly_rate) ** 120 / ((1 + monthly_rate) ** 120 - 1)
            if monthly_rate > 0
            else loan_balance / 120
        )

        plans: Dict[str, Dict[str, float]] = {}

        # Standard
        spayment, stotal, sforgive = _simulate(
            loan_balance,
            monthly_rate,
            PLAN_TERMS["standard"],
            lambda _m, _b: standard_payment,
        )
        plans["standard"] = {
            "monthly": spayment,
            "total": stotal,
            "forgiveness": sforgive,
        }

        # Graduated: payment increases 7% every 2 years starting at 60% of standard
        def grad_payment(month: int, _b: float) -> float:
            step = (month - 1) // 24
            return standard_payment * 0.6 * (1.07 ** step)

        gpayment, gtotal, gforgive = _simulate(
            loan_balance,
            monthly_rate,
            PLAN_TERMS["graduated"],
            grad_payment,
        )
        plans["graduated"] = {
            "monthly": gpayment,
            "total": gtotal,
            "forgiveness": gforgive,
        }

        # IBR
        ibr_payment_func = _income_based_payment(
            annual_income,
            income_growth_rate,
            filing_status,
            family_size,
            0.15,
            standard_payment,
        )
        ibr_monthly, ibr_total, ibr_forgive = _simulate(
            loan_balance,
            monthly_rate,
            PLAN_TERMS["ibr"],
            ibr_payment_func,
            cap_payment=standard_payment,
        )
        plans["ibr"] = {
            "monthly": ibr_monthly,
            "total": ibr_total,
            "forgiveness": ibr_forgive,
        }

        # PAYE
        paye_payment_func = _income_based_payment(
            annual_income,
            income_growth_rate,
            filing_status,
            family_size,
            0.10,
            standard_payment,
        )
        paye_monthly, paye_total, paye_forgive = _simulate(
            loan_balance,
            monthly_rate,
            PLAN_TERMS["paye"],
            paye_payment_func,
            cap_payment=standard_payment,
        )
        plans["paye"] = {
            "monthly": paye_monthly,
            "total": paye_total,
            "forgiveness": paye_forgive,
        }

        # REPAYE (no cap, 25 years)
        repaye_payment_func = _income_based_payment(
            annual_income,
            income_growth_rate,
            filing_status,
            family_size,
            0.10,
            None,
        )
        repaye_monthly, repaye_total, repaye_forgive = _simulate(
            loan_balance,
            monthly_rate,
            PLAN_TERMS["repaye"],
            repaye_payment_func,
        )
        plans["repaye"] = {
            "monthly": repaye_monthly,
            "total": repaye_total,
            "forgiveness": repaye_forgive,
        }

        recommended_plan = min(plans.items(), key=lambda item: item[1]["total"])[0]

        return {
            "status": "success",
            "data": {
                "monthly_payment": {k: v["monthly"] for k, v in plans.items()},
                "total_paid": {k: v["total"] for k, v in plans.items()},
                "forgiveness_amount": {k: v["forgiveness"] for k, v in plans.items()},
                "recommended_plan": recommended_plan,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"student_loan_repayment_comparator failed: {e}")
        _log_lesson(f"student_loan_repayment_comparator: {e}")
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
