"""
Executive Smary: Computes customer acquisition cost versus lifetime value with payback.
Inputs: marketing_spend (float), new_customers (int), avg_revenue_per_customer (float), avg_customer_lifespan_months (float), gross_margin_pct (float), churn_rate (float)
Outputs: cac (float), ltv (float), ltv_to_cac_ratio (float), payback_months (float), healthy_ratio_assessment (str)
MCP Tool Name: cac_ltv_calculator
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "cac_ltv_calculator",
    "description": (
        "Calculates CAC, gross-margin LTV, payback period, and ratio health to evaluate "
        "growth efficiency for subscription and transactional businesses."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "marketing_spend": {
                "type": "number",
                "description": "Total acquisition spend over the period.",
            },
            "new_customers": {
                "type": "number",
                "description": "Number of customers acquired from that spend.",
            },
            "avg_revenue_per_customer": {
                "type": "number",
                "description": "Average monthly revenue per customer.",
            },
            "avg_customer_lifespan_months": {
                "type": "number",
                "description": "Average active months before churn.",
            },
            "gross_margin_pct": {
                "type": "number",
                "description": "Gross margin percentage as decimal.",
            },
            "churn_rate": {
                "type": "number",
                "description": "Monthly churn rate as decimal.",
            },
        },
        "required": [
            "marketing_spend",
            "new_customers",
            "avg_revenue_per_customer",
            "avg_customer_lifespan_months",
            "gross_margin_pct",
            "churn_rate",
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


def cac_ltv_calculator(**kwargs: Any) -> dict:
    """Evaluate customer acquisition efficiency using LTV/CAC metrics."""
    try:
        marketing_spend = float(kwargs["marketing_spend"])
        new_customers = int(kwargs["new_customers"])
        arpc = float(kwargs["avg_revenue_per_customer"])
        lifespan = float(kwargs["avg_customer_lifespan_months"])
        gross_margin = float(kwargs["gross_margin_pct"])
        churn_rate = float(kwargs["churn_rate"])

        if new_customers <= 0 or arpc <= 0:
            raise ValueError("new_customers and avg_revenue_per_customer must be positive")

        cac = marketing_spend / new_customers
        ltv = arpc * gross_margin * lifespan
        ratio = ltv / cac if cac > 0 else float("inf")
        monthly_margin = arpc * gross_margin * (1 - churn_rate)
        payback = cac / monthly_margin if monthly_margin > 0 else float("inf")
        assessment = "excellent" if ratio >= 3 else "needs_improvement" if ratio < 2 else "acceptable"

        return {
            "status": "success",
            "data": {
                "cac": cac,
                "ltv": ltv,
                "ltv_to_cac_ratio": ratio,
                "payback_months": payback,
                "healthy_ratio_assessment": assessment,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"cac_ltv_calculator failed: {e}")
        _log_lesson(f"cac_ltv_calculator: {e}")
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
