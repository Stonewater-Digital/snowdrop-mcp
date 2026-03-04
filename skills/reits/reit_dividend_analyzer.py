"""Analyze REIT dividend sustainability."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "reit_dividend_analyzer",
    "description": "Evaluates dividend yield, payout ratios, and tax characterization.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "affo_per_share": {"type": "number"},
            "dividend_per_share": {"type": "number"},
            "share_price": {"type": "number"},
            "taxable_income": {"type": "number"},
            "total_distributions": {"type": "number"},
            "return_of_capital_pct": {"type": "number"},
            "capital_gain_pct": {"type": "number"},
            "ordinary_income_pct": {"type": "number"},
        },
        "required": [
            "affo_per_share",
            "dividend_per_share",
            "share_price",
            "taxable_income",
            "total_distributions",
            "return_of_capital_pct",
            "capital_gain_pct",
            "ordinary_income_pct",
        ],
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def reit_dividend_analyzer(
    affo_per_share: float,
    dividend_per_share: float,
    share_price: float,
    taxable_income: float,
    total_distributions: float,
    return_of_capital_pct: float,
    capital_gain_pct: float,
    ordinary_income_pct: float,
    **_: Any,
) -> dict[str, Any]:
    """Return dividend metrics."""
    try:
        dividend_yield = dividend_per_share / share_price * 100 if share_price else 0.0
        affo_payout = dividend_per_share / affo_per_share * 100 if affo_per_share else 0.0
        coverage = affo_per_share / dividend_per_share if dividend_per_share else float("inf")
        sustainable = coverage >= 1.05
        tax_char = {
            "return_of_capital_pct": return_of_capital_pct,
            "capital_gain_pct": capital_gain_pct,
            "ordinary_income_pct": ordinary_income_pct,
        }
        tax_equivalent = dividend_yield * (1 - 0.37)
        cut_risk = "low" if sustainable else "elevated"
        data = {
            "dividend_yield": round(dividend_yield, 2),
            "affo_payout_ratio": round(affo_payout, 2),
            "coverage_ratio": round(coverage, 2),
            "sustainable": sustainable,
            "tax_characterization": tax_char,
            "tax_equivalent_yield_37pct": round(tax_equivalent, 2),
            "cut_risk": cut_risk,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("reit_dividend_analyzer", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
