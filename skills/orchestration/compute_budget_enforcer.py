"""Enforce compute guardrails for OpenRouter and related calls."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "compute_budget_enforcer",
    "description": "Makes sure Snowdrop does not exceed the $50/day compute budget.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "daily_spend_usd": {"type": "number"},
            "pending_call_cost": {"type": "number"},
            "daily_cap_usd": {"type": "number", "default": 50.0},
        },
        "required": ["daily_spend_usd", "pending_call_cost"],
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


def compute_budget_enforcer(
    daily_spend_usd: float,
    pending_call_cost: float,
    daily_cap_usd: float = 50.0,
    **_: Any,
) -> dict[str, Any]:
    """Decide whether the next compute call is allowed.

    Args:
        daily_spend_usd: Amount already spent today.
        pending_call_cost: Estimated cost of the next model call.
        daily_cap_usd: Maximum allowed daily spend ceiling.

    Returns:
        Envelope with allowance decision, projected spend, and utilization percentage.
    """

    try:
        if daily_cap_usd <= 0:
            raise ValueError("daily_cap_usd must be positive")

        projected = daily_spend_usd + pending_call_cost
        allowed = projected <= daily_cap_usd
        remaining = max(daily_cap_usd - daily_spend_usd, 0)
        utilization_pct = min(daily_spend_usd / daily_cap_usd * 100, 100)

        data = {
            "allowed": allowed,
            "projected_spend": round(projected, 4),
            "remaining": round(remaining, 4),
            "utilization_pct": round(utilization_pct, 2),
        }

        if not allowed:
            _log_lesson(
                "compute_budget_enforcer",
                f"Budget exceeded: projected ${projected:.2f} against ${daily_cap_usd:.2f}",
            )

        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("compute_budget_enforcer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
