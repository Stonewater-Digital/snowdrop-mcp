"""
Executive Summary: Calculates the net management fee after applying LP-favorable offsets from transaction fees and advisory income at a configurable offset rate.

Inputs: base_fee (float), transaction_fees_earned (float), advisory_income (float), offset_rate (float, default 0.80)
Outputs: dict with net_fee (float), offset_amount (float), offset_pct (float), breakdown (dict)
MCP Tool Name: management_fee_offset
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "management_fee_offset",
    "description": (
        "Computes the net management fee after applying a fee offset for transaction fees "
        "and advisory income earned by the GP. Per ILPA best practices, a configurable "
        "percentage (default 80%) of GP-earned fees is credited against the base management fee, "
        "benefiting LPs. Net fee is floored at zero (cannot be negative)."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "base_fee": {
                "type": "number",
                "description": "Gross management fee before offsets ($)"
            },
            "transaction_fees_earned": {
                "type": "number",
                "description": "Transaction/closing fees earned by the GP ($)"
            },
            "advisory_income": {
                "type": "number",
                "description": "Monitoring, advisory, or consulting income earned by the GP ($)"
            },
            "offset_rate": {
                "type": "number",
                "description": "Fraction of GP fees credited against management fee (default 0.80 = 80%)",
                "default": 0.80,
                "minimum": 0.0,
                "maximum": 1.0
            }
        },
        "required": ["base_fee", "transaction_fees_earned", "advisory_income"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "net_fee": {"type": "number"},
            "offset_amount": {"type": "number"},
            "offset_pct": {"type": "number"},
            "gross_fee_income": {"type": "number"},
            "breakdown": {
                "type": "object",
                "properties": {
                    "base_fee": {"type": "number"},
                    "transaction_fees_earned": {"type": "number"},
                    "advisory_income": {"type": "number"},
                    "total_offset_eligible": {"type": "number"},
                    "offset_rate_applied": {"type": "number"},
                    "offset_amount": {"type": "number"},
                    "net_fee_before_floor": {"type": "number"},
                    "floor_applied": {"type": "boolean"},
                    "net_fee": {"type": "number"}
                }
            },
            "status": {"type": "string"},
            "timestamp": {"type": "string"}
        },
        "required": ["net_fee", "offset_amount", "offset_pct", "breakdown", "status", "timestamp"]
    }
}


def management_fee_offset(**kwargs: Any) -> dict:
    """Calculate net management fee after applying GP fee offsets.

    Implements the standard ILPA fee offset mechanism:
    1. Identify total offset-eligible income: transaction fees + advisory income
    2. Apply offset rate: offset_amount = total_eligible * offset_rate
    3. Net fee = max(0, base_fee - offset_amount)

    The net fee is floored at zero — offsets can eliminate the management fee
    entirely but cannot create a fee credit payable to LPs (that would require
    separate excess offset carry-forward accounting, not implemented here).

    Args:
        **kwargs: Keyword arguments containing:
            base_fee (float): Gross management fee in dollars.
            transaction_fees_earned (float): Closing/transaction fees earned by GP.
            advisory_income (float): Monitoring and advisory fees earned by GP.
            offset_rate (float, optional): Offset fraction, default 0.80.

    Returns:
        dict: Contains:
            - status (str): 'success' or 'error'
            - data (dict):
                - net_fee (float): Management fee after offset (>= 0)
                - offset_amount (float): Dollar amount of offset applied
                - offset_pct (float): offset_amount / base_fee * 100 (% reduction)
                - gross_fee_income (float): Total GP-earned fees before offset
                - breakdown (dict): Step-by-step calculation trace
            - timestamp (str): ISO 8601 UTC timestamp
    """
    try:
        base_fee: float = float(kwargs.get("base_fee", 0))
        transaction_fees: float = float(kwargs.get("transaction_fees_earned", 0))
        advisory_income: float = float(kwargs.get("advisory_income", 0))
        offset_rate: float = float(kwargs.get("offset_rate", 0.80))

        if base_fee < 0:
            raise ValueError(f"base_fee cannot be negative, got {base_fee}")
        if transaction_fees < 0:
            raise ValueError(f"transaction_fees_earned cannot be negative, got {transaction_fees}")
        if advisory_income < 0:
            raise ValueError(f"advisory_income cannot be negative, got {advisory_income}")
        if not (0.0 <= offset_rate <= 1.0):
            raise ValueError(
                f"offset_rate must be between 0.0 and 1.0, got {offset_rate}. "
                f"Use 0.80 for 80% offset."
            )

        total_gp_fee_income = round(transaction_fees + advisory_income, 6)
        total_offset_eligible = total_gp_fee_income  # All GP fees are offset-eligible by default

        offset_amount = round(total_offset_eligible * offset_rate, 6)
        net_fee_before_floor = round(base_fee - offset_amount, 6)
        floor_applied = net_fee_before_floor < 0
        net_fee = max(0.0, net_fee_before_floor)
        net_fee = round(net_fee, 6)

        # If floor was applied, the actual offset is capped at base_fee
        actual_offset_applied = min(offset_amount, base_fee)

        offset_pct = round(actual_offset_applied / base_fee * 100, 4) if base_fee > 0 else 0.0

        # Excess offset (when offset > base_fee) — informational only
        excess_offset = round(max(0.0, offset_amount - base_fee), 6)

        breakdown = {
            "base_fee": base_fee,
            "transaction_fees_earned": transaction_fees,
            "advisory_income": advisory_income,
            "total_gp_fee_income": total_gp_fee_income,
            "total_offset_eligible": total_offset_eligible,
            "offset_rate_applied": offset_rate,
            "offset_rate_pct": round(offset_rate * 100, 2),
            "gross_offset_computed": offset_amount,
            "net_fee_before_floor": net_fee_before_floor,
            "floor_applied": floor_applied,
            "actual_offset_applied": actual_offset_applied,
            "excess_offset_unused": excess_offset,
            "net_fee": net_fee,
        }

        result = {
            "net_fee": net_fee,
            "offset_amount": actual_offset_applied,
            "offset_pct": offset_pct,
            "gross_fee_income": total_gp_fee_income,
            "fee_reduction_dollars": round(base_fee - net_fee, 6),
            "breakdown": breakdown,
        }

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"management_fee_offset failed: {e}")
        _log_lesson(f"management_fee_offset: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    """Append an error lesson to the shared lessons log.

    Args:
        message: The lesson or error description to record.
    """
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        logger.warning("Could not write to logs/lessons.md")
