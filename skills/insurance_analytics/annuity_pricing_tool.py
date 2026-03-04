"""Life annuity pricing tool.

Prices whole-life and deferred-life annuities using a parametric Makeham-like
mortality curve and standard actuarial present value (APV) methodology.
"""
from __future__ import annotations

from typing import Any

from skills.utils import get_iso_timestamp, log_lesson

TOOL_META: dict[str, Any] = {
    "name": "annuity_pricing_tool",
    "description": (
        "Prices whole-life and deferred-life annuities-due using a simple mortality model "
        "calibrated to approximate 2017 CSO rates. Returns annuity factor, present value, "
        "and break-even analysis metrics."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "age": {
                "type": "integer",
                "description": "Annuitant's current attained age. Must be 0–100.",
                "minimum": 0,
                "maximum": 100,
            },
            "gender": {
                "type": "string",
                "enum": ["male", "female"],
                "description": "Gender for mortality curve selection.",
            },
            "discount_rate_pct": {
                "type": "number",
                "description": "Annual discount rate as a percentage (e.g., 4.0 = 4.0%). Must be >= 0.",
                "minimum": 0.0,
            },
            "payment_amount": {
                "type": "number",
                "description": "Annual payment amount per period. Must be > 0.",
                "default": 1.0,
                "exclusiveMinimum": 0.0,
            },
            "annuity_type": {
                "type": "string",
                "enum": ["immediate", "deferred"],
                "description": "Annuity-immediate starts next period; deferred starts after deferral_years.",
                "default": "immediate",
            },
            "deferral_years": {
                "type": "integer",
                "description": "Years before first payment for a deferred annuity. Must be >= 0.",
                "default": 0,
                "minimum": 0,
            },
        },
        "required": ["age", "gender", "discount_rate_pct"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "annuity_present_value": {
                "type": "number",
                "description": "Present value of the annuity stream = annuity_factor × payment_amount.",
            },
            "annuity_factor": {
                "type": "number",
                "description": "ä_x (or ä_{x:n|}) — the actuarial present value per unit of payment.",
            },
            "survival_to_first_payment_pct": {
                "type": "number",
                "description": "Probability of surviving to the first payment date (deferred annuities).",
            },
            "break_even_years": {
                "type": "number",
                "description": "Number of payments needed to recover the purchase price at the discount rate.",
            },
            "implied_yield_pct": {
                "type": "number",
                "description": "The discount rate used in pricing (echoed back for transparency).",
            },
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def _qx_model(age: int, gender: str) -> float:
    """Parametric mortality rate approximating 2017 CSO aggregate.

    Uses a Makeham-inspired formula:
      qx = A + B * exp(c * (age - 30))   for age in [0, 120]
    Calibrated to approximate CSO aggregate rates for male/female.

    Args:
        age: Attained age.
        gender: "male" or "female".

    Returns:
        Annual probability of death (clamped to [0.0, 1.0]).
    """
    import math

    if gender == "female":
        a, b, c = 0.00030, 0.000050, 0.095
    else:
        a, b, c = 0.00040, 0.000060, 0.098

    qx = a + b * math.exp(c * max(age - 30, 0))
    return min(max(qx, 0.0), 1.0)


def annuity_pricing_tool(
    age: int,
    gender: str,
    discount_rate_pct: float,
    payment_amount: float = 1.0,
    annuity_type: str = "immediate",
    deferral_years: int = 0,
    **_: Any,
) -> dict[str, Any]:
    """Price a whole-life or deferred-life annuity-due (payments at start of each year).

    Annuity-due factor:
      ä_x = sum_{t=0}^{omega-x} v^t * t_p_x
    where v = 1/(1+i) and t_p_x = survival probability from age x to x+t.

    For a deferred annuity (ä_{x+d}), payments begin after deferral_years:
      ä_{x|d} = d_p_x * v^d * ä_{x+d}

    Args:
        age: Annuitant's attained age (0–100).
        gender: "male" or "female".
        discount_rate_pct: Annual valuation discount rate %. Must be >= 0.
        payment_amount: Annual payment per period; default 1.0.
        annuity_type: "immediate" or "deferred"; default "immediate".
        deferral_years: Years to first payment for deferred annuity; default 0.

    Returns:
        dict with status "success" and annuity pricing metrics, or status "error".
    """
    try:
        if age < 0 or age > 100:
            raise ValueError(f"age must be 0–100, got {age}")
        if discount_rate_pct < 0:
            raise ValueError(f"discount_rate_pct must be >= 0, got {discount_rate_pct}")
        if payment_amount <= 0:
            raise ValueError(f"payment_amount must be positive, got {payment_amount}")
        if deferral_years < 0:
            raise ValueError(f"deferral_years must be >= 0, got {deferral_years}")

        gender = gender.lower().strip()
        rate = discount_rate_pct / 100.0
        v = 1.0 / (1.0 + rate) if rate > 0 else 1.0  # discount factor per period

        max_age = 121
        payment_start = deferral_years if annuity_type == "deferred" else 0

        # Build t_p_x survival path and accumulate annuity factor
        survival = 1.0
        annuity_factor = 0.0
        survival_to_first_payment = 1.0

        for t in range(max_age - age):
            current_age = age + t
            if current_age >= max_age:
                break

            if t == payment_start:
                survival_to_first_payment = survival

            if t >= payment_start:
                discount = v ** t
                annuity_factor += survival * discount

            qx = _qx_model(current_age, gender)
            survival *= (1.0 - qx)

            if survival < 1e-7:
                break

        annuity_present_value = annuity_factor * payment_amount

        # Break-even: present value of payment stream = purchase price => solve for n
        # Approx: n = APV / payment_amount (in a certain-payment context)
        break_even_years = annuity_factor  # factor already = APV per unit payment

        return {
            "status": "success",
            "annuity_present_value": round(annuity_present_value, 2),
            "annuity_factor": round(annuity_factor, 4),
            "survival_to_first_payment_pct": round(survival_to_first_payment * 100, 4),
            "break_even_years": round(break_even_years, 2),
            "implied_yield_pct": round(discount_rate_pct, 3),
            "timestamp": get_iso_timestamp(),
        }
    except (ValueError, TypeError, ZeroDivisionError, ImportError) as exc:
        log_lesson(f"annuity_pricing_tool: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": get_iso_timestamp()}
