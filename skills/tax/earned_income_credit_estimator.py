"""Estimate the Earned Income Tax Credit (EITC / EIC).

MCP Tool Name: earned_income_credit_estimator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "earned_income_credit_estimator",
    "description": "Estimate the Earned Income Tax Credit (EITC) based on earned income, number of qualifying children, and filing status. Uses 2024 EIC parameters.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "earned_income": {
                "type": "number",
                "description": "Total earned income (wages, salaries, self-employment) in USD.",
            },
            "num_qualifying_children": {
                "type": "integer",
                "description": "Number of qualifying children (0-3+).",
                "default": 0,
            },
            "filing_status": {
                "type": "string",
                "description": "Filing status.",
                "enum": ["single", "married_filing_jointly"],
                "default": "single",
            },
        },
        "required": ["earned_income"],
    },
}

# 2024 EIC parameters: (credit_rate, phase_in_end, max_credit, phase_out_start_single, phase_out_start_mfj, phase_out_rate)
_EIC_PARAMS = {
    0: {
        "credit_rate": 0.0765,
        "phase_in_end": 7840,
        "max_credit": 632,
        "phase_out_start_single": 9800,
        "phase_out_start_mfj": 16370,
        "phase_out_rate": 0.0765,
        "income_limit_single": 18591,
        "income_limit_mfj": 25161,
    },
    1: {
        "credit_rate": 0.34,
        "phase_in_end": 11750,
        "max_credit": 3995,
        "phase_out_start_single": 20600,
        "phase_out_start_mfj": 27180,
        "phase_out_rate": 0.1598,
        "income_limit_single": 46560,
        "income_limit_mfj": 53120,
    },
    2: {
        "credit_rate": 0.40,
        "phase_in_end": 16510,
        "max_credit": 6604,
        "phase_out_start_single": 20600,
        "phase_out_start_mfj": 27180,
        "phase_out_rate": 0.2106,
        "income_limit_single": 52918,
        "income_limit_mfj": 59478,
    },
    3: {
        "credit_rate": 0.45,
        "phase_in_end": 16510,
        "max_credit": 7430,
        "phase_out_start_single": 20600,
        "phase_out_start_mfj": 27180,
        "phase_out_rate": 0.2106,
        "income_limit_single": 56838,
        "income_limit_mfj": 63398,
    },
}


def earned_income_credit_estimator(
    earned_income: float,
    num_qualifying_children: int = 0,
    filing_status: str = "single",
) -> dict[str, Any]:
    """Estimate the Earned Income Tax Credit."""
    try:
        filing_status = filing_status.lower().strip()
        if filing_status not in ("single", "married_filing_jointly"):
            return {
                "status": "error",
                "data": {"error": "EIC filing_status must be 'single' or 'married_filing_jointly'. MFS cannot claim EIC."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        children_key = min(num_qualifying_children, 3)
        params = _EIC_PARAMS[children_key]

        is_mfj = filing_status == "married_filing_jointly"
        phase_out_start = params["phase_out_start_mfj"] if is_mfj else params["phase_out_start_single"]
        income_limit = params["income_limit_mfj"] if is_mfj else params["income_limit_single"]

        if earned_income < 0 or earned_income > income_limit:
            credit = 0.0
            phase = "over_limit" if earned_income > 0 else "no_income"
        elif earned_income <= params["phase_in_end"]:
            # Phase-in: credit increases with income
            credit = earned_income * params["credit_rate"]
            phase = "phase_in"
        elif earned_income <= phase_out_start:
            # Plateau: max credit
            credit = params["max_credit"]
            phase = "plateau"
        else:
            # Phase-out: credit decreases
            reduction = (earned_income - phase_out_start) * params["phase_out_rate"]
            credit = max(params["max_credit"] - reduction, 0)
            phase = "phase_out"

        credit = round(min(credit, params["max_credit"]), 2)

        return {
            "status": "ok",
            "data": {
                "earned_income": round(earned_income, 2),
                "num_qualifying_children": num_qualifying_children,
                "filing_status": filing_status,
                "estimated_eic": credit,
                "max_possible_credit": params["max_credit"],
                "phase": phase,
                "income_limit": income_limit,
                "note": "EIC is fully refundable. Investment income must be $11,600 or less to qualify.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
