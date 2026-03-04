"""Accrue equity dividends by position and payment timing."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

DATE_FORMATS = ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S%z")

TOOL_META: dict[str, Any] = {
    "name": "dividend_accrual_calculator",
    "description": "Accrues dividends between ex-date and pay-date across positions.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "positions": {"type": "array", "items": {"type": "object"}},
            "as_of_date": {"type": "string"},
        },
        "required": ["positions", "as_of_date"],
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


def _parse_date(value: str) -> datetime:
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(f"Invalid date format: {value}")


def dividend_accrual_calculator(positions: list[dict[str, Any]], as_of_date: str, **_: Any) -> dict[str, Any]:
    """Return total accrued and receivable dividends."""
    try:
        as_of = _parse_date(as_of_date)
        total_accrued = 0.0
        total_receivable = 0.0
        breakdown: list[dict[str, Any]] = []
        for position in positions or []:
            shares = float(position.get("shares", 0.0))
            dividend = float(position.get("dividend_per_share", 0.0))
            ex_date = _parse_date(position.get("ex_date")) if position.get("ex_date") else as_of
            pay_date = _parse_date(position.get("pay_date")) if position.get("pay_date") else as_of
            amount = shares * dividend
            status = "upcoming"
            accrued = 0.0
            receivable = 0.0
            if as_of >= ex_date and as_of < pay_date:
                accrued = amount
                receivable = amount
                status = "accrued"
            elif as_of >= pay_date:
                status = "paid"
            data_row = {
                "ticker": position.get("ticker"),
                "shares": shares,
                "status": status,
                "accrued": round(accrued, 4),
                "receivable": round(receivable, 4),
                "dividend_amount": round(amount, 4),
            }
            total_accrued += accrued
            total_receivable += receivable
            breakdown.append(data_row)
        data = {
            "total_accrued": round(total_accrued, 4),
            "total_receivable": round(total_receivable, 4),
            "position_breakdown": breakdown,
        }
        return {"status": "ok", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        try:
            with open("logs/lessons.md", "a") as _f:
                _f.write(f"- [{datetime.now(timezone.utc).isoformat()}] dividend_accrual_calculator: {exc}\n")
        except OSError:
            pass
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
