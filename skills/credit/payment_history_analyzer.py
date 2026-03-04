"""Analyze payment history and assess its impact on credit.

MCP Tool Name: payment_history_analyzer
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "payment_history_analyzer",
    "description": "Analyze payment history by computing on-time percentage and assessing impact on credit score.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "total_payments": {"type": "integer", "description": "Total number of payments made."},
            "on_time_payments": {"type": "integer", "description": "Number of payments made on time."},
        },
        "required": ["total_payments", "on_time_payments"],
    },
}


def payment_history_analyzer(
    total_payments: int, on_time_payments: int
) -> dict[str, Any]:
    """Analyze payment history and assess credit impact."""
    try:
        if total_payments <= 0:
            return {
                "status": "error",
                "data": {"error": "total_payments must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if on_time_payments < 0 or on_time_payments > total_payments:
            return {
                "status": "error",
                "data": {"error": "on_time_payments must be between 0 and total_payments."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        pct = (on_time_payments / total_payments) * 100
        late = total_payments - on_time_payments

        if pct >= 99:
            impact = "Excellent — strong positive impact (~35% of FICO score)"
        elif pct >= 97:
            impact = "Good — minor late payments, small negative impact"
        elif pct >= 95:
            impact = "Fair — noticeable drag on score"
        elif pct >= 90:
            impact = "Poor — significant negative impact"
        else:
            impact = "Very poor — major credit score damage"

        return {
            "status": "ok",
            "data": {
                "total_payments": total_payments,
                "on_time_payments": on_time_payments,
                "late_payments": late,
                "on_time_pct": round(pct, 2),
                "impact_assessment": impact,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
