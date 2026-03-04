"""
Executive Smary: Projects retirement balances with real and nominal values year by year.
Inputs: current_age (int), retirement_age (int), current_balance (float), annual_contribution (float), annual_return (float), inflation_rate (float)
Outputs: balance_at_retirement (dict), year_by_year_projection (list), shortfall_analysis (dict)
MCP Tool Name: retirement_savings_projector
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "retirement_savings_projector",
    "description": (
        "Forecasts retirement savings from current age to retirement, reporting nominal "
        "and inflation-adjusted balances plus a 4% rule shortfall analysis."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "current_age": {
                "type": "number",
                "description": "Current age in years, must be non-negative.",
            },
            "retirement_age": {
                "type": "number",
                "description": "Planned retirement age in years, must exceed current_age.",
            },
            "current_balance": {
                "type": "number",
                "description": "Existing retirement savings in dollars.",
            },
            "annual_contribution": {
                "type": "number",
                "description": "Annual contribution amount in dollars (pre-inflation).",
            },
            "annual_return": {
                "type": "number",
                "description": "Expected annual investment return as decimal.",
            },
            "inflation_rate": {
                "type": "number",
                "description": "Estimated annual inflation rate as decimal.",
            },
        },
        "required": [
            "current_age",
            "retirement_age",
            "current_balance",
            "annual_contribution",
            "annual_return",
            "inflation_rate",
        ],
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


def retirement_savings_projector(**kwargs: Any) -> dict:
    """Project nominal and real balances through retirement age."""
    try:
        current_age = int(kwargs["current_age"])
        retirement_age = int(kwargs["retirement_age"])
        current_balance = float(kwargs["current_balance"])
        annual_contribution = float(kwargs["annual_contribution"])
        annual_return = float(kwargs["annual_return"])
        inflation_rate = float(kwargs["inflation_rate"])

        if current_age < 0:
            raise ValueError("current_age must be non-negative")
        if retirement_age <= current_age:
            raise ValueError("retirement_age must exceed current_age")
        if current_balance < 0 or annual_contribution < 0:
            raise ValueError("balances and contributions must be non-negative")

        years = retirement_age - current_age
        projection = []
        nominal_balance = current_balance
        real_balance = current_balance

        for year in range(1, years + 1):
            nominal_balance = nominal_balance * (1 + annual_return) + annual_contribution
            real_balance = real_balance * (1 + annual_return) / (1 + inflation_rate) + (
                annual_contribution / (1 + inflation_rate) ** year
            )
            projection.append(
                {
                    "age": current_age + year,
                    "nominal_balance": nominal_balance,
                    "real_balance": real_balance,
                    "contributions_to_date": annual_contribution * year,
                }
            )

        target_income = annual_contribution or 1.0
        target_balance = target_income * 25
        projected_real = projection[-1]["real_balance"] if projection else real_balance
        shortfall = max(target_balance - projected_real, 0.0)
        status = "Ahead" if shortfall == 0 else "Behind"
        catch_up = shortfall / years if years > 0 else shortfall

        return {
            "status": "success",
            "data": {
                "balance_at_retirement": {
                    "nominal": projection[-1]["nominal_balance"] if projection else nominal_balance,
                    "real": projected_real,
                },
                "year_by_year_projection": projection,
                "shortfall_analysis": {
                    "target_balance_4pct": target_balance,
                    "projected_shortfall": shortfall,
                    "additional_annual_savings_needed": catch_up,
                    "status": status,
                },
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"retirement_savings_projector failed: {e}")
        _log_lesson(f"retirement_savings_projector: {e}")
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
