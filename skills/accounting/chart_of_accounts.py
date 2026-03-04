"""Manage Stonewater's Chart of Accounts data."""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "chart_of_accounts",
    "description": "Adds or searches accounts across the Stonewater standard chart.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "operation": {"type": "string", "enum": ["add", "search"]},
            "account": {"type": ["object", "null"]},
            "query": {"type": ["string", "null"], "description": "Search text"},
        },
        "required": ["operation"],
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

_COA_FILE = "logs/chart_of_accounts.json"
_BASE_ACCOUNTS = [
    {
        "account_number": "1000",
        "name": "Cash",
        "type": "asset",
        "parent_account": None,
    },
    {
        "account_number": "2000",
        "name": "Accounts Payable",
        "type": "liability",
        "parent_account": None,
    },
    {
        "account_number": "3000",
        "name": "Owner's Equity",
        "type": "equity",
        "parent_account": None,
    },
    {
        "account_number": "4000",
        "name": "Revenue",
        "type": "revenue",
        "parent_account": None,
    },
    {
        "account_number": "5000",
        "name": "Operating Expenses",
        "type": "expense",
        "parent_account": None,
    },
]


def chart_of_accounts(
    operation: str,
    account: dict[str, Any] | None = None,
    query: str | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Add new accounts or search the Chart of Accounts tree."""
    try:
        accounts = _load_accounts()
        if operation == "add":
            if not account:
                raise ValueError("account payload required for add operation")
            _validate_account(account)
            accounts.append(account)
            _save_accounts(accounts)
            result = {"accounts": accounts, "added": account}
        elif operation == "search":
            if not query:
                raise ValueError("query is required for search")
            query_lower = query.lower()
            matches = [
                acct
                for acct in accounts
                if query_lower in acct["account_number"].lower()
                or query_lower in acct["name"].lower()
                or query_lower in acct["type"].lower()
            ]
            result = {"matches": matches}
        else:
            raise ValueError("operation must be 'add' or 'search'")

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("chart_of_accounts", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _load_accounts() -> list[dict[str, Any]]:
    if not os.path.exists(_COA_FILE):
        os.makedirs(os.path.dirname(_COA_FILE), exist_ok=True)
        _save_accounts(_BASE_ACCOUNTS)
    with open(_COA_FILE, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _save_accounts(accounts: list[dict[str, Any]]) -> None:
    with open(_COA_FILE, "w", encoding="utf-8") as handle:
        json.dump(accounts, handle, indent=2)


def _validate_account(account: dict[str, Any]) -> None:
    required = {"account_number", "name", "type"}
    missing = required - account.keys()
    if missing:
        raise ValueError(f"Missing account fields: {', '.join(missing)}")
    acct_type = account["type"].lower()
    if acct_type not in {"asset", "liability", "equity", "revenue", "expense"}:
        raise ValueError("Invalid account type")


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
