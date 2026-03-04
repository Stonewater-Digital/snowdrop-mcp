"""Aggregate dashboard panels for Snowdrop leadership."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "dashboard_aggregator",
    "description": "Groups panels by source, surfaces alerts, and crafts summary sentences.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "panels": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["panels"],
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


def dashboard_aggregator(panels: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Aggregate panels into a unified dashboard."""
    try:
        grouped: dict[str, list[dict[str, Any]]] = {}
        alerts: list[str] = []
        for panel in panels:
            category = panel.get("data_source", "general")
            grouped.setdefault(category, []).append(panel)
            if panel.get("trend") == "down" and panel.get("value"):
                alerts.append(f"{panel.get('panel_name')} trending down")

        summary_sentence = _build_summary(panels)
        data = {
            "dashboard": grouped,
            "panels": panels,
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "alerts": alerts,
            "summary_sentence": summary_sentence,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("dashboard_aggregator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _build_summary(panels: list[dict[str, Any]]) -> str:
    if not panels:
        return "No panels available"
    highlights = sorted(panels, key=lambda p: abs(float(p.get("value", 0.0))), reverse=True)[:2]
    parts = [f"{item.get('panel_name')} at {item.get('value')} ({item.get('trend')})" for item in highlights]
    return "; ".join(parts)


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
