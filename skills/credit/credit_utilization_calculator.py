"""Calculate credit utilization ratios per-card and overall.

MCP Tool Name: credit_utilization_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "credit_utilization_calculator",
    "description": "Calculate credit utilization ratio per card and overall. Provides total balance, total limit, and utilization percentages.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "balances": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of current balances for each card.",
            },
            "limits": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of credit limits for each card (same order as balances).",
            },
        },
        "required": ["balances", "limits"],
    },
}


def credit_utilization_calculator(
    balances: list[float], limits: list[float]
) -> dict[str, Any]:
    """Calculate per-card and overall credit utilization."""
    try:
        if len(balances) != len(limits):
            return {
                "status": "error",
                "data": {"error": "balances and limits must have the same length."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if not balances:
            return {
                "status": "error",
                "data": {"error": "balances list must not be empty."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        per_card = []
        for i, (bal, lim) in enumerate(zip(balances, limits)):
            ratio = (bal / lim * 100) if lim > 0 else 0.0
            per_card.append({
                "card": i + 1,
                "balance": bal,
                "limit": lim,
                "utilization_pct": round(ratio, 2),
            })

        total_bal = sum(balances)
        total_lim = sum(limits)
        overall = (total_bal / total_lim * 100) if total_lim > 0 else 0.0

        return {
            "status": "ok",
            "data": {
                "per_card": per_card,
                "total_balance": round(total_bal, 2),
                "total_limit": round(total_lim, 2),
                "overall_utilization_pct": round(overall, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
