"""Build digest content for agents."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "digest_builder",
    "description": "Creates readable digests summarizing activity, metrics, and tips per agent.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "agent_id": {"type": "string"},
            "period": {"type": "string", "enum": ["daily", "weekly"]},
            "activity": {"type": "array", "items": {"type": "object"}},
            "metrics": {"type": "object"},
            "announcements": {"type": "array", "items": {"type": "string"}},
            "educational_tip": {"type": "string"},
        },
        "required": ["agent_id", "period", "activity", "metrics", "announcements", "educational_tip"],
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


def digest_builder(
    agent_id: str,
    period: str,
    activity: list[dict[str, Any]],
    metrics: dict[str, Any],
    announcements: list[str],
    educational_tip: str,
    **_: Any,
) -> dict[str, Any]:
    """Return markdown digest text and metadata."""
    try:
        highlights = activity[:3]
        highlight_lines = "\n".join(f"- {item.get('description')}" for item in highlights)
        announcement_lines = "\n".join(f"- {item}" for item in announcements) or "- No announcements"
        digest_md = f"""# Snowdrop Digest ({period.title()})

## Highlights
{highlight_lines or '- No highlights'}

## Usage Summary
- Skills used: {metrics.get('skills_used', 0)}
- API calls: {metrics.get('api_calls', 0)}
- Spend: ${metrics.get('total_spend', 0):,.2f}

## Announcements
{announcement_lines}

## Billing Snapshot
Your spend this period totals ${metrics.get('total_spend', 0):,.2f}.

## Tip of the Week
{educational_tip}
"""
        subject_line = f"Snowdrop {period.title()} Digest for {agent_id}"
        key_stat = f"{metrics.get('api_calls', 0)} API calls"
        data = {
            "digest_md": digest_md.strip(),
            "subject_line": subject_line,
            "key_stat": key_stat,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("digest_builder", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
