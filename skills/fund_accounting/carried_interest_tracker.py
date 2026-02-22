"""
Executive Summary: Tracks cumulative GP carried interest earned, distributed, and held in reserve based on fund cash flows.

Inputs: fund_id (str), vintage_year (int), distributions (list[dict]: date, amount), contributions (list[dict]: date, amount)
Outputs: dict with carry_earned (float), carry_distributed (float), carry_reserve (float)
MCP Tool Name: carried_interest_tracker
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "carried_interest_tracker",
    "description": "Tracks cumulative GP carried interest earned, distributed, and held in reserve based on fund cash flows.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "fund_id": {"type": "string", "description": "Fund identifier"},
            "vintage_year": {"type": "integer", "description": "Fund vintage year"},
            "distributions": {
                "type": "array",
                "description": "List of distributions from portfolio to fund",
                "items": {
                    "type": "object",
                    "properties": {
                        "date": {"type": "string", "description": "ISO date string (YYYY-MM-DD)"},
                        "amount": {"type": "number", "description": "Distribution amount in dollars"},
                    },
                    "required": ["date", "amount"],
                },
            },
            "contributions": {
                "type": "array",
                "description": "List of LP capital contributions",
                "items": {
                    "type": "object",
                    "properties": {
                        "date": {"type": "string", "description": "ISO date string (YYYY-MM-DD)"},
                        "amount": {"type": "number", "description": "Contribution amount in dollars"},
                    },
                    "required": ["date", "amount"],
                },
            },
        },
        "required": ["fund_id", "vintage_year", "distributions", "contributions"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "carry_earned": {"type": "number"},
            "carry_distributed": {"type": "number"},
            "carry_reserve": {"type": "number"},
            "total_contributions": {"type": "number"},
            "total_distributions": {"type": "number"},
            "preferred_return_amount": {"type": "number"},
            "profit_subject_to_carry": {"type": "number"},
            "dpi": {"type": "number"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": [
            "carry_earned", "carry_distributed", "carry_reserve",
            "total_contributions", "total_distributions", "status", "timestamp",
        ],
    },
}

_PREFERRED_RETURN_RATE = 0.08   # Standard 8% preferred return
_CARRY_RATE = 0.20              # Standard 20% GP carry
_CARRY_DISTRIBUTION_THRESHOLD = 0.80  # Distribute 80% of earned carry; hold 20% in reserve


def carried_interest_tracker(
    fund_id: str,
    vintage_year: int,
    distributions: list[dict[str, Any]],
    contributions: list[dict[str, Any]],
    preferred_return_rate: float = _PREFERRED_RETURN_RATE,
    carry_rate: float = _CARRY_RATE,
    **kwargs: Any,
) -> dict:
    """Tracks GP carry earned, distributed, and held in reserve.

    Methodology (simplified cash-basis):
    1. Sum all LP contributions.
    2. Compute preferred return = total_contributions * preferred_return_rate.
    3. Sum all distributions (proceeds to fund/LP).
    4. Profit subject to carry = max(0, distributions - contributions - preferred_return).
    5. Carry earned = profit_subject_to_carry * carry_rate.
    6. Carry distributed = carry_earned * carry_distribution_threshold.
    7. Carry reserve = carry_earned - carry_distributed.

    DPI (Distributions to Paid-In) = total_distributions / total_contributions.

    Args:
        fund_id: Fund identifier string.
        vintage_year: Four-digit fund vintage year.
        distributions: List of dicts with keys: date (str), amount (float).
        contributions: List of dicts with keys: date (str), amount (float).
        preferred_return_rate: LP preferred return rate; defaults to 0.08.
        carry_rate: GP carry rate; defaults to 0.20.
        **kwargs: Ignored extra keyword arguments.

    Returns:
        dict: Contains carry_earned, carry_distributed, carry_reserve,
              total_contributions, total_distributions, preferred_return_amount,
              profit_subject_to_carry, dpi, status, timestamp.
    """
    try:
        if not fund_id:
            raise ValueError("fund_id cannot be empty")
        if not (1900 <= vintage_year <= 2100):
            raise ValueError("vintage_year must be a valid year")

        total_contributions = sum(float(c["amount"]) for c in contributions)
        total_distributions = sum(float(d["amount"]) for d in distributions)

        if total_contributions < 0:
            raise ValueError("total_contributions cannot be negative")
        if total_distributions < 0:
            raise ValueError("total_distributions cannot be negative")

        preferred_return_amount = total_contributions * preferred_return_rate
        profit_subject_to_carry = max(
            0.0,
            total_distributions - total_contributions - preferred_return_amount,
        )

        carry_earned = profit_subject_to_carry * carry_rate

        # Distribute 80% of carry, hold 20% as reserve against clawback
        carry_distributed = carry_earned * _CARRY_DISTRIBUTION_THRESHOLD
        carry_reserve = carry_earned - carry_distributed

        dpi = total_distributions / total_contributions if total_contributions > 0 else 0.0

        # Chronological cash flow summary
        sorted_contributions = sorted(contributions, key=lambda x: x.get("date", ""))
        sorted_distributions = sorted(distributions, key=lambda x: x.get("date", ""))

        result = {
            "fund_id": fund_id,
            "vintage_year": vintage_year,
            "total_contributions": round(total_contributions, 2),
            "total_distributions": round(total_distributions, 2),
            "preferred_return_rate": preferred_return_rate,
            "preferred_return_amount": round(preferred_return_amount, 2),
            "profit_subject_to_carry": round(profit_subject_to_carry, 2),
            "carry_rate": carry_rate,
            "carry_earned": round(carry_earned, 2),
            "carry_distributed": round(carry_distributed, 2),
            "carry_reserve": round(carry_reserve, 2),
            "dpi": round(dpi, 4),
            "hurdle_cleared": total_distributions >= (total_contributions + preferred_return_amount),
            "contribution_count": len(contributions),
            "distribution_count": len(distributions),
            "first_contribution_date": sorted_contributions[0]["date"] if sorted_contributions else None,
            "last_distribution_date": sorted_distributions[-1]["date"] if sorted_distributions else None,
        }
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as e:
        logger.error(f"carried_interest_tracker failed: {e}")
        _log_lesson(f"carried_interest_tracker: {e}")
        return {"status": "error", "error": str(e), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    """Appends an error lesson to the lessons log.

    Args:
        message: The lesson message to log.
    """
    os.makedirs("logs", exist_ok=True)
    with open("logs/lessons.md", "a") as f:
        f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
