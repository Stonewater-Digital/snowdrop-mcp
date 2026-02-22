"""Monitor credit facility utilization and pricing tiers."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "credit_facility_utilization_monitor",
    "description": "Aggregates revolver/DDTL/term loan utilization and identifies spread tiers.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "facilities": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["facilities"],
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


def credit_facility_utilization_monitor(facilities: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return utilization and spread grid diagnostics."""
    try:
        total_commitment = sum(f.get("commitment", 0.0) for f in facilities)
        total_drawn = sum(f.get("drawn", 0.0) + f.get("letters_of_credit", 0.0) for f in facilities)
        total_available = total_commitment - total_drawn
        utilization = total_drawn / total_commitment * 100 if total_commitment else 0.0
        spread_tier = None
        for facility in facilities:
            grid = sorted(facility.get("spread_grid", []), key=lambda x: x.get("utilization_threshold", 0))
            for tier in grid:
                if utilization >= tier.get("utilization_threshold", 0):
                    spread_tier = tier
        springing = utilization > 85
        facility_rows = []
        for facility in facilities:
            commit = facility.get("commitment", 0.0)
            drawn = facility.get("drawn", 0.0)
            facility_rows.append(
                {
                    "name": facility.get("name"),
                    "type": facility.get("type"),
                    "commitment": commit,
                    "drawn": drawn,
                    "utilization_pct": round(drawn / commit * 100, 2) if commit else 0.0,
                }
            )
        data = {
            "total_commitment": round(total_commitment, 2),
            "total_drawn": round(total_drawn, 2),
            "total_available": round(total_available, 2),
            "overall_utilization_pct": round(utilization, 2),
            "current_spread_tier": spread_tier,
            "springing_covenants_active": springing,
            "facilities": facility_rows,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("credit_facility_utilization_monitor", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
