"""
Executive Smary: Estimates emergency fund needs based on expenses and household risk.
Inputs: monthly_expenses (float), income_stability (str), dependents (int), existing_savings (float)
Outputs: target_months (int), target_amount (float), current_coverage_months (float), monthly_savings_to_goal (float)
MCP Tool Name: emergency_fund_calculator
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

STABILITY_MONTHS = {
    "stable": 3,
    "variable": 6,
    "freelance": 9,
}

TOOL_META = {
    "name": "emergency_fund_calculator",
    "description": (
        "Determines the ideal emergency fund amount by weighing monthly expenses, income "
        "stability, and dependents while highlighting current coverage gaps."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "monthly_expenses": {
                "type": "number",
                "description": "Average essential monthly expenses in dollars, must be positive.",
            },
            "income_stability": {
                "type": "string",
                "description": "Job income stability: stable, variable, or freelance.",
            },
            "dependents": {
                "type": "number",
                "description": "Number of people relying on this income, must be non-negative.",
            },
            "existing_savings": {
                "type": "number",
                "description": "Liquid savings already available for emergencies, non-negative.",
            },
        },
        "required": ["monthly_expenses", "income_stability", "dependents", "existing_savings"],
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


def emergency_fund_calculator(**kwargs: Any) -> dict:
    """Recommend an emergency fund target and contribution rate."""
    try:
        monthly_expenses = float(kwargs["monthly_expenses"])
        income_stability = str(kwargs["income_stability"]).strip().lower()
        dependents = int(kwargs["dependents"])
        existing_savings = float(kwargs["existing_savings"])

        if monthly_expenses <= 0:
            raise ValueError("monthly_expenses must be positive")
        if income_stability not in STABILITY_MONTHS:
            raise ValueError("income_stability must be stable, variable, or freelance")
        if dependents < 0:
            raise ValueError("dependents must be non-negative")
        if existing_savings < 0:
            raise ValueError("existing_savings must be non-negative")

        base_months = STABILITY_MONTHS[income_stability]
        dependent_adjustment = min(dependents, 3)
        target_months = base_months + dependent_adjustment
        if income_stability == "freelance":
            target_months = min(12, target_months + 3)
        target_months = min(max(target_months, 3), 12)

        target_amount = monthly_expenses * target_months
        current_coverage_months = existing_savings / monthly_expenses
        gap = max(target_amount - existing_savings, 0.0)
        monthly_savings_to_goal = gap / 12 if gap > 0 else 0.0

        return {
            "status": "success",
            "data": {
                "target_months": target_months,
                "target_amount": target_amount,
                "current_coverage_months": current_coverage_months,
                "monthly_savings_to_goal": monthly_savings_to_goal,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"emergency_fund_calculator failed: {e}")
        _log_lesson(f"emergency_fund_calculator: {e}")
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
