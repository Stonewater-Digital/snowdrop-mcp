"""Map skill dependencies and required env vars."""
from __future__ import annotations

import os
import re
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "skill_dependency_mapper",
    "description": "Scans skill files for env vars, internal imports, and external API references.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "skill_directory": {"type": "string", "default": "skills/"},
        },
        "required": [],
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

_ENV_PATTERN = re.compile(r"os\.getenv\(['\"]([A-Z0-9_]+)['\"]")
_IMPORT_PATTERN = re.compile(r"from\s+skills\.([\w\.]+)\s+import|import\s+skills\.([\w\.]+)")
_URL_PATTERN = re.compile(r"https?://([a-zA-Z0-9\.-]+)")


def skill_dependency_mapper(skill_directory: str = "skills/", **_: Any) -> dict[str, Any]:
    """Return dependency metadata for each skill file."""
    try:
        skill_info = []
        for root, _, files in os.walk(skill_directory):
            for filename in files:
                if not filename.endswith(".py") or filename == "__init__.py":
                    continue
                path = os.path.join(root, filename)
                with open(path, "r", encoding="utf-8") as handle:
                    content = handle.read()
                env_vars = set(_ENV_PATTERN.findall(content))
                imports = {
                    match[0] or match[1]
                    for match in _IMPORT_PATTERN.findall(content)
                    if (match[0] or match[1])
                }
                external_apis = set(_URL_PATTERN.findall(content))
                ready_to_run = all(os.getenv(var) for var in env_vars)
                skill_info.append(
                    {
                        "skill_path": path,
                        "env_vars_required": sorted(env_vars),
                        "internal_deps": sorted(imports),
                        "external_apis": sorted(external_apis),
                        "ready_to_run": ready_to_run,
                    }
                )
        data = {"skills": skill_info}
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("skill_dependency_mapper", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
