"""Structure NMTC leveraged transactions."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "nmtc_deal_structurer",
    "description": "Models NMTC leveraged structures with investor equity, leverage loans, and subsidy.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "total_project_cost": {"type": "number"},
            "nmtc_allocation": {"type": "number"},
            "tax_credit_pct": {"type": "number", "default": 39.0},
            "leverage_loan_rate": {"type": "number"},
            "qlici_loan_rate": {"type": "number"},
            "cde_fee_pct": {"type": "number", "default": 3.0},
            "investor_required_return": {"type": "number"},
        },
        "required": ["total_project_cost", "nmtc_allocation", "leverage_loan_rate", "qlici_loan_rate", "investor_required_return"],
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def nmtc_deal_structurer(
    total_project_cost: float,
    nmtc_allocation: float,
    leverage_loan_rate: float,
    qlici_loan_rate: float,
    investor_required_return: float,
    tax_credit_pct: float = 39.0,
    cde_fee_pct: float = 3.0,
    **_: Any,
) -> dict[str, Any]:
    """Return NMTC structure details."""
    try:
        tax_credits_total = nmtc_allocation * (tax_credit_pct / 100)
        investor_equity = tax_credits_total / investor_required_return
        leverage_loan = total_project_cost - investor_equity
        cde_fee = nmtc_allocation * (cde_fee_pct / 100)
        net_subsidy = tax_credits_total - cde_fee
        effective_subsidy_pct = net_subsidy / total_project_cost * 100 if total_project_cost else 0.0
        structure = {
            "fund_sources": {
                "investor_equity": round(investor_equity, 2),
                "leverage_loan": round(leverage_loan, 2),
            },
            "qlici_loans": {
                "A_note": round(leverage_loan, 2),
                "B_note": round(investor_equity, 2),
                "rates": {"A": qlici_loan_rate, "B": qlici_loan_rate - 0.02},
            },
        }
        data = {
            "structure": structure,
            "investor_equity": round(investor_equity, 2),
            "leverage_loan": round(leverage_loan, 2),
            "tax_credits_total": round(tax_credits_total, 2),
            "net_project_subsidy": round(net_subsidy, 2),
            "effective_subsidy_pct": round(effective_subsidy_pct, 2),
            "investor_irr": investor_required_return,
            "year_7_unwind": {"put_price": 1000, "loan_forgiveness": round(investor_equity, 2)},
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("nmtc_deal_structurer", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
