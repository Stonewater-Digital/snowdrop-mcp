"""Project token supply under mint/burn schedules."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "token_supply_modeler",
    "description": "Projects circulating supply month by month with mint and burn events.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "initial_supply": {"type": "number"},
            "mint_schedule": {"type": "array", "items": {"type": "object"}},
            "burn_events": {"type": "array", "items": {"type": "object"}},
            "months_to_project": {"type": "integer"},
        },
        "required": [
            "initial_supply",
            "mint_schedule",
            "burn_events",
            "months_to_project",
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


def token_supply_modeler(
    initial_supply: float,
    mint_schedule: list[dict[str, Any]],
    burn_events: list[dict[str, Any]],
    months_to_project: int,
    **_: Any,
) -> dict[str, Any]:
    """Produce the projected supply curve."""
    try:
        if initial_supply <= 0:
            raise ValueError("initial_supply must be positive")
        if months_to_project <= 0:
            raise ValueError("months_to_project must be positive")
        mint_map = {int(item["month"]): float(item.get("amount", 0)) for item in mint_schedule}
        burn_map = {int(item["month"]): float(item.get("amount", 0)) for item in burn_events}
        supply_curve = []
        supply = initial_supply
        total_minted = 0.0
        total_burned = 0.0
        for month in range(1, months_to_project + 1):
            minted = mint_map.get(month, 0.0)
            burned = burn_map.get(month, 0.0)
            total_minted += minted
            total_burned += burned
            supply = max(supply + minted - burned, 0)
            supply_curve.append(
                {
                    "month": month,
                    "supply": round(supply, 2),
                    "minted": minted,
                    "burned": burned,
                }
            )
        net_inflation_pct = round(((supply - initial_supply) / initial_supply) * 100, 4)
        data = {
            "supply_curve": supply_curve,
            "final_supply": round(supply, 2),
            "total_minted": round(total_minted, 2),
            "total_burned": round(total_burned, 2),
            "net_inflation_pct": net_inflation_pct,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("token_supply_modeler", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
