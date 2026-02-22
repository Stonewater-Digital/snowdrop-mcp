"""
Executive Summary: Context7 doc freshness verification — flags stale skills and reports overall freshness score.
Inputs: skills (list of dicts: skill_name str, current_version str, last_checked str ISO date)
Outputs: stale_skills (list), fresh_count (int), stale_count (int), freshness_score_pct (float)
MCP Tool Name: agent_skill_version_checker
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone, timedelta

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "agent_skill_version_checker",
    "description": (
        "Verifies Context7 documentation freshness for registered skills. "
        "Flags any skill whose last_checked date is older than 7 days and "
        "returns a freshness score as a percentage of up-to-date skills."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "skills": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "skill_name":      {"type": "string"},
                        "current_version": {"type": "string"},
                        "last_checked":    {"type": "string", "format": "date-time"},
                    },
                    "required": ["skill_name", "current_version", "last_checked"],
                },
                "description": "List of skill descriptors with version and last-checked timestamp.",
            }
        },
        "required": ["skills"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "stale_skills":        {"type": "array"},
            "fresh_count":         {"type": "integer"},
            "stale_count":         {"type": "integer"},
            "freshness_score_pct": {"type": "number"},
            "status":              {"type": "string"},
            "timestamp":           {"type": "string"},
        },
        "required": ["stale_skills", "fresh_count", "stale_count", "freshness_score_pct", "status", "timestamp"],
    },
}

STALENESS_THRESHOLD_DAYS: int = 7


def agent_skill_version_checker(skills: list[dict[str, Any]]) -> dict[str, Any]:
    """Check Context7 documentation freshness for each registered skill.

    Args:
        skills: List of skill descriptors. Each dict must contain:
            - skill_name (str): Unique identifier for the skill.
            - current_version (str): Semver or arbitrary version string.
            - last_checked (str): ISO 8601 datetime of the last doc check.

    Returns:
        dict with keys:
            - status (str): "success" or "error".
            - stale_skills (list[dict]): Skills older than STALENESS_THRESHOLD_DAYS.
            - fresh_count (int): Number of skills checked within the threshold window.
            - stale_count (int): Number of skills past the threshold.
            - freshness_score_pct (float): Percentage of skills that are fresh (0–100).
            - timestamp (str): ISO 8601 UTC timestamp of execution.
    """
    try:
        now_utc: datetime = datetime.now(timezone.utc)
        threshold: timedelta = timedelta(days=STALENESS_THRESHOLD_DAYS)

        stale_skills: list[dict[str, Any]] = []
        fresh_count: int = 0

        for skill in skills:
            skill_name: str = skill.get("skill_name", "unknown")
            version: str = skill.get("current_version", "0.0.0")
            raw_checked: str = skill.get("last_checked", "")

            try:
                last_checked_dt: datetime = datetime.fromisoformat(raw_checked)
                # Ensure timezone-aware for comparison
                if last_checked_dt.tzinfo is None:
                    last_checked_dt = last_checked_dt.replace(tzinfo=timezone.utc)
            except ValueError:
                # Unparseable date — treat as never checked
                last_checked_dt = datetime.min.replace(tzinfo=timezone.utc)

            age: timedelta = now_utc - last_checked_dt
            days_old: int = age.days

            if age > threshold:
                days_overdue: int = days_old - STALENESS_THRESHOLD_DAYS
                stale_skills.append(
                    {
                        "skill_name":    skill_name,
                        "version":       version,
                        "last_checked":  raw_checked,
                        "days_old":      days_old,
                        "days_overdue":  days_overdue,
                    }
                )
            else:
                fresh_count += 1

        total: int = len(skills)
        stale_count: int = len(stale_skills)
        freshness_score_pct: float = (fresh_count / total * 100.0) if total > 0 else 0.0

        # Sort stale skills by days_overdue descending — most urgent first
        stale_skills.sort(key=lambda s: s["days_overdue"], reverse=True)

        return {
            "status":              "success",
            "stale_skills":        stale_skills,
            "fresh_count":         fresh_count,
            "stale_count":         stale_count,
            "freshness_score_pct": round(freshness_score_pct, 2),
            "timestamp":           now_utc.isoformat(),
        }

    except Exception as e:
        logger.error(f"agent_skill_version_checker failed: {e}")
        _log_lesson(f"agent_skill_version_checker: {e}")
        return {
            "status":    "error",
            "error":     str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    """Append a failure lesson to the shared lessons log.

    Args:
        message: Human-readable description of the failure.
    """
    with open("logs/lessons.md", "a") as f:
        f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
