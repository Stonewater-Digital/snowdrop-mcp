"""Calculate revenue per employee and provide benchmark comparison.

MCP Tool Name: revenue_per_employee_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "revenue_per_employee_calculator",
    "description": "Calculate revenue per employee and compare against industry benchmarks.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "annual_revenue": {"type": "number", "description": "Total annual revenue."},
            "num_employees": {"type": "integer", "description": "Number of full-time employees."},
        },
        "required": ["annual_revenue", "num_employees"],
    },
}

_BENCHMARKS = {
    "tech_saas": 250000,
    "professional_services": 150000,
    "retail": 175000,
    "manufacturing": 200000,
}


def revenue_per_employee_calculator(
    annual_revenue: float, num_employees: int
) -> dict[str, Any]:
    """Calculate revenue per employee with benchmarks."""
    try:
        if num_employees <= 0:
            return {
                "status": "error",
                "data": {"error": "num_employees must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        rpe = annual_revenue / num_employees

        benchmarks = {
            k: {
                "benchmark": v,
                "your_pct_of_benchmark": round((rpe / v) * 100, 1),
            }
            for k, v in _BENCHMARKS.items()
        }

        return {
            "status": "ok",
            "data": {
                "annual_revenue": annual_revenue,
                "num_employees": num_employees,
                "revenue_per_employee": round(rpe, 2),
                "industry_benchmarks": benchmarks,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
