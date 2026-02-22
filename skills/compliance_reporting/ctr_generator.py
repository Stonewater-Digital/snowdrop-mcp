"""Currency Transaction Report helper."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "ctr_generator",
    "description": "Determines whether a CTR filing is required and drafts the payload.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "transaction": {"type": "object"},
            "filing_entity": {"type": "string"},
        },
        "required": ["transaction", "filing_entity"],
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


def ctr_generator(
    transaction: dict[str, Any],
    filing_entity: str,
    **_: Any,
) -> dict[str, Any]:
    """Check CTR thresholds and craft the draft payload."""
    try:
        if not isinstance(transaction, dict):
            raise ValueError("transaction must be a dict")
        amount = float(transaction.get("amount", 0.0))
        currency = str(transaction.get("currency", "USD"))
        tx_type = str(transaction.get("type", "deposit"))
        counterparty = transaction.get("counterparty")

        related = transaction.get("related_transactions", []) or []
        if not isinstance(related, list):
            raise ValueError("related_transactions must be a list")
        related_total = sum(float(item.get("amount", 0.0)) for item in related if isinstance(item, dict))

        ctr_required = currency.upper() == "USD" and amount >= 10_000 and tx_type in {"deposit", "withdrawal"}
        structuring_warning = (amount + related_total) >= 10_000 and len(related) > 0

        ctr_data = None
        if ctr_required:
            ctr_data = {
                "filing_entity": filing_entity,
                "transaction": transaction,
                "prepared_at": datetime.now(timezone.utc).isoformat(),
                "execution": "pending_thunder_approval",
            }

        result = {
            "ctr_required": ctr_required,
            "ctr_data": ctr_data,
            "structuring_warning": structuring_warning,
        }
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("ctr_generator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
