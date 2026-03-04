"""Size credit enhancement for securitizations."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "credit_enhancement_calculator",
    "description": "Determines required subordination and overcollateralization to hit target ratings.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "pool_balance": {"type": "number"},
            "target_rating": {
                "type": "string",
                "enum": ["AAA", "AA", "A", "BBB"],
            },
            "base_loss_pct": {"type": "number"},
            "stress_multipliers": {"type": "object"},
        },
        "required": ["pool_balance", "target_rating", "base_loss_pct", "stress_multipliers"],
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


def credit_enhancement_calculator(
    pool_balance: float,
    target_rating: str,
    base_loss_pct: float,
    stress_multipliers: dict[str, float],
    **_: Any,
) -> dict[str, Any]:
    """Return enhancement requirements for the chosen rating."""
    try:
        multiplier = stress_multipliers.get(target_rating)
        if multiplier is None:
            raise ValueError("Missing stress multiplier for rating")
        stressed_loss = pool_balance * (base_loss_pct / 100) * multiplier
        required_sub = stressed_loss / pool_balance * 100
        excess_spread = max(0, 5 - base_loss_pct)
        required_oc = max(required_sub - excess_spread, 0)
        total_enhancement = required_sub + required_oc
        senior_size = pool_balance * (1 - total_enhancement / 100)
        data = {
            "required_subordination_pct": round(required_sub, 2),
            "required_oc_pct": round(required_oc, 2),
            "total_enhancement_pct": round(total_enhancement, 2),
            "senior_tranche_size": round(senior_size, 2),
            "enhancement_sufficient": total_enhancement >= required_sub,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("credit_enhancement_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
