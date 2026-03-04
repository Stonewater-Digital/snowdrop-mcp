"""Format chart-ready datasets for Snowdrop reports."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "chart_data_formatter",
    "description": "Normalizes data into Chart.js/Plotly friendly schema with labels/datasets.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "data": {"type": "array", "items": {"type": "object"}},
            "chart_type": {
                "type": "string",
                "enum": ["line", "bar", "pie", "candlestick"],
            },
            "x_field": {"type": "string"},
            "y_fields": {"type": "array", "items": {"type": "string"}},
            "title": {"type": "string"},
        },
        "required": ["data", "chart_type", "x_field", "y_fields", "title"],
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

_COLOR_PALETTE = ["#4C82FB", "#7F57FF", "#F7B500", "#FF6B6B", "#2EC4B6"]


def chart_data_formatter(
    data: list[dict[str, Any]],
    chart_type: str,
    x_field: str,
    y_fields: list[str],
    title: str,
    **_: Any,
) -> dict[str, Any]:
    """Return normalized chart schema."""
    try:
        if not data:
            raise ValueError("data cannot be empty")
        if not y_fields:
            raise ValueError("y_fields required")

        labels = [row.get(x_field) for row in data]
        datasets = []
        for idx, field in enumerate(y_fields):
            values = [row.get(field) for row in data]
            datasets.append(
                {
                    "label": field,
                    "data": values,
                    "borderColor": _COLOR_PALETTE[idx % len(_COLOR_PALETTE)],
                    "backgroundColor": _COLOR_PALETTE[idx % len(_COLOR_PALETTE)],
                }
            )

        schema = {
            "type": chart_type,
            "title": title,
            "labels": labels,
            "datasets": datasets,
            "axes": {
                "x": {"field": x_field},
                "y": {"fields": y_fields},
            },
        }
        return {
            "status": "success",
            "data": schema,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("chart_data_formatter", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
