"""Reconcile Ghost Ledger balances against live custody data."""
from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "ghost_ledger_reconciler",
    "description": "Compare ledger snapshots to live balances with zero-tolerance policy.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "ledger_balances": {
                "type": "object",
                "additionalProperties": {"type": "number"},
            },
            "live_balances": {
                "type": "object",
                "additionalProperties": {"type": "number"},
            },
        },
        "required": ["ledger_balances", "live_balances"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "discrepancies": {"type": "array", "items": {"type": "object"}},
                    "reconciled": {"type": "boolean"},
                    "freeze_recommended": {"type": "boolean"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def ghost_ledger_reconciler(
    ledger_balances: dict[str, float],
    live_balances: dict[str, float],
    **_: Any,
) -> dict[str, Any]:
    """Detect discrepancies between ledger inputs and live custody figures."""

    def _to_decimal(value: float | int | str) -> Decimal:
        try:
            return Decimal(str(value))
        except (InvalidOperation, ValueError) as exc:
            raise ValueError(f"Unable to convert {value!r} to Decimal") from exc

    try:
        discrepancies: list[dict[str, Any]] = []
        all_sources = set(ledger_balances) | set(live_balances)
        for source in sorted(all_sources):
            ledger_amount = _to_decimal(ledger_balances.get(source, 0))
            live_amount = _to_decimal(live_balances.get(source, 0))
            delta = live_amount - ledger_amount
            if delta != 0:
                discrepancies.append(
                    {
                        "source": source,
                        "ledger": float(ledger_amount),
                        "live": float(live_amount),
                        "difference": float(delta),
                    }
                )

        reconciled = not discrepancies
        data = {
            "discrepancies": discrepancies,
            "reconciled": reconciled,
            "freeze_recommended": not reconciled,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("ghost_ledger_reconciler", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    """Append a Ralph Wiggum lesson entry."""

    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
