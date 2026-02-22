"""Compare on-chain balances against Ghost Ledger with zero tolerance."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable

TOOL_META: dict[str, Any] = {
    "name": "wallets_check",
    "description": "Checks on-chain balances versus Ghost Ledger and enforces $0.00 tolerance.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "on_chain_balances": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "source": {"type": "string"},
                        "amount_usd": {"type": "number"},
                    },
                },
            },
            "ghost_ledger_balances": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "source": {"type": "string"},
                        "amount_usd": {"type": "number"},
                    },
                },
            },
            "tolerance_usd": {"type": "number", "default": 0.0},
        },
        "required": ["on_chain_balances", "ghost_ledger_balances"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "in_balance": {"type": "boolean"},
                    "differences": {"type": "array"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def wallets_check(
    on_chain_balances: Iterable[dict[str, Any]],
    ghost_ledger_balances: Iterable[dict[str, Any]],
    tolerance_usd: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Compare balances and enforce tolerance."""
    try:
        ledger_map = {
            entry.get("source"): float(entry.get("amount_usd", 0.0))
            for entry in ghost_ledger_balances
        }
        differences = []
        in_balance = True
        for chain_entry in on_chain_balances:
            source = chain_entry.get("source")
            if not source:
                raise ValueError("Each on_chain entry must specify source")
            chain_amount = float(chain_entry.get("amount_usd", 0.0))
            ledger_amount = ledger_map.get(source)
            if ledger_amount is None:
                raise ValueError(f"Ghost Ledger missing source '{source}'")
            delta = round(chain_amount - ledger_amount, 2)
            if abs(delta) > tolerance_usd:
                in_balance = False
            differences.append({
                "source": source,
                "on_chain": round(chain_amount, 2),
                "ghost_ledger": round(ledger_amount, 2),
                "delta": delta,
            })

        data = {"in_balance": in_balance, "differences": differences}
        status = "success"
        if not in_balance:
            status = "error"
        return {
            "status": status,
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("wallets_check", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
