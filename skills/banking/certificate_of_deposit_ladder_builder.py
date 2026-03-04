"""Build a CD ladder strategy splitting investment across multiple maturities.

MCP Tool Name: certificate_of_deposit_ladder_builder
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "certificate_of_deposit_ladder_builder",
    "description": "Build a CD ladder by dividing a total investment across 1-to-N year CDs. Estimates returns for each rung with a yield curve premium.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "total_investment": {"type": "number", "description": "Total amount to invest in the ladder."},
            "num_rungs": {"type": "integer", "description": "Number of CD rungs (default 5).", "default": 5},
            "base_apy": {"type": "number", "description": "APY for a 1-year CD as decimal (default 0.045).", "default": 0.045},
        },
        "required": ["total_investment"],
    },
}


def certificate_of_deposit_ladder_builder(
    total_investment: float, num_rungs: int = 5, base_apy: float = 0.045
) -> dict[str, Any]:
    """Build a CD ladder and estimate returns per rung."""
    try:
        if total_investment <= 0:
            return {
                "status": "error",
                "data": {"error": "total_investment must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if num_rungs <= 0:
            return {
                "status": "error",
                "data": {"error": "num_rungs must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        per_rung = total_investment / num_rungs
        rungs = []
        total_interest = 0.0

        for i in range(1, num_rungs + 1):
            # Yield curve: longer CDs earn a premium (~0.15% per additional year)
            apy = base_apy + (i - 1) * 0.0015
            years = i
            maturity_value = per_rung * (1 + apy) ** years
            interest = maturity_value - per_rung
            total_interest += interest
            rungs.append({
                "rung": i,
                "term_years": years,
                "amount": round(per_rung, 2),
                "apy_pct": round(apy * 100, 4),
                "maturity_value": round(maturity_value, 2),
                "interest_earned": round(interest, 2),
            })

        return {
            "status": "ok",
            "data": {
                "total_investment": total_investment,
                "num_rungs": num_rungs,
                "per_rung": round(per_rung, 2),
                "base_apy_pct": round(base_apy * 100, 4),
                "rungs": rungs,
                "total_interest": round(total_interest, 2),
                "total_maturity_value": round(total_investment + total_interest, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
