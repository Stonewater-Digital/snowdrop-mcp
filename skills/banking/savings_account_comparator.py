"""Compare savings account earnings across multiple accounts over 1, 3, and 5 years.

MCP Tool Name: savings_account_comparator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "savings_account_comparator",
    "description": "Compare earnings across multiple savings accounts for a given principal over 1, 3, and 5 year horizons, ranked by returns.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "principal": {"type": "number", "description": "Initial deposit amount."},
            "accounts": {
                "type": "array",
                "description": "List of savings accounts to compare.",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Account name/label."},
                        "apy": {"type": "number", "description": "Annual Percentage Yield as decimal."},
                    },
                    "required": ["name", "apy"],
                },
            },
        },
        "required": ["principal", "accounts"],
    },
}


def savings_account_comparator(
    principal: float, accounts: list[dict[str, Any]]
) -> dict[str, Any]:
    """Compare savings accounts by earnings over multiple horizons."""
    try:
        if principal <= 0:
            return {
                "status": "error",
                "data": {"error": "principal must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if not accounts:
            return {
                "status": "error",
                "data": {"error": "accounts list must not be empty."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        results = []
        for acct in accounts:
            name = acct["name"]
            apy = acct["apy"]
            earnings = {}
            for years in [1, 3, 5]:
                balance = principal * (1 + apy) ** years
                earnings[f"year_{years}_balance"] = round(balance, 2)
                earnings[f"year_{years}_interest"] = round(balance - principal, 2)
            results.append({"name": name, "apy_pct": round(apy * 100, 4), **earnings})

        results.sort(key=lambda x: x["year_5_interest"], reverse=True)
        for rank, item in enumerate(results, 1):
            item["rank"] = rank

        return {
            "status": "ok",
            "data": {"principal": principal, "comparisons": results},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
