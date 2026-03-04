"""Track tenant concentration risk."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "tenant_concentration_tracker",
    "description": "Flags top tenant exposure versus single-tenant and top-10 limits.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "tenants": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "rent_pct": {"type": "number"},
                    },
                    "required": ["name", "rent_pct"],
                },
            },
            "single_tenant_limit_pct": {"type": "number", "default": 5.0},
            "top_ten_limit_pct": {"type": "number", "default": 30.0},
        },
        "required": ["tenants"],
    },
    "outputSchema": {"type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def tenant_concentration_tracker(
    tenants: list[dict[str, Any]],
    single_tenant_limit_pct: float = 5.0,
    top_ten_limit_pct: float = 30.0,
    **_: Any,
) -> dict[str, Any]:
    """Return tenant concentration stats."""
    try:
        sorted_tenants = sorted(tenants, key=lambda t: t.get("rent_pct", 0.0), reverse=True)
        top_ten_total = sum(item.get("rent_pct", 0.0) for item in sorted_tenants[:10])
        largest = sorted_tenants[0] if sorted_tenants else {"name": "", "rent_pct": 0.0}
        data = {
            "largest_tenant": largest,
            "top_ten_rent_pct": round(top_ten_total, 2),
            "single_tenant_breach": largest.get("rent_pct", 0.0) > single_tenant_limit_pct,
            "top_ten_breach": top_ten_total > top_ten_limit_pct,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("tenant_concentration_tracker", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
