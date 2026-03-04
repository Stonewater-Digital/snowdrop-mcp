"""Estimate recoveries by seniority and collateral."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "recovery_rate_estimator",
    "description": "Aggregates LGD and recovery percentages by class.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "positions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "seniority": {"type": "string"},
                        "collateral_type": {"type": "string"},
                        "balance": {"type": "number"},
                        "recovery_pct": {"type": "number"},
                    },
                    "required": ["seniority", "collateral_type", "balance", "recovery_pct"],
                },
            },
        },
        "required": ["positions"],
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


def recovery_rate_estimator(positions: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return weighted recovery rates by dimension."""
    try:
        total_balance = sum(p.get("balance", 0.0) for p in positions)
        weighted_sum = sum(p.get("balance", 0.0) * p.get("recovery_pct", 0.0) for p in positions)
        overall_recovery = weighted_sum / total_balance if total_balance else 0.0
        seniority_breakdown: dict[str, float] = defaultdict(float)
        collateral_breakdown: dict[str, float] = defaultdict(float)
        balances_by_seniority: dict[str, float] = defaultdict(float)
        balances_by_collateral: dict[str, float] = defaultdict(float)
        for position in positions:
            balance = position.get("balance", 0.0)
            rec_pct = position.get("recovery_pct", 0.0)
            seniority = position.get("seniority", "unknown")
            collateral = position.get("collateral_type", "unknown")
            seniority_breakdown[seniority] += balance * rec_pct
            balances_by_seniority[seniority] += balance
            collateral_breakdown[collateral] += balance * rec_pct
            balances_by_collateral[collateral] += balance
        seniority_rates = {
            key: round((seniority_breakdown[key] / balances_by_seniority[key]) if balances_by_seniority[key] else 0.0, 2)
            for key in balances_by_seniority
        }
        collateral_rates = {
            key: round((collateral_breakdown[key] / balances_by_collateral[key]) if balances_by_collateral[key] else 0.0, 2)
            for key in balances_by_collateral
        }
        data = {
            "overall_recovery_pct": round(overall_recovery, 2),
            "seniority_recovery_pct": seniority_rates,
            "collateral_recovery_pct": collateral_rates,
            "portfolio_lgd_pct": round(100 - overall_recovery, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("recovery_rate_estimator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
