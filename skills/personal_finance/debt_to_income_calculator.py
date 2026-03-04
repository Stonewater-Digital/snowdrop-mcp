"""
Executive Smary: Computes mortgage-ready front-end and back-end DTI ratios.
Inputs: monthly_debts (list), gross_monthly_income (float)
Outputs: front_end_dti (float), back_end_dti (float), qualification_status (dict), max_additional_debt (float)
MCP Tool Name: debt_to_income_calculator
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

logger = logging.getLogger("snowdrop.skills")

THRESHOLDS = {
    "conventional": {"front_end": 0.28, "back_end": 0.36},
    "fha": {"front_end": 0.31, "back_end": 0.43},
    "va": {"front_end": 0.0, "back_end": 0.41},
}

TOOL_META = {
    "name": "debt_to_income_calculator",
    "description": (
        "Evaluates monthly debt obligations relative to income for mortgage qualification "
        "across Conventional, FHA, and VA programs."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "monthly_debts": {
                "type": "array",
                "description": "List of debt items with type (housing/other) and amount.",
                "items": {"type": "object"},
            },
            "gross_monthly_income": {
                "type": "number",
                "description": "Household gross monthly income before taxes.",
            },
        },
        "required": ["monthly_debts", "gross_monthly_income"],
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


def debt_to_income_calculator(**kwargs: Any) -> dict:
    """Calculate DTI metrics and identify mortgage program eligibility."""
    try:
        debts_input = kwargs["monthly_debts"]
        income = float(kwargs["gross_monthly_income"])

        if income <= 0:
            raise ValueError("gross_monthly_income must be positive")
        if not isinstance(debts_input, list):
            raise ValueError("monthly_debts must be a list")

        debts: List[Dict[str, Any]] = []
        for item in debts_input:
            debt_type = str(item.get("type", "other")).lower()
            amount = float(item["amount"])
            if amount < 0:
                raise ValueError("debt amount must be non-negative")
            debts.append({"type": debt_type, "amount": amount})

        housing = sum(d["amount"] for d in debts if d["type"] == "housing")
        other = sum(d["amount"] for d in debts if d["type"] != "housing")
        total = housing + other
        front_end = housing / income
        back_end = total / income
        qualification_status = {
            program: (
                front_end <= limits["front_end"] if limits["front_end"] > 0 else True
            )
            and back_end <= limits["back_end"]
            for program, limits in THRESHOLDS.items()
        }
        max_back_end_allowance = income * 0.43
        max_additional_debt = max(max_back_end_allowance - total, 0.0)

        return {
            "status": "success",
            "data": {
                "front_end_dti": front_end,
                "back_end_dti": back_end,
                "qualification_status": qualification_status,
                "max_additional_debt": max_additional_debt,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"debt_to_income_calculator failed: {e}")
        _log_lesson(f"debt_to_income_calculator: {e}")
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
