"""Estimate auto insurance premium with age and accident adjustments.

MCP Tool Name: auto_insurance_premium_estimator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "auto_insurance_premium_estimator",
    "description": "Estimate auto insurance annual premium based on vehicle value, driver age, experience, accident history, and coverage type.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "vehicle_value": {"type": "number", "description": "Current vehicle value."},
            "driver_age": {"type": "integer", "description": "Driver's age."},
            "years_licensed": {"type": "integer", "description": "Years holding a valid license."},
            "accidents": {"type": "integer", "description": "Number of at-fault accidents in past 5 years (default 0).", "default": 0},
            "coverage_type": {
                "type": "string",
                "description": "Coverage type: 'full' (comprehensive+collision) or 'liability' (default 'full').",
                "default": "full",
            },
        },
        "required": ["vehicle_value", "driver_age", "years_licensed"],
    },
}


def auto_insurance_premium_estimator(
    vehicle_value: float,
    driver_age: int,
    years_licensed: int,
    accidents: int = 0,
    coverage_type: str = "full",
) -> dict[str, Any]:
    """Estimate auto insurance premium."""
    try:
        # Base rate as percentage of vehicle value
        if coverage_type.lower() == "full":
            base_rate = 0.04  # 4% of vehicle value
        else:
            base_rate = 0.015  # 1.5% for liability only

        base_premium = vehicle_value * base_rate

        # Age adjustment
        if driver_age < 25:
            age_factor = 1.50  # young driver surcharge
        elif driver_age > 65:
            age_factor = 1.20  # senior surcharge
        else:
            age_factor = 1.0

        # Experience discount
        if years_licensed >= 10:
            experience_factor = 0.90
        elif years_licensed >= 5:
            experience_factor = 0.95
        else:
            experience_factor = 1.0

        # Accident surcharge: ~25% per accident
        accident_factor = 1.0 + (accidents * 0.25)

        estimated_premium = base_premium * age_factor * experience_factor * accident_factor
        monthly = estimated_premium / 12

        return {
            "status": "ok",
            "data": {
                "vehicle_value": vehicle_value,
                "driver_age": driver_age,
                "years_licensed": years_licensed,
                "accidents": accidents,
                "coverage_type": coverage_type,
                "base_annual_premium": round(base_premium, 2),
                "age_factor": age_factor,
                "experience_factor": experience_factor,
                "accident_factor": accident_factor,
                "estimated_annual_premium": round(estimated_premium, 2),
                "estimated_monthly_premium": round(monthly, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
