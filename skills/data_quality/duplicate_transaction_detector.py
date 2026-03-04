"""Detect duplicate Ghost Ledger transactions."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "duplicate_transaction_detector",
    "description": "Finds exact and fuzzy duplicate transactions for Ghost Ledger hygiene.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "transactions": {
                "type": "array",
                "items": {"type": "object"},
            }
        },
        "required": ["transactions"],
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


def duplicate_transaction_detector(
    transactions: list[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    """Return duplicate groupings and dollar impact."""

    try:
        exact_dupes = _exact_duplicates(transactions)
        fuzzy_dupes = _fuzzy_duplicates(transactions)
        total_value = sum(item.get("amount", 0) for group in exact_dupes for item in group)
        total_value += sum(item.get("amount", 0) for group in fuzzy_dupes for item in group)
        data = {
            "exact_dupes": exact_dupes,
            "fuzzy_dupes": fuzzy_dupes,
            "total_duplicate_value": round(total_value, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("duplicate_transaction_detector", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _exact_duplicates(transactions: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for tx in transactions:
        tx_id = tx.get("tx_id")
        if not tx_id:
            continue
        groups.setdefault(tx_id, []).append(tx)
    return [group for group in groups.values() if len(group) > 1]


def _fuzzy_duplicates(transactions: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    matches: list[list[dict[str, Any]]] = []
    seen_indices: set[int] = set()
    for idx, tx in enumerate(transactions):
        if idx in seen_indices:
            continue
        bucket = [tx]
        for jdx in range(idx + 1, len(transactions)):
            other = transactions[jdx]
            if _is_fuzzy_match(tx, other):
                bucket.append(other)
                seen_indices.add(jdx)
        if len(bucket) > 1:
            matches.append(bucket)
    return matches


def _is_fuzzy_match(tx_a: dict[str, Any], tx_b: dict[str, Any]) -> bool:
    try:
        amount_a = float(tx_a.get("amount", 0))
        amount_b = float(tx_b.get("amount", 0))
    except (TypeError, ValueError):
        return False
    if abs(amount_a - amount_b) > 0.01:
        return False
    return (
        tx_a.get("date") == tx_b.get("date")
        and tx_a.get("counterparty") == tx_b.get("counterparty")
        and tx_a.get("source") == tx_b.get("source")
    )


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
