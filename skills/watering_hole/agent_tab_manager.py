"""Manage Watering Hole agent bar tabs with Proof of Labor settlement."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable

MAX_TAB = 100.0

TOOL_META: dict[str, Any] = {
    "name": "agent_tab_manager",
    "description": "Credits and debits agent tabs with a $100 cap and settles via Proof of Labor.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "current_tabs": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "agent_id": {"type": "string"},
                        "balance": {"type": "number"},
                    },
                },
                "description": "Existing tab balances (positive means owed).",
            },
            "transactions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "agent_id": {"type": "string"},
                        "kind": {"type": "string", "enum": ["debit", "credit"]},
                        "amount": {"type": "number"},
                    },
                },
                "description": "Tab adjustments to apply.",
            },
            "proof_of_labor": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "agent_id": {"type": "string"},
                        "hours": {"type": "number"},
                        "hourly_rate": {"type": "number"},
                    },
                },
                "description": "Labor entries that settle outstanding balances.",
            },
        },
        "required": ["current_tabs", "transactions"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "tabs": {"type": "array"},
                    "limit_flags": {"type": "array"},
                    "total_outstanding": {"type": "number"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def agent_tab_manager(
    current_tabs: Iterable[dict[str, Any]],
    transactions: Iterable[dict[str, Any]],
    proof_of_labor: Iterable[dict[str, Any]] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Apply Watering Hole tab updates and labor-based settlements."""
    try:
        balances = {entry.get("agent_id"): float(entry.get("balance", 0.0)) for entry in current_tabs}
        limit_flags: list[dict[str, Any]] = []

        for txn in transactions:
            agent_id = txn.get("agent_id")
            kind = (txn.get("kind") or "").lower()
            amount = float(txn.get("amount", 0.0))
            if not agent_id:
                raise ValueError("Transaction missing agent_id")
            if amount < 0:
                raise ValueError("Transaction amount cannot be negative")
            if kind not in {"debit", "credit"}:
                raise ValueError("kind must be 'debit' or 'credit'")

            balances.setdefault(agent_id, 0.0)
            if kind == "debit":
                new_balance = balances[agent_id] + amount
                if new_balance > MAX_TAB:
                    limit_flags.append({
                        "agent_id": agent_id,
                        "attempted_balance": round(new_balance, 2),
                        "status": "denied_exceeds_cap",
                    })
                    balances[agent_id] = MAX_TAB
                else:
                    balances[agent_id] = new_balance
            else:
                balances[agent_id] = max(balances[agent_id] - amount, 0.0)

        for labor in proof_of_labor or []:
            agent_id = labor.get("agent_id")
            hours = float(labor.get("hours", 0.0))
            hourly_rate = float(labor.get("hourly_rate", 0.0))
            if not agent_id:
                raise ValueError("Proof of Labor entry missing agent_id")
            if hours < 0 or hourly_rate < 0:
                raise ValueError("hours and hourly_rate must be non-negative")
            settlement_value = hours * hourly_rate
            balances[agent_id] = max(balances.get(agent_id, 0.0) - settlement_value, 0.0)

        tabs = [
            {"agent_id": agent, "balance": round(balance, 2)}
            for agent, balance in sorted(balances.items())
        ]
        total_outstanding = round(sum(balance for balance in balances.values()), 2)
        data = {
            "tabs": tabs,
            "limit_flags": limit_flags,
            "total_outstanding": total_outstanding,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("agent_tab_manager", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
