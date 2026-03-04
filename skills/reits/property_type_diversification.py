"""Measure diversification across property types."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "property_type_diversification",
    "description": "Computes HHI concentration and highlights overweight property types.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "property_mix": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {"type": {"type": "string"}, "exposure_pct": {"type": "number"}},
                    "required": ["type", "exposure_pct"],
                },
            },
            "limit_pct": {"type": "number", "default": 40.0},
        },
        "required": ["property_mix"],
    },
    "outputSchema": {"type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def property_type_diversification(property_mix: list[dict[str, Any]], limit_pct: float = 40.0, **_: Any) -> dict[str, Any]:
    """Return diversification metrics."""
    try:
        hhi = sum((item.get("exposure_pct", 0.0) / 100) ** 2 for item in property_mix)
        overweight = [item for item in property_mix if item.get("exposure_pct", 0.0) > limit_pct]
        data = {
            "hhi": round(hhi, 4),
            "overweight_properties": overweight,
            "even_mix_warning": hhi > 0.2,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("property_type_diversification", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
