"""Model ABS/MBS cash flows with prepayments and defaults."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "securitization_cashflow_modeler",
    "description": "Generates month-by-month cash flow projections including CPR/CDR and servicing fees.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "pool_balance": {"type": "number"},
            "wac": {"type": "number"},
            "wam": {"type": "integer"},
            "cpr": {"type": "number"},
            "cdr": {"type": "number"},
            "recovery_rate": {"type": "number"},
            "servicing_fee_pct": {"type": "number"},
        },
        "required": ["pool_balance", "wac", "wam", "cpr", "cdr", "recovery_rate", "servicing_fee_pct"],
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


def securitization_cashflow_modeler(
    pool_balance: float,
    wac: float,
    wam: int,
    cpr: float,
    cdr: float,
    recovery_rate: float,
    servicing_fee_pct: float,
    **_: Any,
) -> dict[str, Any]:
    """Return projected principal, interest, losses, and yield."""
    try:
        balance = pool_balance
        monthly_rate = wac / 12 / 100
        smm = 1 - (1 - cpr / 100) ** (1 / 12)
        default_rate = 1 - (1 - cdr / 100) ** (1 / 12)
        servicing_rate = servicing_fee_pct / 12 / 100
        cashflows = []
        total_interest = total_principal = total_losses = 0.0
        for month in range(1, wam + 1):
            if balance <= 0:
                break
            interest = balance * monthly_rate
            scheduled_principal = pool_balance / wam
            prepayment = (balance - scheduled_principal) * smm
            defaults = (balance - scheduled_principal - prepayment) * default_rate
            recoveries = defaults * recovery_rate / 100
            loss = defaults - recoveries
            servicing = balance * servicing_rate
            principal_collected = scheduled_principal + prepayment + recoveries
            balance -= principal_collected
            total_interest += interest - servicing
            total_principal += principal_collected
            total_losses += loss
            cashflows.append(
                {
                    "month": month,
                    "interest": round(interest - servicing, 2),
                    "principal": round(principal_collected, 2),
                    "loss": round(loss, 2),
                    "ending_balance": round(max(balance, 0), 2),
                }
            )
        wal = sum(cf["month"] * cf["principal"] for cf in cashflows) / max(total_principal, 1e-6)
        total_cash = total_interest + total_principal
        yield_investor = total_cash / max(pool_balance, 1e-6) / (len(cashflows) / 12)
        data = {
            "monthly_cashflows": cashflows,
            "total_principal_collected": round(total_principal, 2),
            "total_interest": round(total_interest, 2),
            "total_losses": round(total_losses, 2),
            "wal_months": round(wal, 2),
            "yield_to_investor": round(yield_investor * 100, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("securitization_cashflow_modeler", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
