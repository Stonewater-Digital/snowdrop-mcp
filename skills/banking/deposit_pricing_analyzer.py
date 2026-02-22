"""Analyze deposit pricing sensitivity to rate changes."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "deposit_pricing_analyzer",
    "description": "Calculates weighted cost of deposits, effective beta, and expense impact from rate shifts.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "deposits": {"type": "array", "items": {"type": "object"}},
            "rate_change_bps": {"type": "integer"},
        },
        "required": ["deposits", "rate_change_bps"],
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


def deposit_pricing_analyzer(
    deposits: list[dict[str, Any]],
    rate_change_bps: int,
    **_: Any,
) -> dict[str, Any]:
    """Return cost metrics and sensitivity for deposit portfolios."""
    try:
        total_balance = sum(d.get("balance", 0) for d in deposits)
        if total_balance <= 0:
            raise ValueError("Total deposit balance must be positive")
        weighted_cost = sum(d["balance"] * d.get("rate_offered", 0) for d in deposits) / total_balance
        betas = [d.get("deposit_beta", 0) for d in deposits]
        effective_beta = sum(d["balance"] * d.get("deposit_beta", 0) for d in deposits) / total_balance
        rate_delta = rate_change_bps / 10000
        projected_cost = weighted_cost + effective_beta * rate_delta
        annual_impact = total_balance * (projected_cost - weighted_cost)
        sorted_deposits = sorted(deposits, key=lambda d: d.get("deposit_beta", 0))
        data = {
            "weighted_avg_cost": round(weighted_cost * 100, 3),
            "effective_beta": round(effective_beta, 2),
            "projected_cost_after_change": round(projected_cost * 100, 3),
            "annual_expense_impact": round(annual_impact, 2),
            "most_sensitive_product": sorted_deposits[-1].get("product") if sorted_deposits else None,
            "least_sensitive_product": sorted_deposits[0].get("product") if sorted_deposits else None,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("deposit_pricing_analyzer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
