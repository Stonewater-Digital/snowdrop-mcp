"""Analyze geographic concentration across markets."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "geographic_concentration_analyzer",
    "description": "Calculates HHI by region and flags concentration against limits.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "exposures": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {"region": {"type": "string"}, "exposure_pct": {"type": "number"}},
                    "required": ["region", "exposure_pct"],
                },
            },
            "limit_pct": {"type": "number", "default": 25.0},
        },
        "required": ["exposures"],
    },
    "outputSchema": {"type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def geographic_concentration_analyzer(exposures: list[dict[str, Any]], limit_pct: float = 25.0, **_: Any) -> dict[str, Any]:
    """Return geographic concentration insights."""
    try:
        hhi = sum((item.get("exposure_pct", 0.0) / 100) ** 2 for item in exposures)
        breaches = [item for item in exposures if item.get("exposure_pct", 0.0) > limit_pct]
        top_region = max(exposures, key=lambda x: x.get("exposure_pct", 0.0)) if exposures else {"region": "", "exposure_pct": 0.0}
        data = {
            "hhi": round(hhi, 4),
            "breaches": breaches,
            "top_region": top_region,
            "diversification_warning": hhi > 0.18,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("geographic_concentration_analyzer", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
