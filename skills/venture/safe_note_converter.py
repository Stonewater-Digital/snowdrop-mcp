"""Model SAFE conversions into priced rounds."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "safe_note_converter",
    "description": "Calculates SAFE conversion price, shares, and founder dilution.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "safe_amt": {"type": "number"},
            "valuation_cap": {"type": "number"},
            "discount_pct": {"type": "number", "default": 20.0},
            "mfn": {"type": "boolean", "default": False},
            "next_round_pre_money": {"type": "number"},
            "next_round_pps": {"type": "number"},
            "pre_money_safe": {"type": "boolean", "default": False},
        },
        "required": [
            "safe_amt",
            "valuation_cap",
            "next_round_pre_money",
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


def safe_note_converter(
    safe_amt: float,
    valuation_cap: float,
    discount_pct: float | None = 20.0,
    mfn: bool = False,
    next_round_pre_money: float = 0,
    next_round_pps: float = 0,
    pre_money_safe: bool = False,
    **_: Any,
) -> dict[str, Any]:
    """Return SAFE conversion economics."""
    try:
        if safe_amt <= 0 or valuation_cap <= 0 or next_round_pps <= 0:
            raise ValueError("SAFE amount, valuation cap, and PPS must be positive")
        discount_pct = discount_pct or 0
        cap_price = valuation_cap / max(next_round_pre_money / next_round_pps, 1e-6)
        discount_price = next_round_pps * (1 - discount_pct / 100)
        conversion_price = min(cap_price, discount_price)
        method_used = "cap" if conversion_price == cap_price else "discount"
        shares = int(safe_amt / max(conversion_price, 1e-6))
        effective_valuation = shares * next_round_pps
        dilution = safe_amt / (next_round_pre_money + safe_amt) * 100 if pre_money_safe else safe_amt / (next_round_pre_money + safe_amt) * 100
        ownership_pct = shares * next_round_pps / max(next_round_pre_money + safe_amt, 1e-6) * 100
        if mfn:
            method_used += "_mfn"
        data = {
            "conversion_price": round(conversion_price, 4),
            "shares_issued": shares,
            "effective_valuation": round(effective_valuation, 2),
            "method_used": method_used,
            "dilution_to_founders_pct": round(dilution, 4),
            "ownership_pct": round(ownership_pct, 4),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("safe_note_converter", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
