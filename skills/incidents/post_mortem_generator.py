"""Generate blameless post-mortems for Snowdrop incidents."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "post_mortem_generator",
    "description": "Creates structured post-mortem Markdown with action items and lessons learned.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "incident": {
                "type": "object",
                "description": (
                    "Incident dictionary containing title, severity, timeline, root cause, contributing"
                    " factors, detection_method, resolution, and duration_minutes."
                ),
            }
        },
        "required": ["incident"],
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


def post_mortem_generator(incident: dict[str, Any], **_: Any) -> dict[str, Any]:
    """Render a blameless post-mortem for the provided incident."""
    try:
        required = [
            "title",
            "severity",
            "timeline",
            "root_cause",
            "contributing_factors",
            "detection_method",
            "resolution",
            "duration_minutes",
        ]
        missing = [field for field in required if field not in incident]
        if missing:
            raise ValueError(f"Incident missing fields: {', '.join(missing)}")

        timeline_md = "\n".join(
            f"- {item.get('timestamp')}: {item.get('event')}" for item in incident.get("timeline", [])
        )
        summary = (
            f"Incident '{incident['title']}' ({incident['severity']}) lasted "
            f"{incident['duration_minutes']} minutes and was detected via {incident['detection_method']}."
        )
        impact = "Affected systems: " + ", ".join(incident.get("affected_systems", [])) if incident.get("affected_systems") else "Impact details pending."

        action_items = _derive_actions(
            incident.get("contributing_factors", []),
            incident.get("resolution", ""),
        )
        lessons = [
            "Codify detection improvements",
            "Validate runbooks against scenario",
        ]

        markdown = f"""# Post-Mortem: {incident['title']}

**Severity:** {incident['severity']}  \\
**Duration:** {incident['duration_minutes']} minutes  \\
**Detection:** {incident['detection_method']}  \\
**Summary:** {summary}

## Impact
{impact}

## Timeline
{timeline_md}

## Root Cause
{incident['root_cause']}

## Resolution
{incident['resolution']}

## Action Items
{_actions_md(action_items)}

## Lessons Learned
- {lessons[0]}
- {lessons[1]}
"""

        data = {
            "post_mortem_md": markdown.strip(),
            "action_items": action_items,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("post_mortem_generator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _derive_actions(factors: list[str], resolution: str) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []
    for factor in factors:
        actions.append(
            {
                "action": f"Address contributing factor: {factor}",
                "owner": "Snowdrop Ops",
                "due_date": None,
                "status": "pending",
            }
        )
    if resolution:
        actions.append(
            {
                "action": f"Backtest and automate fix: {resolution[:120]}",
                "owner": "Automation Guild",
                "due_date": None,
                "status": "pending",
            }
        )
    return actions


def _actions_md(items: list[dict[str, Any]]) -> str:
    if not items:
        return "- No follow-up required"
    lines = []
    for item in items:
        lines.append(
            f"- [ ] {item['action']} (Owner: {item['owner']}, Status: {item['status']})"
        )
    return "\n".join(lines)


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
