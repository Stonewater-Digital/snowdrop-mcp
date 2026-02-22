"""
Executive Summary: Determines whether the GP owes a clawback based on carry received versus carry entitled after preferred return.

Inputs: total_distributions (float), total_contributions (float), preferred_return (float), carry_received (float)
Outputs: dict with clawback_amount (float), clawback_required (bool), entitled_carry (float)
MCP Tool Name: clawback_analyzer
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "clawback_analyzer",
    "description": "Determines whether the GP owes a clawback based on carry received versus carry entitled after preferred return.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "total_distributions": {
                "type": "number",
                "description": "Total distributions paid to all partners (LP + GP) in dollars",
            },
            "total_contributions": {
                "type": "number",
                "description": "Total capital contributions made to the fund in dollars",
            },
            "preferred_return": {
                "type": "number",
                "description": "LP preferred return rate (e.g. 0.08 for 8%); applied as a flat rate to contributions",
            },
            "carry_received": {
                "type": "number",
                "description": "Total carried interest actually paid to the GP in dollars",
            },
        },
        "required": ["total_distributions", "total_contributions", "preferred_return", "carry_received"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "clawback_amount": {"type": "number"},
            "clawback_required": {"type": "boolean"},
            "entitled_carry": {"type": "number"},
            "lp_preferred_return_amount": {"type": "number"},
            "profit_above_hurdle": {"type": "number"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": [
            "clawback_amount", "clawback_required", "entitled_carry",
            "lp_preferred_return_amount", "profit_above_hurdle", "status", "timestamp",
        ],
    },
}

_STANDARD_CARRY_RATE = 0.20  # Industry standard GP carry rate


def clawback_analyzer(
    total_distributions: float,
    total_contributions: float,
    preferred_return: float,
    carry_received: float,
    carry_rate: float = _STANDARD_CARRY_RATE,
    **kwargs: Any,
) -> dict:
    """Determines GP clawback obligation by comparing carry received to carry entitled.

    Clawback logic:
    1. LP preferred return = contributions * preferred_return (flat, non-compounded)
    2. Profit above hurdle = max(0, total_distributions - contributions - lp_pref)
    3. Entitled carry = profit_above_hurdle * carry_rate
    4. Clawback = max(0, carry_received - entitled_carry)

    This ensures the GP only retains carry on realized profits after LPs
    have received their capital back plus preferred return.

    Args:
        total_distributions: Total distributions paid to all partners in dollars.
        total_contributions: Total capital contributions made to the fund in dollars.
        preferred_return: LP preferred return rate applied to total contributions.
        carry_received: Total carry actually paid to the GP in dollars.
        carry_rate: GP carry rate; defaults to 0.20 (20%).
        **kwargs: Ignored extra keyword arguments.

    Returns:
        dict: Contains clawback_amount (float), clawback_required (bool),
              entitled_carry (float), lp_preferred_return_amount (float),
              profit_above_hurdle (float), status, and timestamp.
    """
    try:
        if total_contributions < 0:
            raise ValueError("total_contributions cannot be negative")
        if total_distributions < 0:
            raise ValueError("total_distributions cannot be negative")
        if not (0.0 <= preferred_return <= 1.0):
            raise ValueError("preferred_return must be between 0 and 1")
        if carry_received < 0:
            raise ValueError("carry_received cannot be negative")
        if not (0.0 <= carry_rate <= 1.0):
            raise ValueError("carry_rate must be between 0 and 1")

        # LP preferred return is calculated on total contributions
        lp_preferred_return_amount = total_contributions * preferred_return

        # Profit above the hurdle (after returning capital + preferred)
        profit_above_hurdle = max(
            0.0,
            total_distributions - total_contributions - lp_preferred_return_amount,
        )

        # Entitled carry = standard carry rate on profits above hurdle
        entitled_carry = profit_above_hurdle * carry_rate

        # Clawback: GP must return excess carry received
        clawback_amount = max(0.0, carry_received - entitled_carry)
        clawback_required = clawback_amount > 0.0

        result = {
            "clawback_required": clawback_required,
            "clawback_amount": round(clawback_amount, 2),
            "entitled_carry": round(entitled_carry, 2),
            "carry_received": round(carry_received, 2),
            "carry_excess": round(carry_received - entitled_carry, 2),
            "lp_preferred_return_amount": round(lp_preferred_return_amount, 2),
            "profit_above_hurdle": round(profit_above_hurdle, 2),
            "total_distributions": round(total_distributions, 2),
            "total_contributions": round(total_contributions, 2),
            "preferred_return_rate": preferred_return,
            "carry_rate": carry_rate,
        }
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as e:
        logger.error(f"clawback_analyzer failed: {e}")
        _log_lesson(f"clawback_analyzer: {e}")
        return {"status": "error", "error": str(e), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    """Appends an error lesson to the lessons log.

    Args:
        message: The lesson message to log.
    """
    os.makedirs("logs", exist_ok=True)
    with open("logs/lessons.md", "a") as f:
        f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
