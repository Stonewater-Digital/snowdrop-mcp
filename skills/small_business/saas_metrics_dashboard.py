"""
Executive Smary: Calculates core SaaS KPIs like NRR, churn, ARPU, and quick ratio.
Inputs: mrr (float), new_mrr (float), churned_mrr (float), expansion_mrr (float), customers (int), new_customers (int), churned_customers (int)
Outputs: net_new_mrr (float), revenue_churn_rate (float), logo_churn_rate (float), arpu (float), net_revenue_retention (float), quick_ratio (float)
MCP Tool Name: saas_metrics_dashboard
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "saas_metrics_dashboard",
    "description": (
        "Generates a snapshot of SaaS health including net new MRR, churn metrics, ARPU, "
        "net revenue retention, and the quick ratio."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "mrr": {
                "type": "number",
                "description": "Monthly recurring revenue at period start.",
            },
            "new_mrr": {
                "type": "number",
                "description": "MRR from new customers in the period.",
            },
            "churned_mrr": {
                "type": "number",
                "description": "MRR lost from churn in the period.",
            },
            "expansion_mrr": {
                "type": "number",
                "description": "MRR gained from existing customers (upsell/cross-sell).",
            },
            "customers": {
                "type": "number",
                "description": "Active customer count at period start.",
            },
            "new_customers": {
                "type": "number",
                "description": "Customers added during the period.",
            },
            "churned_customers": {
                "type": "number",
                "description": "Customers lost during the period.",
            },
        },
        "required": [
            "mrr",
            "new_mrr",
            "churned_mrr",
            "expansion_mrr",
            "customers",
            "new_customers",
            "churned_customers",
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


def saas_metrics_dashboard(**kwargs: Any) -> dict:
    """Compute SaaS KPIs including net new MRR, churn, retention, and quick ratio."""
    try:
        mrr = float(kwargs["mrr"])
        new_mrr = float(kwargs["new_mrr"])
        churned_mrr = float(kwargs["churned_mrr"])
        expansion_mrr = float(kwargs["expansion_mrr"])
        customers = int(kwargs["customers"])
        new_customers = int(kwargs["new_customers"])
        churned_customers = int(kwargs["churned_customers"])

        if customers <= 0:
            raise ValueError("customers must be positive")

        net_new_mrr = new_mrr + expansion_mrr - churned_mrr
        revenue_churn_rate = churned_mrr / mrr if mrr > 0 else 0.0
        logo_churn_rate = churned_customers / customers
        arpu = mrr / customers
        net_revenue_retention = (mrr + expansion_mrr - churned_mrr) / mrr if mrr > 0 else 0.0
        quick_ratio = (
            (new_mrr + expansion_mrr) / churned_mrr if churned_mrr > 0 else float("inf")
        )

        return {
            "status": "success",
            "data": {
                "net_new_mrr": net_new_mrr,
                "revenue_churn_rate": revenue_churn_rate,
                "logo_churn_rate": logo_churn_rate,
                "arpu": arpu,
                "net_revenue_retention": net_revenue_retention,
                "quick_ratio": quick_ratio,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"saas_metrics_dashboard failed: {e}")
        _log_lesson(f"saas_metrics_dashboard: {e}")
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
