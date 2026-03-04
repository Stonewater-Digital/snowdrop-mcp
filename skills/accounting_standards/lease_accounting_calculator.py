"""Calculate ASC 842 lease accounting balances."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "lease_accounting_calculator",
    "description": "Computes lease liability, ROU asset, and income statement impact for ASC 842.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "lease_payments": {"type": "array", "items": {"type": "object"}},
            "lease_term_years": {"type": "integer"},
            "discount_rate": {"type": "number"},
            "lease_type": {"type": "string", "enum": ["operating", "finance"]},
            "residual_guarantee": {"type": "number", "default": 0},
        },
        "required": ["lease_payments", "lease_term_years", "discount_rate", "lease_type"],
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


def lease_accounting_calculator(
    lease_payments: list[dict[str, Any]],
    lease_term_years: int,
    discount_rate: float,
    lease_type: str,
    residual_guarantee: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Return ROU asset, liability, and year-by-year schedule."""
    try:
        payments = [p.get("payment", 0) for p in sorted(lease_payments, key=lambda p: p.get("year"))]
        pv = 0.0
        for idx, payment in enumerate(payments, start=1):
            pv += payment / ((1 + discount_rate / 100) ** idx)
        pv += residual_guarantee / ((1 + discount_rate / 100) ** lease_term_years)
        rou_asset = pv
        liability = pv
        schedule = []
        remaining = liability
        for idx, payment in enumerate(payments, start=1):
            interest = remaining * discount_rate / 100
            principal = payment - interest
            remaining = max(remaining - principal, 0)
            schedule.append(
                {
                    "year": idx,
                    "payment": round(payment, 2),
                    "interest": round(interest, 2),
                    "principal": round(principal, 2),
                    "ending_liability": round(remaining, 2),
                }
            )
        if lease_type == "operating":
            annual_expense = sum(payments) / lease_term_years
            income_impact = {"lease_expense": round(annual_expense, 2)}
        else:
            income_impact = {"interest_expense": round(schedule[0]["interest"], 2), "amortization": round(rou_asset / lease_term_years, 2)}
        data = {
            "rou_asset": round(rou_asset, 2),
            "lease_liability": round(liability, 2),
            "year_by_year": schedule,
            "total_lease_expense": round(sum(p.get("payment", 0) for p in lease_payments), 2),
            "balance_sheet_impact": {"asset": round(rou_asset, 2), "liability": round(liability, 2)},
            "income_statement_impact_year1": income_impact,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("lease_accounting_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
