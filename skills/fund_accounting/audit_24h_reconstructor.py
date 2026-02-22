"""Rebuild a 24-hour ledger view for auditability."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "audit_24h_reconstructor",
    "description": "Filters ledger activity to a 24h window and produces a running balance.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "target_date": {
                "type": "string",
                "description": "Date to reconstruct (YYYY-MM-DD).",
            },
            "transactions": {
                "type": "array",
                "items": {"type": "object"},
                "description": "Transactions with timestamp and amount fields.",
            },
            "opening_balance": {
                "type": "number",
                "description": "Balance at the beginning of the window.",
                "default": 0.0,
            },
        },
        "required": ["target_date", "transactions"],
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


def audit_24h_reconstructor(
    target_date: str,
    transactions: list[dict[str, Any]],
    opening_balance: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Return a chronological reconstruction for the supplied day.

    Args:
        target_date: ISO8601 date describing the 24-hour window to rebuild.
        transactions: Source transactions containing timestamps and amounts.
        opening_balance: Balance at the start of the period for running totals.

    Returns:
        Envelope with ordered timeline entries and closing balance.
    """

    try:
        day_start = _parse_date(target_date)
        window_end = day_start + timedelta(days=1)

        filtered = []
        for tx in transactions:
            ts_str = tx.get("timestamp")
            if not ts_str:
                continue
            ts = _parse_timestamp(ts_str)
            if day_start <= ts < window_end:
                filtered.append((ts, tx))

        filtered.sort(key=lambda item: item[0])
        balance = opening_balance
        timeline: list[dict[str, Any]] = []

        for ts, tx in filtered:
            amount = float(tx.get("amount", 0) or 0)
            balance += amount
            timeline.append(
                {
                    "timestamp": ts.isoformat(),
                    "amount": round(amount, 4),
                    "running_balance": round(balance, 4),
                    "description": tx.get("description"),
                    "source": tx.get("source"),
                }
            )

        data = {
            "window": {
                "start": day_start.isoformat(),
                "end": window_end.isoformat(),
            },
            "opening_balance": round(opening_balance, 4),
            "closing_balance": round(balance, 4),
            "timeline": timeline,
        }

        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("audit_24h_reconstructor", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _parse_date(day: str) -> datetime:
    base = day.strip()
    if "T" in base:
        dt = _parse_timestamp(base)
        return dt.replace(hour=0, minute=0, second=0, microsecond=0)
    return datetime.fromisoformat(f"{base}T00:00:00+00:00")


def _parse_timestamp(value: str) -> datetime:
    normalized = value.replace("Z", "+00:00")
    dt = datetime.fromisoformat(normalized)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
