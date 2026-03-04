"""Assemble balance sheet reports from trial balances."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "balance_sheet_generator",
    "description": "Groups trial balance entries into a balance sheet (A=L+E validation).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "trial_balance": {"type": "array", "items": {"type": "object"}},
            "as_of_date": {"type": "string"},
            "entity_name": {"type": "string", "default": "Stonewater Solutions LLC"},
        },
        "required": ["trial_balance", "as_of_date"],
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


_TYPE_MAP = {
    "asset": "assets",
    "liability": "liabilities",
    "equity": "equity",
}


def balance_sheet_generator(
    trial_balance: list[dict[str, Any]],
    as_of_date: str,
    entity_name: str = "Stonewater Solutions LLC",
    **_: Any,
) -> dict[str, Any]:
    """Return a classified balance sheet with the accounting identity check."""
    try:
        grouped = {"assets": [], "liabilities": [], "equity": []}
        totals = {"assets": 0.0, "liabilities": 0.0, "equity": 0.0}
        for account in trial_balance:
            acct_type = account.get("type", "").lower()
            bucket = _TYPE_MAP.get(acct_type)
            if not bucket:
                continue
            balance = float(account.get("balance", 0.0))
            grouped[bucket].append(account)
            totals[bucket] += balance
        total_assets = round(totals["assets"], 2)
        total_liabilities = round(totals["liabilities"], 2)
        total_equity = round(totals["equity"], 2)
        in_balance = total_assets == round(total_liabilities + total_equity, 2)
        data = {
            "entity_name": entity_name,
            "as_of_date": as_of_date,
            "sections": grouped,
            "total_assets": total_assets,
            "total_liabilities": total_liabilities,
            "total_equity": total_equity,
            "in_balance": in_balance,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("balance_sheet_generator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
