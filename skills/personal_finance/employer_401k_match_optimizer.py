"""
Executive Smary: Maximizes employer 401(k) match capture based on salary and plan limits.
Inputs: salary (float), employer_match_pct (float), employer_match_cap_pct (float), current_contribution_pct (float), annual_limit (float)
Outputs: optimal_contribution_pct (float), free_money_captured (float), annual_match_value (float), contribution_amount (float), remaining_match (float)
MCP Tool Name: employer_401k_match_optimizer
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "employer_401k_match_optimizer",
    "description": (
        "Evaluates contribution rates needed to earn the full employer match while "
        "respecting IRS limits and highlights remaining match dollars on the table."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "salary": {
                "type": "number",
                "description": "Gross annual salary eligible for the 401(k) plan.",
            },
            "employer_match_pct": {
                "type": "number",
                "description": "Employer match percentage (e.g., 0.5 for 50% match).",
            },
            "employer_match_cap_pct": {
                "type": "number",
                "description": "Maximum salary percentage the employer will match.",
            },
            "current_contribution_pct": {
                "type": "number",
                "description": "Employee's current contribution percentage of salary.",
            },
            "annual_limit": {
                "type": "number",
                "description": "IRS annual contribution limit in dollars.",
            },
        },
        "required": [
            "salary",
            "employer_match_pct",
            "employer_match_cap_pct",
            "current_contribution_pct",
            "annual_limit",
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


def employer_401k_match_optimizer(**kwargs: Any) -> dict:
    """Suggest contribution rates to maximize employer match and quantify gaps."""
    try:
        salary = float(kwargs["salary"])
        match_pct = float(kwargs["employer_match_pct"])
        match_cap_pct = float(kwargs["employer_match_cap_pct"])
        current_pct = float(kwargs["current_contribution_pct"])
        annual_limit = float(kwargs["annual_limit"])

        if salary <= 0 or annual_limit <= 0:
            raise ValueError("salary and annual_limit must be positive")
        if match_pct < 0 or match_cap_pct < 0 or current_pct < 0:
            raise ValueError("percentages must be non-negative")

        max_contribution_pct = min(annual_limit / salary * 100, 100)
        optimal_pct = min(match_cap_pct, max_contribution_pct)
        contribution_amount = salary * min(current_pct, max_contribution_pct) / 100
        optimal_contribution_amount = salary * optimal_pct / 100
        match_base_pct = min(current_pct, match_cap_pct)
        annual_match_value = salary * match_base_pct / 100 * match_pct
        full_match_value = salary * match_cap_pct / 100 * match_pct
        remaining_match = max(full_match_value - annual_match_value, 0.0)

        return {
            "status": "success",
            "data": {
                "optimal_contribution_pct": optimal_pct,
                "free_money_captured": annual_match_value,
                "annual_match_value": annual_match_value,
                "contribution_amount": contribution_amount,
                "remaining_match": remaining_match,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"employer_401k_match_optimizer failed: {e}")
        _log_lesson(f"employer_401k_match_optimizer: {e}")
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
