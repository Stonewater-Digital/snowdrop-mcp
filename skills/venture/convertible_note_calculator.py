"""Calculate convertible note conversion economics."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "convertible_note_calculator",
    "description": "Computes accrued interest, conversion price, and shares for convertible notes.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "principal": {"type": "number"},
            "interest_rate": {"type": "number"},
            "term_months": {"type": "integer"},
            "valuation_cap": {"type": ["number", "null"], "default": None},
            "discount_pct": {"type": "number", "default": 20.0},
            "issue_date": {"type": "string"},
            "conversion_date": {"type": "string"},
            "qualified_financing_amount": {"type": "number"},
            "next_round_pps": {"type": "number"},
        },
        "required": [
            "principal",
            "interest_rate",
            "term_months",
            "issue_date",
            "conversion_date",
            "qualified_financing_amount",
            "next_round_pps",
        ],
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


def convertible_note_calculator(
    principal: float,
    interest_rate: float,
    term_months: int,
    valuation_cap: float | None,
    discount_pct: float = 20.0,
    issue_date: str = "",
    conversion_date: str = "",
    qualified_financing_amount: float = 0.0,
    next_round_pps: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Return note conversion details based on cap or discount."""
    try:
        if principal <= 0 or next_round_pps <= 0:
            raise ValueError("Principal and PPS must be positive")
        months = max(term_months, 1)
        accrued_interest = principal * (interest_rate / 100) * (months / 12)
        total_converting = principal + accrued_interest
        discount_price = next_round_pps * (1 - discount_pct / 100)
        cap_price = None
        if valuation_cap:
            implied_shares = qualified_financing_amount / next_round_pps if next_round_pps else 1
            cap_price = valuation_cap / max(implied_shares, 1)
        if cap_price is not None and cap_price < discount_price:
            conversion_price = cap_price
            method = "cap"
        else:
            conversion_price = discount_price
            method = "discount"
        shares = int(total_converting / max(conversion_price, 1e-6))
        effective_discount = 1 - (conversion_price / next_round_pps)
        data = {
            "accrued_interest": round(accrued_interest, 2),
            "total_converting": round(total_converting, 2),
            "conversion_price": round(conversion_price, 4),
            "shares_issued": shares,
            "effective_discount_pct": round(effective_discount * 100, 2),
            "cap_or_discount_used": method,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("convertible_note_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
