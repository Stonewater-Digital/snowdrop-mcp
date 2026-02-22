"""Compute quarterly estimated tax payments under safe harbor rules."""
from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "estimated_tax_calculator",
    "description": "Applies 90%/100% safe harbor logic to estimate quarterly payments and due dates.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "ytd_income": {"type": "number"},
            "ytd_withholding": {"type": "number"},
            "prior_year_tax": {"type": "number"},
            "filing_status": {
                "type": "string",
                "enum": ["single", "married_joint", "llc_passthrough"],
            },
        },
        "required": ["ytd_income", "ytd_withholding", "prior_year_tax", "filing_status"],
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

_TAX_RATE = {
    "single": 0.32,
    "married_joint": 0.28,
    "llc_passthrough": 0.35,
}

_DUE_SEQUENCE = [
    (4, 15),  # April 15
    (6, 15),  # June 15
    (9, 15),  # September 15
    (1, 15),  # January 15 (following year)
]


def estimated_tax_calculator(
    ytd_income: float,
    ytd_withholding: float,
    prior_year_tax: float,
    filing_status: str,
    **_: Any,
) -> dict[str, Any]:
    """Return safe harbor annual estimate and upcoming quarterly payment."""
    try:
        if filing_status not in _TAX_RATE:
            raise ValueError("Unsupported filing_status")
        if ytd_income < 0 or ytd_withholding < 0 or prior_year_tax < 0:
            raise ValueError("Income and tax inputs must be non-negative")

        est_rate = _TAX_RATE[filing_status]
        current_year_tax = ytd_income * est_rate
        safe_harbor_target = max(prior_year_tax, 0.9 * current_year_tax)
        remaining_tax = max(0.0, safe_harbor_target - ytd_withholding)

        next_due, quarters_remaining = _next_due_date()
        quarterly_payment = remaining_tax / max(1, quarters_remaining)

        data = {
            "annual_estimate": round(safe_harbor_target, 2),
            "quarterly_payment_due": round(quarterly_payment, 2),
            "next_due_date": next_due.isoformat(),
            "quarters_remaining": quarters_remaining,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("estimated_tax_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _next_due_date() -> tuple[date, int]:
    today = date.today()
    upcoming = None
    quarters_remaining = 1
    for month, day in _DUE_SEQUENCE:
        year = today.year if month >= today.month else today.year + 1
        candidate = date(year, month, day)
        if candidate >= today:
            upcoming = candidate
            break
        quarters_remaining += 1
    if upcoming is None:
        upcoming = date(today.year + 1, 4, 15)
        quarters_remaining = 1
    remaining_dates = [
        date(upcoming.year if month >= upcoming.month else upcoming.year + 1, month, day)
        for month, day in _DUE_SEQUENCE
        if (month, day) >= (upcoming.month, upcoming.day)
    ]
    quarters_remaining = max(1, len(remaining_dates))
    return upcoming, quarters_remaining


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
