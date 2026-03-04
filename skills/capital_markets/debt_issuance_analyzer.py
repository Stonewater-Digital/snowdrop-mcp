"""Evaluate bond issuance all-in cost."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "debt_issuance_analyzer",
    "description": "Computes net proceeds, OID yields, and all-in borrowing costs for bond deals.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "face_value": {"type": "number"},
            "coupon_rate": {"type": "number"},
            "maturity_years": {"type": "integer"},
            "issue_price_pct": {"type": "number"},
            "underwriter_spread_pct": {"type": "number"},
            "rating_agency_fees": {"type": "number"},
            "legal_fees": {"type": "number"},
            "sec_fees": {"type": "number"},
        },
        "required": ["face_value", "coupon_rate", "maturity_years", "issue_price_pct", "underwriter_spread_pct", "rating_agency_fees", "legal_fees", "sec_fees"],
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


def debt_issuance_analyzer(
    face_value: float,
    coupon_rate: float,
    maturity_years: int,
    issue_price_pct: float,
    underwriter_spread_pct: float,
    rating_agency_fees: float,
    legal_fees: float,
    sec_fees: float,
    **_: Any,
) -> dict[str, Any]:
    """Return issuance cost metrics."""
    try:
        gross_proceeds = face_value * (issue_price_pct / 100)
        issuance_costs = face_value * (underwriter_spread_pct / 100) + rating_agency_fees + legal_fees + sec_fees
        net_proceeds = gross_proceeds - issuance_costs
        annual_coupon = face_value * coupon_rate
        oid_yield = (coupon_rate + (100 - issue_price_pct) / (maturity_years))
        all_in_cost = (annual_coupon + issuance_costs / maturity_years) / net_proceeds if net_proceeds else 0.0
        data = {
            "gross_proceeds": round(gross_proceeds, 2),
            "net_proceeds": round(net_proceeds, 2),
            "all_in_cost_pct": round(all_in_cost * 100, 2),
            "oid_amortization_annual": round((100 - issue_price_pct) / maturity_years, 4),
            "annual_coupon_payment": round(annual_coupon, 2),
            "total_issuance_costs": round(issuance_costs, 2),
            "breakeven_vs_bank_loan": "attractive" if all_in_cost < coupon_rate else "bank cheaper",
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("debt_issuance_analyzer", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
