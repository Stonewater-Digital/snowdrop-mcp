"""Calculate credit account age statistics from account open dates.

MCP Tool Name: credit_age_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "credit_age_calculator",
    "description": "Calculate average, oldest, and newest credit account ages from a list of ISO-format account open dates.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "account_open_dates": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of account open dates in ISO format (YYYY-MM-DD).",
            },
        },
        "required": ["account_open_dates"],
    },
}


def credit_age_calculator(account_open_dates: list[str]) -> dict[str, Any]:
    """Calculate credit age statistics from account open dates."""
    try:
        if not account_open_dates:
            return {
                "status": "error",
                "data": {"error": "account_open_dates must not be empty."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        now = datetime.now(timezone.utc)
        ages_months = []

        for date_str in account_open_dates:
            dt = datetime.fromisoformat(date_str).replace(tzinfo=timezone.utc)
            delta = now - dt
            months = delta.days / 30.44  # average days per month
            ages_months.append(months)

        avg_months = sum(ages_months) / len(ages_months)
        oldest_months = max(ages_months)
        newest_months = min(ages_months)

        return {
            "status": "ok",
            "data": {
                "num_accounts": len(ages_months),
                "average_age_months": round(avg_months, 1),
                "average_age_years": round(avg_months / 12, 1),
                "oldest_age_months": round(oldest_months, 1),
                "oldest_age_years": round(oldest_months / 12, 1),
                "newest_age_months": round(newest_months, 1),
                "newest_age_years": round(newest_months / 12, 1),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
