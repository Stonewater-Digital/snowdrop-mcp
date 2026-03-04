"""
Executive Smary: Estimates Social Security benefits based on earnings history and claiming age.
Inputs: average_indexed_monthly_earnings (float), birth_year (int), planned_claiming_age (int)
Outputs: monthly_benefit (float), annual_benefit (float), cumulative_by_age_85 (float), breakeven_vs_62 (float), pia (float), bend_points (list)
MCP Tool Name: social_security_estimator
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

BEND_POINTS_2024 = [1174, 5885]

TOOL_META = {
    "name": "social_security_estimator",
    "description": (
        "Approximates the primary insurance amount (PIA) and adjusts benefits for early "
        "or delayed claiming relative to full retirement age."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "average_indexed_monthly_earnings": {
                "type": "number",
                "description": "Average indexed monthly earnings (AIME) in dollars.",
            },
            "birth_year": {
                "type": "number",
                "description": "Birth year for FRA calculation.",
            },
            "planned_claiming_age": {
                "type": "number",
                "description": "Age at which benefits will be claimed (62-70).",
            },
        },
        "required": ["average_indexed_monthly_earnings", "birth_year", "planned_claiming_age"],
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


def social_security_estimator(**kwargs: Any) -> dict:
    """Estimate Social Security benefits using 2024 bend points and claiming adjustments."""
    try:
        aime = float(kwargs["average_indexed_monthly_earnings"])
        birth_year = int(kwargs["birth_year"])
        claiming_age = int(kwargs["planned_claiming_age"])

        if aime <= 0:
            raise ValueError("average_indexed_monthly_earnings must be positive")
        if claiming_age < 62 or claiming_age > 70:
            raise ValueError("planned_claiming_age must be between 62 and 70")

        fra = 67 if birth_year >= 1960 else 66
        pia = _calculate_pia(aime)
        adjusted_benefit = _apply_claiming_adjustment(pia, fra, claiming_age)
        annual_benefit = adjusted_benefit * 12
        cumulative_by_age_85 = annual_benefit * max(85 - claiming_age, 0)
        breakeven_vs_62 = _breakeven_age(pia, fra)

        return {
            "status": "success",
            "data": {
                "monthly_benefit": adjusted_benefit,
                "annual_benefit": annual_benefit,
                "cumulative_by_age_85": cumulative_by_age_85,
                "breakeven_vs_62": breakeven_vs_62,
                "pia": pia,
                "bend_points": BEND_POINTS_2024,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"social_security_estimator failed: {e}")
        _log_lesson(f"social_security_estimator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _calculate_pia(aime: float) -> float:
    first, second = BEND_POINTS_2024
    if aime <= first:
        return aime * 0.9
    if aime <= second:
        return first * 0.9 + (aime - first) * 0.32
    return first * 0.9 + (second - first) * 0.32 + (aime - second) * 0.15


def _apply_claiming_adjustment(pia: float, fra: int, claiming_age: int) -> float:
    months_diff = (claiming_age - fra) * 12
    if months_diff == 0:
        return pia
    if months_diff < 0:
        months = abs(months_diff)
        reduction = min(months, 36) * (5 / 9 / 100) + max(months - 36, 0) * (5 / 12 / 100)
        return pia * (1 - reduction)
    delay_bonus = months_diff * (2 / 3 / 100)
    return pia * (1 + delay_bonus)


def _breakeven_age(pia: float, fra: int) -> float:
    early = _apply_claiming_adjustment(pia, fra, 62)
    delay = _apply_claiming_adjustment(pia, fra, 70)
    extra = delay - early
    if extra <= 0:
        return fra
    years = (pia * 12 * (70 - 62)) / (extra * 12)
    return 62 + years


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
