"""Create backup snapshot manifests for Snowdrop state."""
from __future__ import annotations

import hashlib
import os
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "backup_snapshot_creator",
    "description": "Compiles file manifests for Snowdrop backups (no writes performed).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "snapshot_type": {
                "type": "string",
                "enum": ["full", "config_only", "ledger_only"],
            }
        },
        "required": ["snapshot_type"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "manifest": {"type": "object"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def backup_snapshot_creator(snapshot_type: str, **_: Any) -> dict[str, Any]:
    """Return a manifest of files and checksums for Thunder review."""

    try:
        files = _select_files(snapshot_type)
        entries: list[dict[str, Any]] = []
        total_size = 0
        for path in files:
            if not os.path.isfile(path):
                continue
            size = os.path.getsize(path)
            checksum = _sha256(path)
            total_size += size
            entries.append({"path": path, "size_bytes": size, "sha256": checksum})

        manifest = {
            "snapshot_type": snapshot_type,
            "files": entries,
            "total_size_bytes": total_size,
            "submission_status": "pending_thunder_approval",
        }
        return {
            "status": "success",
            "data": {"manifest": manifest},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("backup_snapshot_creator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _select_files(snapshot_type: str) -> list[str]:
    if snapshot_type not in {"full", "config_only", "ledger_only"}:
        raise ValueError("snapshot_type must be full, config_only, or ledger_only")
    config_files = _list_files("config")
    ledger_files = _list_files("skills/ghost_ledger") + ["ghost_ledger.py"]
    registry_files = [
        "skills/__init__.py",
        "skills/skill_builder.py",
        "skills/mcp_server.py",
    ]
    if snapshot_type == "config_only":
        return config_files
    if snapshot_type == "ledger_only":
        return ledger_files
    return sorted(set(config_files + ledger_files + registry_files))


def _list_files(root: str) -> list[str]:
    collected: list[str] = []
    if not os.path.isdir(root):
        return collected
    for base, _, files in os.walk(root):
        for filename in files:
            collected.append(os.path.join(base, filename))
    return sorted(collected)


def _sha256(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while chunk := handle.read(65536):
            digest.update(chunk)
    return digest.hexdigest()


def _log_lesson(skill_name: str, error: str) -> None:
    """Append a Ralph Wiggum lesson entry."""

    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
