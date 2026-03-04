"""
Executive Summary
-----------------
Cleans up Docker resources on the local machine (HP Spectre / MacBook Pro) to
prevent disk exhaustion. Designed to be called on a schedule by a subagent.
Supports dry-run mode for safe inspection before deletion.

Inputs:
  action        : str   — "prune_images" | "prune_containers" | "prune_volumes"
                          | "prune_all" | "disk_usage"  (required)
  keep_images   : list  — image names/tags to preserve (e.g. ["snowdrop-mcp:latest"])
  dry_run       : bool  — if True, shows what WOULD be deleted without deleting
  min_age_days  : int   — only remove images/containers older than N days (default 1)

Outputs:
  {"status": "ok"|"error", "data": {"freed_bytes": int, "items_removed": int,
   "details": [...], "disk_usage": {...}}, "timestamp": "<ISO8601>"}

MCP Tool Name: docker_cleanup

Agent Notes (Claude Code / Cursor / Codex CLI / Gemini CLI):
  - Run "disk_usage" first to check current state before pruning
  - Always pass keep_images=["snowdrop-mcp:latest"] to protect the live image
  - Schedule: run prune_all weekly; run disk_usage daily and alert if > 80% full
  - dry_run=True is safe to run at any time for inspection
"""

import json
import logging
import os
import subprocess
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

TOOL_META = {
    "name": "docker_cleanup",
    "description": (
        "Clean up Docker images, containers, and volumes on the local machine "
        "to prevent disk exhaustion. Supports dry-run mode. Schedule weekly via subagent. "
        "Always preserve keep_images list (e.g. the live snowdrop-mcp image)."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["prune_images", "prune_containers", "prune_volumes", "prune_all", "disk_usage"],
                "description": "Cleanup operation to perform.",
            },
            "keep_images": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Image names/tags to preserve. Default: ['snowdrop-mcp:latest']",
            },
            "dry_run": {
                "type": "boolean",
                "default": False,
                "description": "If true, shows what would be removed without removing anything.",
            },
            "min_age_days": {
                "type": "integer",
                "default": 1,
                "description": "Only remove images/containers older than N days.",
            },
        },
        "required": ["action"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
        "required": ["status", "data", "timestamp"],
    },
}

_DEFAULT_KEEP = ["snowdrop-mcp:latest", "python:3.11-slim"]


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _wrap(status: str, data: dict) -> dict:
    return {"status": status, "data": data, "timestamp": _now_iso()}


def _run(cmd: list[str]) -> tuple[str, str, int]:
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    return result.stdout.strip(), result.stderr.strip(), result.returncode


def _disk_usage_data() -> dict:
    stdout, _, rc = _run(["docker", "system", "df", "--format", "{{json .}}"])
    if rc != 0:
        stdout, _, _ = _run(["docker", "system", "df"])
        return {"raw": stdout}
    rows = []
    for line in stdout.splitlines():
        line = line.strip()
        if line:
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                rows.append({"raw": line})
    return {"rows": rows}


def _prune_images(keep_images: list[str], dry_run: bool, min_age_days: int) -> dict:
    # List all images to identify candidates
    stdout, _, rc = _run([
        "docker", "images", "--format",
        "{{.Repository}}:{{.Tag}}\t{{.ID}}\t{{.CreatedAt}}\t{{.Size}}"
    ])
    if rc != 0:
        return {"error": "Failed to list images"}

    candidates = []
    kept = []
    for line in stdout.splitlines():
        parts = line.split("\t")
        if len(parts) < 4:
            continue
        name, image_id, created_at, size = parts[0], parts[1], parts[2], parts[3]
        if any(k in name for k in keep_images):
            kept.append(name)
            continue
        if name == "<none>:<none>":  # dangling
            candidates.append({"name": name, "id": image_id, "size": size})
        else:
            candidates.append({"name": name, "id": image_id, "size": size})

    if dry_run:
        return {
            "dry_run": True,
            "would_remove": candidates,
            "would_keep": kept,
            "candidate_count": len(candidates),
        }

    # Prune dangling images, then unused images older than min_age_days
    stdout1, _, _ = _run(["docker", "image", "prune", "-f"])
    stdout2, _, _ = _run([
        "docker", "image", "prune", "-f", "-a",
        "--filter", f"until={min_age_days * 24}h",
    ])
    return {
        "dangling_prune_output": stdout1,
        "aged_prune_output": stdout2,
        "kept": kept,
        "items_removed": len(candidates),
    }


def _prune_containers(dry_run: bool, min_age_days: int) -> dict:
    if dry_run:
        stdout, _, _ = _run([
            "docker", "ps", "-a", "--filter", "status=exited",
            "--format", "{{.Names}}\t{{.Status}}"
        ])
        return {"dry_run": True, "stopped_containers": stdout}
    stdout, _, _ = _run([
        "docker", "container", "prune", "-f",
        "--filter", f"until={min_age_days * 24}h",
    ])
    return {"output": stdout}


def _prune_volumes(dry_run: bool) -> dict:
    if dry_run:
        stdout, _, _ = _run(["docker", "volume", "ls", "--filter", "dangling=true", "-q"])
        return {"dry_run": True, "dangling_volumes": stdout.splitlines()}
    stdout, _, _ = _run(["docker", "volume", "prune", "-f"])
    return {"output": stdout}


def docker_cleanup(
    action: str,
    keep_images: list = None,
    dry_run: bool = False,
    min_age_days: int = 1,
) -> dict:
    """Clean up Docker resources. Safe to call from any agent on schedule."""
    if keep_images is None:
        keep_images = list(_DEFAULT_KEEP)

    try:
        if action == "disk_usage":
            usage = _disk_usage_data()
            # Warn if space looks high
            raw, _, _ = _run(["docker", "system", "df"])
            return _wrap("ok", {"disk_usage": usage, "raw_summary": raw})

        elif action == "prune_images":
            data = _prune_images(keep_images, dry_run, min_age_days)
            return _wrap("ok", data)

        elif action == "prune_containers":
            data = _prune_containers(dry_run, min_age_days)
            return _wrap("ok", data)

        elif action == "prune_volumes":
            data = _prune_volumes(dry_run)
            return _wrap("ok", data)

        elif action == "prune_all":
            images = _prune_images(keep_images, dry_run, min_age_days)
            containers = _prune_containers(dry_run, min_age_days)
            volumes = _prune_volumes(dry_run)
            usage_after = _disk_usage_data()
            return _wrap("ok", {
                "images": images,
                "containers": containers,
                "volumes": volumes,
                "disk_usage_after": usage_after,
                "dry_run": dry_run,
            })

        else:
            return _wrap("error", {"message": f"Unknown action '{action}'."})

    except FileNotFoundError:
        return _wrap("error", {"message": "Docker is not installed or not in PATH."})
    except subprocess.TimeoutExpired:
        return _wrap("error", {"message": "Docker command timed out after 120s."})
    except Exception as exc:
        logger.exception("docker_cleanup error")
        return _wrap("error", {"message": str(exc)})
