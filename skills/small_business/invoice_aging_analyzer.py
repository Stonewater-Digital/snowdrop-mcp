"""
Executive Smary: Produces an AR aging report with collection metrics and bad debt estimate.
Inputs: invoices (list)
Outputs: aging_buckets (dict), total_outstanding (float), weighted_average_days (float), collection_rate (float), bad_debt_estimate (float)
MCP Tool Name: invoice_aging_analyzer
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger("snowdrop.skills")

BUCKETS = [(0, 30), (31, 60), (61, 90), (91, 120), (121, float("inf"))]

TOOL_META = {
    "name": "invoice_aging_analyzer",
    "description": (
        "Groups invoices into standard aging buckets, calculates outstanding exposure, "
        "and estimates collection performance and bad debt reserves."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "invoices": {
                "type": "array",
                "description": "List of invoices with id, amount, issue_date, due_date, paid_date (optional).",
                "items": {"type": "object"},
            }
        },
        "required": ["invoices"],
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


def invoice_aging_analyzer(**kwargs: Any) -> dict:
    """Create AR aging buckets and calculate outstanding exposure."""
    try:
        invoices = kwargs["invoices"]
        if not isinstance(invoices, list):
            raise ValueError("invoices must be a list")

        buckets = {f"{low}-{high if high != float('inf') else '+'}": 0.0 for low, high in BUCKETS}
        total_outstanding = 0.0
        weighted_days = 0.0
        total_amount = 0.0
        collected = 0.0
        today = datetime.now(timezone.utc).date()

        for inv in invoices:
            amount = float(inv["amount"])
            total_amount += amount
            paid_date = inv.get("paid_date")
            if paid_date:
                collected += amount
                continue
            due_date = datetime.fromisoformat(inv["due_date"]).date()
            days_past_due = (today - due_date).days
            outstanding = amount
            total_outstanding += outstanding
            weighted_days += outstanding * max(days_past_due, 0)
            bucket_key = _bucket_label(days_past_due)
            buckets[bucket_key] += outstanding

        weighted_average_days = weighted_days / total_outstanding if total_outstanding else 0.0
        collection_rate = collected / total_amount if total_amount else 0.0
        bad_debt_estimate = buckets["121-inf"] * 0.5

        return {
            "status": "success",
            "data": {
                "aging_buckets": buckets,
                "total_outstanding": total_outstanding,
                "weighted_average_days": weighted_average_days,
                "collection_rate": collection_rate,
                "bad_debt_estimate": bad_debt_estimate,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError, KeyError) as e:
        logger.error(f"invoice_aging_analyzer failed: {e}")
        _log_lesson(f"invoice_aging_analyzer: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _bucket_label(days_past_due: int) -> str:
    for low, high in BUCKETS:
        if days_past_due <= high:
            return f"{low}-{int(high) if high != float('inf') else 'inf'}"
    return "121-inf"


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
