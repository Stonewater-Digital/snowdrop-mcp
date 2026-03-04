"""Generate weekly status reports."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "status_report_generator",
    "description": "Formats Snowdrop execution updates into a markdown status report.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "completed": {"type": "array", "items": {"type": "string"}},
            "in_progress": {"type": "array", "items": {"type": "string"}},
            "blocked": {"type": "array", "items": {"type": "string"}},
            "metrics": {"type": "object"},
            "highlights": {"type": "array", "items": {"type": "string"}},
            "period": {"type": "string"},
        },
        "required": ["completed", "in_progress", "blocked", "metrics", "highlights", "period"],
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


def status_report_generator(
    completed: list[str],
    in_progress: list[str],
    blocked: list[str],
    metrics: dict[str, Any],
    highlights: list[str],
    period: str,
    **_: Any,
) -> dict[str, Any]:
    """Render a markdown status report."""
    try:
        report = f"""# Snowdrop Status Report — {period}

## Executive Summary
- {highlights[0] if highlights else 'Momentum steady'}

## Accomplishments
{_bulletize(completed)}

## In Progress
{_bulletize(in_progress)}

## Blockers
{_bulletize(blocked)}

## Key Metrics
{_metrics_table(metrics)}

## Next Week Priorities
{_bulletize(highlights)}
"""
        executive_summary = (
            highlights[0]
            if highlights
            else f"Steady execution; revenue ${metrics.get('revenue', 'N/A')}"
        )
        data = {
            "report_md": report.strip(),
            "executive_summary": executive_summary,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("status_report_generator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _bulletize(items: list[str]) -> str:
    if not items:
        return "- None"
    return "\n".join(f"- {item}" for item in items)


def _metrics_table(metrics: dict[str, Any]) -> str:
    if not metrics:
        return "- Metrics unavailable"
    lines = ["| Metric | Value |", "| --- | --- |"]
    for key, value in metrics.items():
        lines.append(f"| {key} | {value} |")
    return "\n".join(lines)


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
