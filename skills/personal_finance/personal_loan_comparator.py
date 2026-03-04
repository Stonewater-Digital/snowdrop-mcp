"""
Executive Smary: Compares personal loan offers by true cost, payments, and effective APR.
Inputs: offers (list)
Outputs: ranked_by_total_cost (list), monthly_payment (dict), effective_apr (dict), total_interest (dict)
MCP Tool Name: personal_loan_comparator
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "personal_loan_comparator",
    "description": (
        "Evaluates personal loan offers by accounting for origination fees, payments, "
        "total interest, and estimated effective APR to rank the cheapest option."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "offers": {
                "type": "array",
                "description": "List of loan offers with lender, amount, rate, term_months, origination_fee.",
                "items": {"type": "object"},
            }
        },
        "required": ["offers"],
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


def personal_loan_comparator(**kwargs: Any) -> dict:
    """Rank personal loan offers by total borrowing cost and effective apr."""
    try:
        offers_input = kwargs["offers"]
        if not isinstance(offers_input, list) or not offers_input:
            raise ValueError("offers must be a non-empty list")

        monthly_payment: Dict[str, float] = {}
        effective_apr: Dict[str, float] = {}
        total_interest: Dict[str, float] = {}
        ranked: List[Dict[str, Any]] = []

        for offer in offers_input:
            lender = str(offer.get("lender", "Unknown"))
            amount = float(offer["amount"])
            rate = float(offer["rate"])
            term_months = int(offer["term_months"])
            origination_fee = float(offer.get("origination_fee", 0.0))
            if amount <= 0 or term_months <= 0:
                raise ValueError("amount and term_months must be positive")
            monthly_rate = rate / 12
            if monthly_rate == 0:
                payment = amount / term_months
            else:
                factor = (1 + monthly_rate) ** term_months
                payment = amount * monthly_rate * factor / (factor - 1)
            total_paid = payment * term_months
            interest_paid = total_paid - amount
            proceeds = max(amount - origination_fee, 1e-9)
            eff_apr = ((interest_paid + origination_fee) / proceeds) / (term_months / 12)

            monthly_payment[lender] = payment
            effective_apr[lender] = eff_apr
            total_interest[lender] = interest_paid
            ranked.append(
                {
                    "lender": lender,
                    "total_cost": interest_paid + origination_fee,
                    "monthly_payment": payment,
                    "effective_apr": eff_apr,
                }
            )

        ranked.sort(key=lambda x: x["total_cost"])

        return {
            "status": "success",
            "data": {
                "ranked_by_total_cost": ranked,
                "monthly_payment": monthly_payment,
                "effective_apr": effective_apr,
                "total_interest": total_interest,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"personal_loan_comparator failed: {e}")
        _log_lesson(f"personal_loan_comparator: {e}")
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
