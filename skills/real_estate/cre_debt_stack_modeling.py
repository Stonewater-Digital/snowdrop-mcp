"""
Executive Summary: Models a CRE capital stack with senior/mezz/equity tranches, blended cost of capital, and LTV per layer.
Inputs: total_value (float), loan_tranches (list of dicts: name, amount, rate, priority)
Outputs: dict with stack_table (list), blended_cost (float), total_ltv (float)
MCP Tool Name: cre_debt_stack_modeling
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "cre_debt_stack_modeling",
    "description": (
        "Models a commercial real estate capital stack with senior debt, mezzanine, "
        "and equity tranches. Calculates blended cost of capital, cumulative LTV per "
        "tranche, and flags structural risk (e.g., LTV > 80% for senior)."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "total_value": {
                "type": "number",
                "description": "Appraised or purchase price of the property (dollars)."
            },
            "loan_tranches": {
                "type": "array",
                "description": "List of debt/equity tranches ordered by waterfall priority.",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "amount": {"type": "number"},
                        "rate": {"type": "number", "description": "Annual interest/preferred rate as decimal (e.g., 0.065)."},
                        "priority": {"type": "integer", "description": "1 = most senior (paid first)."}
                    },
                    "required": ["name", "amount", "rate", "priority"]
                }
            }
        },
        "required": ["total_value", "loan_tranches"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "stack_table": {"type": "array"},
                    "blended_cost": {"type": "number"},
                    "total_ltv": {"type": "number"},
                    "total_debt": {"type": "number"},
                    "equity_amount": {"type": "number"},
                    "risk_flags": {"type": "array"}
                },
                "required": ["stack_table", "blended_cost", "total_ltv"]
            },
            "timestamp": {"type": "string"}
        },
        "required": ["status", "timestamp"]
    }
}

# CRE underwriting thresholds
SENIOR_LTV_LIMIT: float = 0.65       # 65% typical senior LTV ceiling
TOTAL_LTV_LIMIT: float = 0.80        # 80% total stack LTV warning threshold


def cre_debt_stack_modeling(
    total_value: float,
    loan_tranches: list[dict],
    **kwargs: Any
) -> dict:
    """Model a CRE capital stack, computing LTV and blended cost of capital.

    Tranches are sorted by ascending priority (1 = most senior). For each tranche,
    the cumulative LTV and annual interest cost are computed. Blended cost of capital
    is the weighted average rate across all debt tranches (equity treated as zero-rate
    unless explicitly given a preferred rate).

    Args:
        total_value: Property appraised value or purchase price in dollars.
        loan_tranches: List of tranche dicts, each requiring name (str), amount (float),
            rate (float as decimal), and priority (int, 1 = senior-most).
        **kwargs: Ignored extra keyword arguments for MCP compatibility.

    Returns:
        dict with keys: status, data (stack_table, blended_cost, total_ltv,
        total_debt, equity_amount, risk_flags), timestamp.

    Raises:
        ValueError: If total_value is non-positive or tranches list is empty.
    """
    try:
        total_value = float(total_value)
        if total_value <= 0:
            raise ValueError(f"total_value must be positive, got {total_value}")
        if not loan_tranches:
            raise ValueError("loan_tranches list cannot be empty.")

        # Validate and coerce each tranche
        coerced: list[dict] = []
        for i, t in enumerate(loan_tranches):
            if not isinstance(t, dict):
                raise ValueError(f"Tranche at index {i} must be a dict.")
            for field in ("name", "amount", "rate", "priority"):
                if field not in t:
                    raise ValueError(f"Tranche at index {i} missing required field '{field}'.")
            coerced.append({
                "name": str(t["name"]),
                "amount": float(t["amount"]),
                "rate": float(t["rate"]),
                "priority": int(t["priority"])
            })

        # Sort tranches senior-to-junior
        sorted_tranches = sorted(coerced, key=lambda x: x["priority"])

        stack_table: list[dict] = []
        cumulative_amount: float = 0.0
        total_interest_cost: float = 0.0
        risk_flags: list[str] = []

        for tranche in sorted_tranches:
            cumulative_amount += tranche["amount"]
            cumulative_ltv: float = cumulative_amount / total_value
            tranche_ltv: float = tranche["amount"] / total_value
            annual_interest: float = tranche["amount"] * tranche["rate"]
            total_interest_cost += annual_interest

            entry = {
                "name": tranche["name"],
                "amount": round(tranche["amount"], 2),
                "rate_pct": round(tranche["rate"] * 100, 3),
                "priority": tranche["priority"],
                "tranche_ltv_pct": round(tranche_ltv * 100, 2),
                "cumulative_ltv_pct": round(cumulative_ltv * 100, 2),
                "annual_interest": round(annual_interest, 2)
            }
            stack_table.append(entry)

            # Risk flag: senior tranche LTV > SENIOR_LTV_LIMIT
            if tranche["priority"] == 1 and tranche_ltv > SENIOR_LTV_LIMIT:
                risk_flags.append(
                    f"Senior tranche '{tranche['name']}' LTV of "
                    f"{tranche_ltv * 100:.1f}% exceeds {SENIOR_LTV_LIMIT * 100:.0f}% guideline."
                )

        total_debt: float = sum(t["amount"] for t in sorted_tranches)
        total_ltv: float = total_debt / total_value
        equity_amount: float = max(0.0, total_value - total_debt)

        if total_ltv > TOTAL_LTV_LIMIT:
            risk_flags.append(
                f"Total stack LTV of {total_ltv * 100:.1f}% exceeds "
                f"{TOTAL_LTV_LIMIT * 100:.0f}% underwriting threshold."
            )

        # Blended cost of capital (weighted average of all tranche rates by amount)
        blended_cost: float = total_interest_cost / total_debt if total_debt > 0 else 0.0

        result = {
            "stack_table": stack_table,
            "blended_cost": round(blended_cost * 100, 4),   # expressed as percent
            "blended_cost_decimal": round(blended_cost, 6),
            "total_ltv": round(total_ltv * 100, 2),          # expressed as percent
            "total_debt": round(total_debt, 2),
            "equity_amount": round(equity_amount, 2),
            "equity_pct": round((equity_amount / total_value) * 100, 2),
            "annual_debt_service": round(total_interest_cost, 2),
            "risk_flags": risk_flags,
            "total_value": total_value
        }

        logger.info(
            "cre_debt_stack_modeling: LTV=%.2f%%, blended_cost=%.3f%%, flags=%d",
            total_ltv * 100, blended_cost * 100, len(risk_flags)
        )

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except Exception as e:
        logger.error("cre_debt_stack_modeling failed: %s", e)
        _log_lesson(f"cre_debt_stack_modeling: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _log_lesson(message: str) -> None:
    """Append a lesson-learned entry to the shared lessons log.

    Args:
        message: Description of the error or lesson to record.
    """
    try:
        os.makedirs("logs", exist_ok=True)
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError as log_err:
        logger.warning("Could not write to lessons.md: %s", log_err)
