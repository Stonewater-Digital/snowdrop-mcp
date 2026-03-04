"""Calculate freelance hourly rate needed to meet income goals.

MCP Tool Name: freelance_rate_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "freelance_rate_calculator",
    "description": "Calculate the hourly rate a freelancer needs to charge to meet their target annual income after taxes and expenses.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "target_annual_income": {
                "type": "number",
                "description": "Desired annual net income (take-home pay).",
            },
            "billable_hours_per_week": {
                "type": "number",
                "description": "Expected billable hours per week.",
                "default": 30,
            },
            "weeks_per_year": {
                "type": "number",
                "description": "Working weeks per year (accounting for vacation/sick time).",
                "default": 48,
            },
            "expenses_pct": {
                "type": "number",
                "description": "Business expenses as fraction of gross revenue (e.g., 0.30 for 30%).",
                "default": 0.30,
            },
            "tax_rate": {
                "type": "number",
                "description": "Estimated total tax rate as fraction (income + self-employment tax).",
                "default": 0.30,
            },
        },
        "required": ["target_annual_income"],
    },
}


def freelance_rate_calculator(
    target_annual_income: float,
    billable_hours_per_week: float = 30,
    weeks_per_year: float = 48,
    expenses_pct: float = 0.30,
    tax_rate: float = 0.30,
) -> dict[str, Any]:
    """Calculate freelance hourly rate needed to meet income goals."""
    try:
        if billable_hours_per_week <= 0 or weeks_per_year <= 0:
            return {
                "status": "error",
                "data": {"error": "Billable hours and weeks must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        retention = 1 - tax_rate - expenses_pct
        if retention <= 0:
            return {
                "status": "error",
                "data": {"error": "Tax rate + expenses percentage must be less than 100%."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # Work backwards: net = gross * (1 - tax - expenses)
        gross_needed = target_annual_income / retention
        total_billable_hours = billable_hours_per_week * weeks_per_year
        hourly_rate = gross_needed / total_billable_hours

        annual_taxes = gross_needed * tax_rate
        annual_expenses = gross_needed * expenses_pct

        # Comparison at different utilization rates
        utilization_scenarios = []
        for util_label, hours in [("20 hrs/wk", 20), ("25 hrs/wk", 25), ("30 hrs/wk", 30), ("35 hrs/wk", 35), ("40 hrs/wk", 40)]:
            total_h = hours * weeks_per_year
            rate = gross_needed / total_h
            utilization_scenarios.append({
                "billable_hours": util_label,
                "hourly_rate": round(rate, 2),
                "daily_rate_8hr": round(rate * 8, 2),
            })

        return {
            "status": "ok",
            "data": {
                "target_net_income": target_annual_income,
                "gross_revenue_needed": round(gross_needed, 2),
                "estimated_taxes": round(annual_taxes, 2),
                "estimated_expenses": round(annual_expenses, 2),
                "billable_hours_per_week": billable_hours_per_week,
                "weeks_per_year": weeks_per_year,
                "total_billable_hours": total_billable_hours,
                "minimum_hourly_rate": round(hourly_rate, 2),
                "daily_rate_8hr": round(hourly_rate * 8, 2),
                "monthly_revenue_target": round(gross_needed / 12, 2),
                "utilization_scenarios": utilization_scenarios,
                "note": "Remember to account for: health insurance, retirement contributions (SEP IRA/Solo 401k), "
                "non-billable time (admin, marketing, invoicing), and irregular income months. "
                "Self-employment tax is ~15.3% in addition to income tax.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
