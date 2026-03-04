"""Calculate personal savings rate and classify financial health.

MCP Tool Name: savings_rate_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "savings_rate_calculator",
    "description": "Calculates savings rate as a percentage of gross income and classifies the result.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "gross_income": {
                "type": "number",
                "description": "Monthly or annual gross income in dollars.",
            },
            "total_savings": {
                "type": "number",
                "description": "Monthly or annual total savings/investments in dollars (same period as income).",
            },
        },
        "required": ["gross_income", "total_savings"],
    },
}


def savings_rate_calculator(gross_income: float, total_savings: float) -> dict[str, Any]:
    """Calculates savings rate and classifies financial health."""
    try:
        if gross_income <= 0:
            return {
                "status": "error",
                "data": {"error": "Gross income must be a positive number."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        rate = round((total_savings / gross_income) * 100, 2)

        if rate < 0:
            classification = "Negative (spending more than earning)"
            guidance = "Focus on reducing expenses or increasing income to stop depleting savings/taking on debt."
        elif rate < 5:
            classification = "Very Low"
            guidance = "Below the minimum recommended rate. Aim for at least 10-15%. Start with small automatic transfers."
        elif rate < 10:
            classification = "Below Average"
            guidance = "Below the U.S. average. Increase gradually by 1-2% every few months. Automate savings."
        elif rate < 15:
            classification = "Average"
            guidance = "Near the recommended minimum. Good start, but aim for 15-20% for a comfortable retirement."
        elif rate < 20:
            classification = "Good"
            guidance = "Solid savings rate. Meets most retirement planning recommendations. Consider optimizing tax-advantaged accounts."
        elif rate < 30:
            classification = "Very Good"
            guidance = "Well above average. On track for early retirement or significant wealth accumulation."
        elif rate < 50:
            classification = "Excellent"
            guidance = "Exceptional savings discipline. Financial independence may be achievable in 15-20 years."
        else:
            classification = "Extraordinary"
            guidance = "Extreme savings rate. Financial independence may be achievable in under 15 years. Ensure quality of life is not overly sacrificed."

        return {
            "status": "ok",
            "data": {
                "gross_income": gross_income,
                "total_savings": total_savings,
                "savings_rate_percent": rate,
                "classification": classification,
                "guidance": guidance,
                "benchmarks": {
                    "us_average": "~5-8% personal savings rate",
                    "recommended_minimum": "15-20% for standard retirement at 65",
                    "financial_independence": "50%+ for early retirement in 15-17 years",
                },
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
