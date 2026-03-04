"""Estimate Social Security retirement benefits based on average monthly earnings.

MCP Tool Name: social_security_benefit_estimator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

# 2024 PIA bend points
_BEND_POINT_1 = 1174  # 90% of first $1,174
_BEND_POINT_2 = 7078  # 32% of $1,174 to $7,078; 15% above $7,078

TOOL_META: dict[str, Any] = {
    "name": "social_security_benefit_estimator",
    "description": "Estimate Social Security retirement benefits from average indexed monthly earnings (AIME). Calculates Primary Insurance Amount (PIA) and adjusts for early/late claiming.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "avg_monthly_earnings": {
                "type": "number",
                "description": "Average Indexed Monthly Earnings (AIME). Can estimate as: (average annual earnings over best 35 years) / 12.",
            },
            "full_retirement_age": {
                "type": "integer",
                "description": "Full retirement age (FRA). 67 for those born 1960+, 66 for earlier cohorts.",
                "default": 67,
            },
            "claiming_age": {
                "type": "integer",
                "description": "Age at which benefits are claimed (62-70).",
                "default": 67,
            },
        },
        "required": ["avg_monthly_earnings"],
    },
}


def social_security_benefit_estimator(
    avg_monthly_earnings: float,
    full_retirement_age: int = 67,
    claiming_age: int = 67,
) -> dict[str, Any]:
    """Estimate Social Security retirement benefits."""
    try:
        if claiming_age < 62 or claiming_age > 70:
            return {
                "status": "error",
                "data": {"error": "Claiming age must be between 62 and 70."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        aime = avg_monthly_earnings

        # Calculate PIA from bend points
        if aime <= _BEND_POINT_1:
            pia = aime * 0.90
        elif aime <= _BEND_POINT_2:
            pia = _BEND_POINT_1 * 0.90 + (aime - _BEND_POINT_1) * 0.32
        else:
            pia = _BEND_POINT_1 * 0.90 + (_BEND_POINT_2 - _BEND_POINT_1) * 0.32 + (aime - _BEND_POINT_2) * 0.15

        # Adjustment for early/late claiming
        months_diff = (claiming_age - full_retirement_age) * 12

        if months_diff < 0:
            # Early claiming reduction
            # First 36 months: 5/9 of 1% per month = ~6.67% per year
            # Beyond 36 months: 5/12 of 1% per month = 5% per year
            early_months = abs(months_diff)
            if early_months <= 36:
                reduction = early_months * (5 / 900)
            else:
                reduction = 36 * (5 / 900) + (early_months - 36) * (5 / 1200)
            adjusted_pia = pia * (1 - reduction)
            adjustment_desc = f"{reduction*100:.1f}% reduction for claiming {abs(months_diff)} months early"
        elif months_diff > 0:
            # Delayed retirement credits: 8% per year = 2/3 of 1% per month
            credit = months_diff * (2 / 300)
            adjusted_pia = pia * (1 + credit)
            adjustment_desc = f"{credit*100:.1f}% increase for delaying {months_diff} months past FRA"
        else:
            adjusted_pia = pia
            adjustment_desc = "Claiming at full retirement age — no adjustment"

        # Calculate at different ages for comparison
        scenarios: list[dict[str, Any]] = []
        for age in [62, 65, full_retirement_age, 70]:
            m_diff = (age - full_retirement_age) * 12
            if m_diff < 0:
                early = abs(m_diff)
                if early <= 36:
                    red = early * (5 / 900)
                else:
                    red = 36 * (5 / 900) + (early - 36) * (5 / 1200)
                amt = pia * (1 - red)
            elif m_diff > 0:
                cred = m_diff * (2 / 300)
                amt = pia * (1 + cred)
            else:
                amt = pia
            scenarios.append({
                "claiming_age": age,
                "monthly_benefit": round(amt, 2),
                "annual_benefit": round(amt * 12, 2),
            })

        return {
            "status": "ok",
            "data": {
                "aime": round(aime, 2),
                "pia_at_fra": round(pia, 2),
                "claiming_age": claiming_age,
                "full_retirement_age": full_retirement_age,
                "adjusted_monthly_benefit": round(adjusted_pia, 2),
                "adjusted_annual_benefit": round(adjusted_pia * 12, 2),
                "adjustment": adjustment_desc,
                "scenarios": scenarios,
                "note": "Uses 2024 bend points ($1,174 / $7,078). Actual benefits depend on your earnings record, "
                "COLAs, and the year you turn 62. This is an estimate — check ssa.gov/myaccount for personalized projections.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
