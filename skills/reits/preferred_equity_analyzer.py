"""Assess preferred equity returns and coverage."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "preferred_equity_analyzer",
    "description": "Calculates preferred equity cash yield, coverage, and call protection metrics.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "preferred_equity_amount": {"type": "number"},
            "coupon_pct": {"type": "number"},
            "noi_after_debt_service": {"type": "number"},
            "call_protection_years": {"type": "number", "default": 2.0},
        },
        "required": ["preferred_equity_amount", "coupon_pct", "noi_after_debt_service"],
    },
    "outputSchema": {"type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def preferred_equity_analyzer(
    preferred_equity_amount: float,
    coupon_pct: float,
    noi_after_debt_service: float,
    call_protection_years: float = 2.0,
    **_: Any,
) -> dict[str, Any]:
    """Return preferred equity metrics."""
    try:
        cash_distribution = preferred_equity_amount * (coupon_pct / 100)
        coverage = noi_after_debt_service / cash_distribution if cash_distribution else 0.0
        implied_call_premium = coupon_pct * call_protection_years * 0.25
        data = {
            "annual_distribution": round(cash_distribution, 2),
            "coverage_ratio": round(coverage, 2),
            "implied_call_premium_pct": round(implied_call_premium, 2),
            "distribution_warning": coverage < 1.2,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("preferred_equity_analyzer", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
