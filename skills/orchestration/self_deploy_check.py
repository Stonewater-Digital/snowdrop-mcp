"""Check for unpushed commits and auto-push to trigger CI/CD.

Executive Summary:
    A heartbeat skill Snowdrop invokes periodically (cron on snowdrop-node or
    Cloud Scheduler) to detect unpushed commits on main and push them to
    origin, triggering the Cloud Build CI/CD pipeline.

Table of Contents:
    - TOOL_META
    - self_deploy_check()
"""
from __future__ import annotations

import subprocess
from datetime import datetime, timezone
from typing import Any


TOOL_META: dict[str, Any] = {
    "name": "self_deploy_check",
    "description": (
        "Detect unpushed commits on the current branch and push to origin/main "
        "to trigger Cloud Build CI/CD. Returns a summary of pushed commits or "
        "'nothing to deploy' if HEAD matches origin/main."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "dry_run": {
                "type": "boolean",
                "default": False,
                "description": "If true, report unpushed commits without actually pushing.",
            },
        },
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["ok", "error"]},
            "data": {"type": "object"},
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "data", "timestamp"],
    },
}


def _run(cmd: list[str], cwd: str | None = None) -> subprocess.CompletedProcess:
    """Run a subprocess with stdout/stderr capture."""
    return subprocess.run(
        cmd, capture_output=True, text=True, timeout=30, cwd=cwd,
    )


def self_deploy_check(dry_run: bool = False) -> dict[str, Any]:
    """Check for unpushed commits and optionally push to trigger CI/CD.

    Args:
        dry_run: If True, only report what would be pushed without pushing.

    Returns:
        Standard Snowdrop response dict with status, data, and timestamp.
    """
    ts = datetime.now(timezone.utc).isoformat()

    try:
        # Fetch latest remote state
        fetch = _run(["git", "fetch", "origin", "main"])
        if fetch.returncode != 0:
            return {
                "status": "error",
                "data": {"error": f"git fetch failed: {fetch.stderr.strip()}"},
                "timestamp": ts,
            }

        # Check for unpushed commits
        log = _run(["git", "log", "origin/main..HEAD", "--oneline"])
        if log.returncode != 0:
            return {
                "status": "error",
                "data": {"error": f"git log failed: {log.stderr.strip()}"},
                "timestamp": ts,
            }

        commits = [line for line in log.stdout.strip().splitlines() if line]

        if not commits:
            return {
                "status": "ok",
                "data": {
                    "action": "nothing_to_deploy",
                    "message": "HEAD matches origin/main — no unpushed commits.",
                    "commit_count": 0,
                },
                "timestamp": ts,
            }

        if dry_run:
            return {
                "status": "ok",
                "data": {
                    "action": "dry_run",
                    "message": f"{len(commits)} unpushed commit(s) detected (dry run — not pushed).",
                    "commit_count": len(commits),
                    "commits": commits,
                },
                "timestamp": ts,
            }

        # Push to origin main
        push = _run(["git", "push", "origin", "main"])
        if push.returncode != 0:
            return {
                "status": "error",
                "data": {"error": f"git push failed: {push.stderr.strip()}"},
                "timestamp": ts,
            }

        _log_lesson(f"self_deploy_check: pushed {len(commits)} commit(s) to origin/main")

        return {
            "status": "ok",
            "data": {
                "action": "pushed",
                "message": f"Pushed {len(commits)} commit(s) to origin/main — CI/CD triggered.",
                "commit_count": len(commits),
                "commits": commits,
            },
            "timestamp": ts,
        }

    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "data": {"error": "Git command timed out after 30s"},
            "timestamp": ts,
        }
    except Exception as exc:
        _log_lesson(f"self_deploy_check error: {exc}")
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": ts,
        }


def _log_lesson(message: str) -> None:
    """Append a lesson to the lessons log."""
    try:
        from skills.utils import log_lesson
        log_lesson(message)
    except Exception:
        pass
