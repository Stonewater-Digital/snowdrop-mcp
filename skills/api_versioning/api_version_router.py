"""Route skills to the correct API version."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "api_version_router",
    "description": "Negotiates version routing and flags deprecations for skills.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "requested_version": {"type": "string"},
            "available_versions": {"type": "array", "items": {"type": "string"}},
            "skill_name": {"type": "string"},
            "default_version": {"type": "string", "default": "v1"},
        },
        "required": ["requested_version", "available_versions", "skill_name"],
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


DEPRECATIONS = {
    "v1": {"sunset": "2025-12-31", "skills": ["legacy_skill"]},
}


def api_version_router(
    requested_version: str,
    available_versions: list[str],
    skill_name: str,
    default_version: str = "v1",
    **_: Any,
) -> dict[str, Any]:
    """Return version routing decision with warnings when needed."""
    try:
        available = set(available_versions)
        version = requested_version if requested_version in available else default_version
        skill_available = version in available
        deprecation_info = DEPRECATIONS.get(version)
        warning = None
        sunset_date = None
        if deprecation_info and skill_name in deprecation_info.get("skills", []):
            warning = f"{skill_name} on {version} sunsets soon"
            sunset_date = deprecation_info.get("sunset")
        data = {
            "routed_version": version,
            "skill_available": skill_available,
            "deprecation_warning": warning,
            "sunset_date": sunset_date,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("api_version_router", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
