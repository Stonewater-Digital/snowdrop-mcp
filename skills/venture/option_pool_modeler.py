"""Model ESOP pool expansion and dilution impact."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "option_pool_modeler",
    "description": "Evaluates current and proposed option pool sizing plus dilution to shareholders.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "current_pool_shares": {"type": "integer"},
            "current_pool_allocated": {"type": "integer"},
            "total_shares_outstanding": {"type": "integer"},
            "proposed_pool_increase_pct": {"type": "number"},
            "new_round_pre_money": {"type": ["number", "null"], "default": None},
        },
        "required": [
            "current_pool_shares",
            "current_pool_allocated",
            "total_shares_outstanding",
            "proposed_pool_increase_pct",
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


def option_pool_modeler(
    current_pool_shares: int,
    current_pool_allocated: int,
    total_shares_outstanding: int,
    proposed_pool_increase_pct: float,
    new_round_pre_money: float | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Return utilization, dilution, and post-expansion pool stats."""
    try:
        if total_shares_outstanding <= 0:
            raise ValueError("total_shares_outstanding must be positive")
        utilization = current_pool_allocated / max(current_pool_shares, 1)
        new_pool_shares = int(current_pool_shares * (1 + proposed_pool_increase_pct / 100))
        added_shares = new_pool_shares - current_pool_shares
        dilution = added_shares / (total_shares_outstanding + added_shares) * 100
        effective_pre = None
        if new_round_pre_money:
            effective_pre = new_round_pre_money - (new_round_pre_money * dilution / 100)
        data = {
            "current_pool_pct": round(current_pool_shares / total_shares_outstanding * 100, 2),
            "utilization_pct": round(utilization * 100, 2),
            "new_pool_shares": new_pool_shares,
            "dilution_from_expansion_pct": round(dilution, 4),
            "effective_pre_money": round(effective_pre, 2) if effective_pre else None,
            "shares_available_for_grants": max(new_pool_shares - current_pool_allocated, 0),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("option_pool_modeler", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
