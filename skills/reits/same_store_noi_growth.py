"""Compare same-store NOI year over year."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "same_store_noi_growth",
    "description": "Calculates YoY same-store NOI growth and contribution analysis.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "prior_noi": {"type": "number"},
            "current_noi": {"type": "number"},
            "expansion_noi": {"type": "number", "default": 0.0},
            "disposition_noi": {"type": "number", "default": 0.0},
        },
        "required": ["prior_noi", "current_noi"],
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def same_store_noi_growth(
    prior_noi: float,
    current_noi: float,
    expansion_noi: float = 0.0,
    disposition_noi: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Return growth rates and contribution splits."""
    try:
        base_growth_pct = ((current_noi - prior_noi) / prior_noi * 100) if prior_noi else 0.0
        same_store_noi = current_noi - expansion_noi + disposition_noi
        same_store_growth_pct = ((same_store_noi - prior_noi) / prior_noi * 100) if prior_noi else 0.0
        contribution = {
            "same_store": round(same_store_noi - prior_noi, 2),
            "expansion": round(expansion_noi, 2),
            "dispositions": round(-disposition_noi, 2),
        }
        data = {
            "reported_growth_pct": round(base_growth_pct, 2),
            "same_store_growth_pct": round(same_store_growth_pct, 2),
            "growth_contribution": contribution,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("same_store_noi_growth", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
