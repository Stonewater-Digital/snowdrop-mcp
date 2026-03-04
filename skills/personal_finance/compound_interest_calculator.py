"""
Executive Smary: Projects the future value of an investment with periodic compounding.
Inputs: principal (float), annual_rate (float), compounds_per_year (int), years (float)
Outputs: future_value (float), total_interest (float), effective_annual_rate (float), growth_schedule (list)
MCP Tool Name: compound_interest_calculator
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "compound_interest_calculator",
    "description": (
        "Calculates the future value of an investment with compound interest, returning "
        "effective annual yield and year-by-year growth."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "principal": {
                "type": "number",
                "description": "Initial amount invested in dollars, must be non-negative.",
            },
            "annual_rate": {
                "type": "number",
                "description": "Nominal annual interest rate expressed as decimal (e.g., 0.05).",
            },
            "compounds_per_year": {
                "type": "number",
                "description": "Number of compounding periods per year (1 for annual, 12 for monthly).",
            },
            "years": {
                "type": "number",
                "description": "Investment horizon in years, can be fractional.",
            },
        },
        "required": ["principal", "annual_rate", "compounds_per_year", "years"],
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


def compound_interest_calculator(**kwargs: Any) -> dict:
    """Compute compound growth, effective annual rate, and yearly balances."""
    try:
        principal = float(kwargs["principal"])
        annual_rate = float(kwargs["annual_rate"])
        compounds_per_year = int(kwargs["compounds_per_year"])
        years = float(kwargs["years"])

        if principal < 0:
            raise ValueError("principal must be non-negative")
        if compounds_per_year <= 0:
            raise ValueError("compounds_per_year must be positive")
        if years < 0:
            raise ValueError("years must be non-negative")

        periods = compounds_per_year * years
        period_rate = annual_rate / compounds_per_year
        future_value = principal * (1 + period_rate) ** periods
        total_interest = future_value - principal
        effective_annual_rate = (1 + period_rate) ** compounds_per_year - 1

        full_years = int(years)
        remainder = years - full_years
        schedule = []
        for year in range(1, full_years + 1):
            balance = principal * (1 + period_rate) ** (compounds_per_year * year)
            schedule.append(
                {
                    "year": year,
                    "balance": balance,
                    "interest_earned": balance - principal,
                }
            )
        if remainder > 1e-9:
            partial_periods = compounds_per_year * years
            balance = principal * (1 + period_rate) ** partial_periods
            schedule.append(
                {
                    "year": years,
                    "balance": balance,
                    "interest_earned": balance - principal,
                }
            )

        return {
            "status": "success",
            "data": {
                "future_value": future_value,
                "total_interest": total_interest,
                "effective_annual_rate": effective_annual_rate,
                "growth_schedule": schedule,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"compound_interest_calculator failed: {e}")
        _log_lesson(f"compound_interest_calculator: {e}")
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
