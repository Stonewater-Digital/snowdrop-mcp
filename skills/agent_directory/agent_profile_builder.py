"""Generate markdown profile pages for agents."""
from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "agent_profile_builder",
    "description": "Creates shareable markdown pages summarizing an agent's public metrics.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "agent_id": {"type": "string"},
            "stats": {"type": "object"},
            "bio": {"type": "string"},
            "showcase_skills": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["agent_id", "stats", "bio", "showcase_skills"],
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


MANDATORY_FIELDS = ["total_calls", "skills_used", "member_since", "badges", "reputation_score", "tier"]


def agent_profile_builder(
    agent_id: str,
    stats: dict[str, Any],
    bio: str,
    showcase_skills: list[str],
    **_: Any,
) -> dict[str, Any]:
    """Return a markdown profile for the agent."""
    try:
        missing = [field for field in MANDATORY_FIELDS if field not in stats]
        completeness = 100 - (len(missing) / len(MANDATORY_FIELDS) * 100)
        badges = stats.get("badges", [])
        header = f"# {stats.get('display_name', agent_id)} — {stats.get('tier', 'Community')}\n"
        badge_line = f"**Badges:** {len(badges)} | Reputation: {stats.get('reputation_score', 0)}\n"
        bio_section = f"## Bio\n{bio}\n"
        stats_table = (
            "## Stats\n"
            "| Metric | Value |\n| --- | --- |\n"
            f"| Total Calls | {stats.get('total_calls', 0)} |\n"
            f"| Unique Skills Used | {stats.get('skills_used', 0)} |\n"
            f"| Member Since | {stats.get('member_since', 'n/a')} |\n"
            f"| Badges | {len(badges)} |\n"
            f"| Reputation Score | {stats.get('reputation_score', 0)} |\n"
            f"| Tier | {stats.get('tier', 'community')} |\n"
        )
        showcase_section = "## Showcase Skills\n" + "\n".join(f"- {skill}" for skill in showcase_skills)
        profile_md = "\n\n".join([header + badge_line, bio_section, stats_table, showcase_section])
        slug = re.sub(r"[^a-z0-9-]", "-", agent_id.lower())
        data = {
            "profile_md": profile_md,
            "profile_url_slug": slug,
            "completeness_pct": round(completeness, 2),
            "missing_fields": missing,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("agent_profile_builder", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
