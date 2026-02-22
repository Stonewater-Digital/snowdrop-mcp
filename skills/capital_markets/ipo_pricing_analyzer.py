"""Analyze IPO pricing versus comps."""
from __future__ import annotations

from statistics import mean
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "ipo_pricing_analyzer",
    "description": "Evaluates implied valuation, dilution, and discount to comps for IPO ranges.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "filing_range_low": {"type": "number"},
            "filing_range_high": {"type": "number"},
            "shares_offered": {"type": "integer"},
            "pre_ipo_shares": {"type": "integer"},
            "greenshoe_pct": {"type": "number", "default": 15.0},
            "comps": {"type": "array", "items": {"type": "object"}},
            "company_revenue": {"type": "number"},
            "company_ebitda": {"type": "number"},
        },
        "required": [
            "filing_range_low",
            "filing_range_high",
            "shares_offered",
            "pre_ipo_shares",
            "comps",
            "company_revenue",
            "company_ebitda",
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


def ipo_pricing_analyzer(
    filing_range_low: float,
    filing_range_high: float,
    shares_offered: int,
    pre_ipo_shares: int,
    comps: list[dict[str, Any]],
    company_revenue: float,
    company_ebitda: float,
    greenshoe_pct: float = 15.0,
    **_: Any,
) -> dict[str, Any]:
    """Return IPO valuation metrics."""
    try:
        implied_low = filing_range_low * (pre_ipo_shares + shares_offered)
        implied_high = filing_range_high * (pre_ipo_shares + shares_offered)
        comp_ev_rev = mean(c.get("ev_revenue", 0.0) for c in comps) if comps else 0.0
        implied_ev = ((implied_low + implied_high) / 2)
        discount = (implied_ev / company_revenue) / comp_ev_rev - 1 if comp_ev_rev else 0.0
        dilution = shares_offered / (pre_ipo_shares + shares_offered) * 100
        gross_proceeds = filing_range_high * shares_offered
        greenshoe = gross_proceeds * (greenshoe_pct / 100)
        recommended_price = filing_range_low if discount > 0 else filing_range_high
        first_day_pop = -discount * 0.5 * 100
        data = {
            "implied_ev_range": {"low": round(implied_low, 2), "high": round(implied_high, 2)},
            "discount_to_comps_pct": round(discount * 100, 2),
            "dilution_pct": round(dilution, 2),
            "gross_proceeds": round(gross_proceeds, 2),
            "greenshoe_proceeds": round(greenshoe, 2),
            "recommended_price": round(recommended_price, 2),
            "first_day_pop_estimate_pct": round(first_day_pop, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("ipo_pricing_analyzer", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
