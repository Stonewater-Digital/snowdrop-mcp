"""
Executive Smary: Analyzes SaaS cohort retention curves and implied LTV by cohort.
Inputs: cohort_data (list)
Outputs: retention_rates_by_cohort (list), average_retention_curve (list), ltv_by_cohort (dict), churn_by_month (list)
MCP Tool Name: cohort_retention_analyzer
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "cohort_retention_analyzer",
    "description": (
        "Computes retention percentages for each cohort, aggregates the average curve, "
        "and estimates cohort-level LTV along with churn by month."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "cohort_data": {
                "type": "array",
                "description": "List of cohorts with cohort_month and monthly_active_users series.",
                "items": {"type": "object"},
            }
        },
        "required": ["cohort_data"],
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


def cohort_retention_analyzer(**kwargs: Any) -> dict:
    """Produce sticky-cohort analytics from monthly active user data."""
    try:
        cohort_data = kwargs["cohort_data"]
        if not isinstance(cohort_data, list) or not cohort_data:
            raise ValueError("cohort_data must be a non-empty list")

        retention_rates: List[Dict[str, Any]] = []
        ltv_by_cohort: Dict[str, float] = {}
        max_months = 0
        retention_matrix: List[List[float]] = []

        for cohort in cohort_data:
            label = str(cohort["cohort_month"])
            active_series = [float(val) for val in cohort["monthly_active_users"]]
            if not active_series or active_series[0] <= 0:
                raise ValueError("Each cohort must include positive starting users")
            start = active_series[0]
            rates = [users / start for users in active_series]
            retention_rates.append({"cohort": label, "retention": rates})
            ltv_by_cohort[label] = sum(rates)
            retention_matrix.append(rates)
            max_months = max(max_months, len(rates))

        avg_curve = []
        churn_by_month = []
        for month in range(max_months):
            month_rates = [rates[month] for rates in retention_matrix if month < len(rates)]
            if not month_rates:
                continue
            avg_rate = sum(month_rates) / len(month_rates)
            avg_curve.append(avg_rate)
            churn_by_month.append(1 - avg_rate)

        return {
            "status": "success",
            "data": {
                "retention_rates_by_cohort": retention_rates,
                "average_retention_curve": avg_curve,
                "ltv_by_cohort": ltv_by_cohort,
                "churn_by_month": churn_by_month,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"cohort_retention_analyzer failed: {e}")
        _log_lesson(f"cohort_retention_analyzer: {e}")
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
