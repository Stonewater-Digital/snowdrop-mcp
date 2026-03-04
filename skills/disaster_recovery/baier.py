"""Backup integrity verifier (BAIER)."""
from __future__ import annotations

import hashlib
import os
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "backup_verifier",
    "description": "Checks backup manifests for missing or corrupted files using SHA-256 hashes.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "manifest": {"type": "object"},
            "backup_location": {"type": "string"},
        },
        "required": ["manifest", "backup_location"],
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


def backup_verifier(
    manifest: dict[str, Any],
    backup_location: str,
    **_: Any,
) -> dict[str, Any]:
    """Return verification summary for backup manifest."""
    try:
        files = manifest.get("files", [])
        if not files:
            raise ValueError("manifest.files cannot be empty")
        files_checked = 0
        files_ok = 0
        missing: list[str] = []
        corrupted: list[str] = []
        for file_entry in files:
            rel_path = file_entry.get("path")
            expected_hash = file_entry.get("expected_sha256")
            full_path = os.path.join(backup_location, rel_path)
            files_checked += 1
            if not os.path.exists(full_path):
                missing.append(rel_path)
                continue
            computed_hash = _sha256(full_path)
            if computed_hash != expected_hash:
                corrupted.append(rel_path)
                continue
            files_ok += 1
        verified = not missing and not corrupted
        data = {
            "verified": verified,
            "files_checked": files_checked,
            "files_ok": files_ok,
            "files_missing": missing,
            "files_corrupted": corrupted,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("backup_verifier", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _sha256(path: str) -> str:
    hasher = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
