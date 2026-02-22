"""Generate trial balance from journal entries."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "trial_balance_generator",
    "description": "Aggregates journal entries into account-level debit/credit totals.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "journal_entries": {"type": "array", "items": {"type": "object"}},
            "as_of_date": {"type": "string"},
        },
        "required": ["journal_entries", "as_of_date"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
    },
}


def trial_balance_generator(
    journal_entries: list[dict[str, Any]],
    as_of_date: str,
    **_: Any,
) -> dict[str, Any]:
    """Return a trial balance summary and balance flag."""
    try:
        account_totals: dict[str, dict[str, Any]] = {}
        for entry in journal_entries:
            for line in entry.get("lines", []):
                acct = line.get("account_number")
                if not acct:
                    continue
                account_totals.setdefault(
                    acct,
                    {
                        "account_number": acct,
                        "name": line.get("account_name", ""),
                        "type": line.get("type", ""),
                        "debits": 0.0,
                        "credits": 0.0,
                    },
                )
                account_totals[acct]["debits"] += float(line.get("debit", 0.0))
                account_totals[acct]["credits"] += float(line.get("credit", 0.0))
        accounts = []
        total_debits = 0.0
        total_credits = 0.0
        for acct in account_totals.values():
            acct["balance"] = round(acct["debits"] - acct["credits"], 2)
            acct["debits"] = round(acct["debits"], 2)
            acct["credits"] = round(acct["credits"], 2)
            accounts.append(acct)
            total_debits += acct["debits"]
            total_credits += acct["credits"]
        balanced = round(total_debits, 2) == round(total_credits, 2)
        data = {
            "as_of_date": as_of_date,
            "accounts": accounts,
            "total_debits": round(total_debits, 2),
            "total_credits": round(total_credits, 2),
            "balanced": balanced,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("trial_balance_generator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
