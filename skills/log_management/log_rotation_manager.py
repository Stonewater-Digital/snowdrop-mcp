"""Recommend log rotation actions based on size and age."""
from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "log_rotation_manager",
    "description": "Evaluates log files and proposes rotation/compression/deletion actions.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "log_files": {"type": "array", "items": {"type": "object"}},
            "current_date": {"type": "string"},
        },
        "required": ["log_files", "current_date"],
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


def log_rotation_manager(
    log_files: list[dict[str, Any]],
    current_date: str,
    **_: Any,
) -> dict[str, Any]:
    """Return rotation recommendations for log files."""
    try:
        today = datetime.fromisoformat(current_date).date()
        actions = []
        total_size_mb = 0.0
        files_to_rotate = 0
        files_to_delete = 0
        space_freed_mb = 0.0

        for entry in log_files:
            path = Path(entry.get("path", ""))
            if not path.exists():
                continue
            max_size = float(entry.get("max_size_mb", 100))
            max_age = int(entry.get("max_age_days", 7))
            compress = bool(entry.get("compress", False))
            stats = path.stat()
            size_mb = stats.st_size / (1024 * 1024)
            total_size_mb += size_mb
            modified = datetime.fromtimestamp(stats.st_mtime, tz=timezone.utc).date()
            age_days = (today - modified).days

            if age_days > max_age * 2:
                actions.append(
                    {
                        "path": str(path),
                        "action": "delete",
                        "reason": f"age {age_days}d exceeds {max_age * 2}d",
                    }
                )
                files_to_delete += 1
                space_freed_mb += size_mb
                continue

            rotate_needed = size_mb > max_size or age_days > max_age
            if rotate_needed:
                files_to_rotate += 1
                rotate_action = {
                    "path": str(path),
                    "action": "rotate",
                    "reason": "size" if size_mb > max_size else "age",
                    "suggested_name": f"{path}.{today.isoformat()}",
                }
                if compress:
                    rotate_action["post_action"] = "compress"
                actions.append(rotate_action)

        data = {
            "actions": actions,
            "total_log_size_mb": round(total_size_mb, 2),
            "files_to_rotate": files_to_rotate,
            "files_to_delete": files_to_delete,
            "space_freed_mb": round(space_freed_mb, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("log_rotation_manager", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
