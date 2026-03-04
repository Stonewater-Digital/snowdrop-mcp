"""Insurance premium calculator.

Computes gross written premium from base rate, exposure units, and modifiers
following standard ISO/NCCI manual rating methodology.
"""
from __future__ import annotations

from typing import Any

from skills.utils import get_iso_timestamp, log_lesson

TOOL_META: dict[str, Any] = {
    "name": "premium_calculator",
    "description": (
        "Computes gross written premium from base rate, exposure units, experience modification, "
        "schedule credits, and other adjustments following standard manual rating methodology."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "base_rate": {
                "type": "number",
                "description": "Base rate per exposure unit (e.g., dollars per $100 of payroll, per vehicle, per unit).",
                "exclusiveMinimum": 0,
            },
            "exposure_units": {
                "type": "number",
                "description": "Number of exposure units (e.g., payroll in $100s, vehicle count, headcount).",
                "exclusiveMinimum": 0,
            },
            "experience_mod": {
                "type": "number",
                "description": "Experience modification factor (e-mod). 1.0 = unity; <1.0 = credit; >1.0 = debit. Typical range 0.50–2.50.",
                "default": 1.0,
                "exclusiveMinimum": 0,
            },
            "schedule_credits_pct": {
                "type": "number",
                "description": (
                    "Schedule rating adjustment as a signed percentage of experience-adjusted premium. "
                    "Positive = surcharge, negative = credit. Most states cap at ±25%."
                ),
                "default": 0.0,
                "minimum": -100.0,
                "maximum": 100.0,
            },
            "other_adjustments_pct": {
                "type": "number",
                "description": (
                    "Additional multiplicative adjustment as a signed percentage "
                    "(e.g., premium discount, expense constant). Applied after schedule factor."
                ),
                "default": 0.0,
                "minimum": -100.0,
                "maximum": 100.0,
            },
        },
        "required": ["base_rate", "exposure_units"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "manual_premium": {"type": "number", "description": "base_rate × exposure_units before any mods."},
            "experience_modified_premium": {"type": "number", "description": "Manual premium × experience_mod."},
            "schedule_factor": {"type": "number", "description": "Multiplicative factor from schedule_credits_pct."},
            "other_factor": {"type": "number", "description": "Multiplicative factor from other_adjustments_pct."},
            "gross_written_premium": {"type": "number", "description": "Final GWP after all modifiers."},
            "effective_rate_per_unit": {"type": "number", "description": "GWP ÷ exposure_units."},
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def premium_calculator(
    base_rate: float,
    exposure_units: float,
    experience_mod: float = 1.0,
    schedule_credits_pct: float = 0.0,
    other_adjustments_pct: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Compute gross written premium using standard manual rating steps.

    Rating sequence (ISO/NCCI methodology):
      1. Manual premium  = base_rate × exposure_units
      2. Experience-adjusted = manual_premium × experience_mod
      3. Schedule factor = 1 + schedule_credits_pct / 100
      4. Other factor    = 1 + other_adjustments_pct / 100
      5. GWP             = experience_adjusted × schedule_factor × other_factor

    Args:
        base_rate: Rate per exposure unit (must be > 0).
        exposure_units: Number of exposure units (must be > 0).
        experience_mod: Experience modification factor; default 1.0.
        schedule_credits_pct: Signed schedule adjustment %; default 0.0.
        other_adjustments_pct: Additional signed adjustment %; default 0.0.

    Returns:
        dict with status "success" and premium components, or status "error".
    """
    try:
        if base_rate <= 0:
            raise ValueError(f"base_rate must be positive, got {base_rate}")
        if exposure_units <= 0:
            raise ValueError(f"exposure_units must be positive, got {exposure_units}")
        if experience_mod <= 0:
            raise ValueError(f"experience_mod must be positive, got {experience_mod}")

        manual_premium = base_rate * exposure_units
        experience_adjusted = manual_premium * experience_mod
        schedule_factor = 1.0 + schedule_credits_pct / 100.0
        other_factor = 1.0 + other_adjustments_pct / 100.0

        if schedule_factor <= 0:
            raise ValueError(
                f"schedule_credits_pct={schedule_credits_pct} produces non-positive schedule_factor={schedule_factor}"
            )
        if other_factor <= 0:
            raise ValueError(
                f"other_adjustments_pct={other_adjustments_pct} produces non-positive other_factor={other_factor}"
            )

        gross_written_premium = experience_adjusted * schedule_factor * other_factor

        return {
            "status": "success",
            "manual_premium": round(manual_premium, 2),
            "experience_modified_premium": round(experience_adjusted, 2),
            "schedule_factor": round(schedule_factor, 4),
            "other_factor": round(other_factor, 4),
            "gross_written_premium": round(gross_written_premium, 2),
            "effective_rate_per_unit": round(gross_written_premium / exposure_units, 4),
            "timestamp": get_iso_timestamp(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as exc:
        log_lesson(f"premium_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": get_iso_timestamp()}
