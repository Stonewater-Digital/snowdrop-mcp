"""Educational guide to the time value of money.

MCP Tool Name: time_value_of_money_guide
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "time_value_of_money_guide",
    "description": "Returns educational content on time value of money: PV, FV, annuities, perpetuities, and discount rates.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def time_value_of_money_guide() -> dict[str, Any]:
    """Returns educational content on the time value of money."""
    try:
        return {
            "status": "ok",
            "data": {
                "definition": "The Time Value of Money (TVM) is the foundational financial principle that a dollar today is worth more than a dollar in the future, because today's dollar can be invested to earn a return. TVM underpins all of finance — from bond pricing and stock valuation to mortgage calculations and retirement planning.",
                "key_concepts": [
                    "Money has a time dimension — the same amount is worth different values at different points in time",
                    "The discount rate reflects the opportunity cost of capital, risk, and inflation",
                    "Present value converts future cash flows to today's dollars; future value does the reverse",
                    "TVM is the foundation of DCF analysis, NPV, IRR, and nearly all valuation methods",
                ],
                "present_value": {
                    "formula": "PV = FV / (1 + r)^n, where FV = future value, r = discount rate per period, n = number of periods",
                    "meaning": "What a future sum of money is worth today, given a specific rate of return.",
                    "example": "$10,000 received in 5 years at a 6% discount rate: PV = $10,000 / (1.06)^5 = $7,473. You would be indifferent between $7,473 today and $10,000 in 5 years at 6%.",
                },
                "future_value": {
                    "formula": "FV = PV * (1 + r)^n",
                    "meaning": "What a current sum of money will be worth at a future date, given a specific rate of return.",
                    "example": "$5,000 invested today at 8% for 10 years: FV = $5,000 * (1.08)^10 = $10,795.",
                },
                "annuity": {
                    "definition": "A series of equal payments made at regular intervals over a specified period.",
                    "pv_formula": "PV = PMT * [(1 - (1 + r)^-n) / r], where PMT = payment per period",
                    "fv_formula": "FV = PMT * [((1 + r)^n - 1) / r]",
                    "ordinary_annuity": "Payments occur at the END of each period (most loans, bonds).",
                    "annuity_due": "Payments occur at the BEGINNING of each period (rent, insurance premiums). Worth more than ordinary annuity by a factor of (1 + r).",
                    "example": "$500/month for 20 years at 7% annual (0.583% monthly): FV = ~$260,000. Only $120,000 was contributed — the rest is compound growth.",
                },
                "perpetuity": {
                    "definition": "A stream of equal payments that continues forever (no end date).",
                    "formula": "PV = PMT / r",
                    "growing_perpetuity": "PV = PMT / (r - g), where g = constant growth rate per period. Requires r > g.",
                    "example": "An investment paying $1,000/year forever at a 5% discount rate: PV = $1,000 / 0.05 = $20,000.",
                    "applications": "Preferred stock valuation, Gordon Growth Model for stocks, endowment fund planning.",
                },
                "discount_rate": {
                    "definition": "The interest rate used to convert future cash flows to present values. Reflects the opportunity cost of capital and the riskiness of the cash flows.",
                    "components": [
                        "Risk-free rate (typically the Treasury yield for the relevant maturity)",
                        "Inflation premium (compensation for expected purchasing power loss)",
                        "Risk premium (compensation for uncertainty — higher for riskier cash flows)",
                        "Liquidity premium (compensation for inability to sell quickly)",
                    ],
                    "impact": "Higher discount rates reduce present values significantly. A 2% increase in discount rate can reduce a long-term investment's PV by 20-40%.",
                },
                "example": "Choosing between $50,000 today or $80,000 in 5 years. At a 10% discount rate: PV of $80,000 in 5 years = $80,000 / (1.10)^5 = $49,674. The lump sum today ($50,000) is slightly more valuable. At 8%, the PV is $54,450, making the future payment the better choice.",
                "common_mistakes": [
                    "Ignoring TVM entirely — comparing dollar amounts at different time periods without discounting",
                    "Using the wrong discount rate (too high or too low for the risk level)",
                    "Confusing nominal and real rates (not adjusting for inflation)",
                    "Mismatching periods — using an annual rate with monthly payments without converting",
                    "Forgetting that the discount rate itself can change over time",
                ],
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
