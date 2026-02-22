"""Generate executive-ready markdown briefings."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "executive_summary_generator",
    "description": "Formats operational metrics into a Thunder-ready briefing.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "metrics": {"type": "object"},
        },
        "required": ["metrics"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "summary": {"type": "string"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def executive_summary_generator(metrics: dict[str, Any], **_: Any) -> dict[str, Any]:
    """Return formatted markdown summarizing operational health."""

    try:
        summary = _build_summary(metrics)
        return {
            "status": "success",
            "data": {"summary": summary},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("executive_summary_generator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _build_summary(metrics: dict[str, Any]) -> str:
    revenue = metrics.get("revenue_24h", 0)
    expenses = metrics.get("expenses_24h", 0)
    open_positions = metrics.get("open_positions", 0)
    active_agents = metrics.get("active_agents", 0)
    reconciliation_status = metrics.get("reconciliation_status", "unknown")
    alerts = metrics.get("alerts", [])

    margin = revenue - expenses
    decisions = metrics.get("decisions_needed") or []
    lines = [
        "# Snowdrop Executive Briefing",
        f"**Runway Check:** Revenue (24h) `{revenue:.2f}` vs Expenses `{expenses:.2f}`",
        f"**Operating Margin:** `{margin:.2f}`",
        f"**Open Positions:** `{open_positions}`",
        f"**Active Agents:** `{active_agents}`",
        f"**Ledger Status:** `{reconciliation_status}`",
        "",
        "## Alerts",
    ]
    if alerts:
        for alert in alerts:
            lines.append(f"- {alert}")
    else:
        lines.append("- No blocking alerts.")

    lines.append("\n## Decisions Needed")
    if decisions:
        for idx, decision in enumerate(decisions, 1):
            lines.append(f"{idx}. {decision}")
    else:
        lines.append("- Awaiting Thunder guidance on capital deployment.")

    return "\n".join(lines)


def _log_lesson(skill_name: str, error: str) -> None:
    """Append a Ralph Wiggum lesson entry."""

    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
