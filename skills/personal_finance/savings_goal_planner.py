"""
Executive Smary: Determines the monthly savings needed to reach a target within a timeframe.
Inputs: target_amount (float), current_savings (float), annual_rate (float), years (float)
Outputs: monthly_contribution (float), total_contributed (float), interest_earned (float), milestone_timeline (list)
MCP Tool Name: savings_goal_planner
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "savings_goal_planner",
    "description": (
        "Solves for the monthly contribution required to hit a savings goal given current "
        "balance, time horizon, and expected return, with annual milestones."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "target_amount": {
                "type": "number",
                "description": "Desired ending balance in dollars, must exceed zero.",
            },
            "current_savings": {
                "type": "number",
                "description": "Existing savings earmarked for the goal, non-negative dollars.",
            },
            "annual_rate": {
                "type": "number",
                "description": "Expected annual return as decimal (can be zero or negative).",
            },
            "years": {
                "type": "number",
                "description": "Years until goal, can be fractional but must be positive.",
            },
        },
        "required": ["target_amount", "current_savings", "annual_rate", "years"],
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


def savings_goal_planner(**kwargs: Any) -> dict:
    """Calculate monthly savings needed and project yearly milestones."""
    try:
        target = float(kwargs["target_amount"])
        current = float(kwargs["current_savings"])
        annual_rate = float(kwargs["annual_rate"])
        years = float(kwargs["years"])

        if target <= 0:
            raise ValueError("target_amount must be positive")
        if current < 0:
            raise ValueError("current_savings must be non-negative")
        if years <= 0:
            raise ValueError("years must be positive")

        months = int(round(years * 12))
        months = max(months, 1)
        monthly_rate = annual_rate / 12
        current_future_value = current * (1 + monthly_rate) ** months
        goal_gap = max(target - current_future_value, 0.0)

        if monthly_rate == 0:
            monthly_contribution = goal_gap / months if goal_gap > 0 else 0.0
            final_balance = current + monthly_contribution * months
        else:
            factor = ((1 + monthly_rate) ** months - 1) / monthly_rate
            monthly_contribution = goal_gap / factor if goal_gap > 0 else 0.0
            final_balance = current_future_value + monthly_contribution * factor

        total_contributed = monthly_contribution * months
        interest_earned = final_balance - (current + total_contributed)

        milestones = []
        balance = current
        for year in range(1, int(years) + 1):
            periods = year * 12
            if monthly_rate == 0:
                balance = current + monthly_contribution * periods
            else:
                balance = current * (1 + monthly_rate) ** periods + monthly_contribution * (
                    ((1 + monthly_rate) ** periods - 1) / monthly_rate
                )
            milestones.append(
                {
                    "year": year,
                    "projected_balance": balance,
                    "contributions_to_date": monthly_contribution * periods,
                }
            )

        if years - int(years) > 1e-9:
            periods = months
            milestones.append(
                {
                    "year": years,
                    "projected_balance": final_balance,
                    "contributions_to_date": total_contributed,
                }
            )

        return {
            "status": "success",
            "data": {
                "monthly_contribution": monthly_contribution,
                "total_contributed": total_contributed,
                "interest_earned": interest_earned,
                "milestone_timeline": milestones,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"savings_goal_planner failed: {e}")
        _log_lesson(f"savings_goal_planner: {e}")
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
