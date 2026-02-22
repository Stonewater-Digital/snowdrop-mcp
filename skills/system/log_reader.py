"""
Executive Summary: Log reader skill that retrieves recent lines from either a journalctl
user-service stream or a local log file. Supports line-count limiting and journalctl
--since filtering. Handles missing files and subprocess errors gracefully.
Inputs: source (str), service_name (str, optional), file_path (str, optional),
        lines (int, default 50), since (str, optional)
Outputs: {"lines": [str], "count": int, "source": str}
MCP Tool Name: log_reader
"""
import logging
import os
import subprocess
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "log_reader",
    "description": (
        "Read recent log lines from a journalctl user-service or a local log file. "
        "For journalctl, provide service_name (e.g. 'snowdrop-mcp'). "
        "For file, provide file_path (absolute path). "
        "Optionally specify lines (default 50) and, for journalctl, a since expression "
        "such as '1 hour ago' or 'today'."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "source": {
                "type": "string",
                "description": "Log source: 'journalctl' or 'file'.",
                "enum": ["journalctl", "file"],
            },
            "service_name": {
                "type": "string",
                "description": "Systemd user service name (required when source='journalctl').",
            },
            "file_path": {
                "type": "string",
                "description": "Absolute path to log file (required when source='file').",
            },
            "lines": {
                "type": "integer",
                "description": "Number of recent lines to return (default 50, max 2000).",
                "default": 50,
            },
            "since": {
                "type": "string",
                "description": (
                    "journalctl --since expression, e.g. '1 hour ago' or 'today'. "
                    "Only used when source='journalctl'."
                ),
            },
        },
        "required": ["source"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "lines": {"type": "array", "items": {"type": "string"}},
                    "count": {"type": "integer"},
                    "source": {"type": "string"},
                },
            },
            "timestamp": {"type": "string"},
        },
        "required": ["status", "timestamp"],
    },
}

_MAX_LINES = 2000


def _read_journalctl(service_name: str, lines: int, since: str | None) -> list[str]:
    """Retrieve log lines for a systemd user service via journalctl.

    Args:
        service_name: The systemd user service name.
        lines: Maximum number of lines to fetch.
        since: Optional --since time expression (e.g. '1 hour ago').

    Returns:
        List of log line strings (may be empty).

    Raises:
        RuntimeError: If journalctl exits with a non-zero code.
    """
    cmd = [
        "journalctl",
        "--user",
        "-u", service_name,
        "-n", str(lines),
        "--no-pager",
    ]
    if since:
        cmd += ["--since", since]

    result = subprocess.run(
        cmd,
        shell=False,
        capture_output=True,
        text=True,
        timeout=15,
    )
    if result.returncode not in (0, 1):  # 1 = no entries found, still valid
        raise RuntimeError(
            f"journalctl exited {result.returncode}: {result.stderr.strip()}"
        )
    raw = result.stdout.strip()
    return raw.splitlines() if raw else []


def _read_file(file_path: str, lines: int) -> list[str]:
    """Read the last N lines from a log file.

    Args:
        file_path: Absolute path to the log file.
        lines: Maximum number of lines to return (from the end of the file).

    Returns:
        List of line strings.

    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If the file cannot be read.
    """
    with open(file_path, "r", encoding="utf-8", errors="replace") as fh:
        all_lines = fh.readlines()
    return [l.rstrip("\n") for l in all_lines[-lines:]]


def log_reader(
    source: str,
    service_name: str = "",
    file_path: str = "",
    lines: int = 50,
    since: str = "",
) -> dict:
    """Read recent log lines from journalctl or a local file.

    Args:
        source: "journalctl" or "file".
        service_name: Systemd user service name (required for journalctl).
        file_path: Absolute path to log file (required for file).
        lines: Number of recent lines to return (default 50, capped at 2000).
        since: journalctl --since expression, e.g. "1 hour ago" (journalctl only).

    Returns:
        Dict with keys:
            status (str): "ok" or "error".
            data (dict): lines (list[str]), count (int), source (str).
            error (str): Error message if status is "error".
            timestamp (str): ISO-8601 UTC timestamp.
    """
    ts = datetime.now(timezone.utc).isoformat()

    # --- Input validation ---
    if source not in ("journalctl", "file"):
        return {
            "status": "error",
            "error": "source must be 'journalctl' or 'file'.",
            "timestamp": ts,
        }

    try:
        lines = int(lines)
    except (TypeError, ValueError):
        lines = 50
    lines = max(1, min(lines, _MAX_LINES))

    since_val: str | None = since.strip() if since and isinstance(since, str) else None

    try:
        if source == "journalctl":
            if not service_name or not isinstance(service_name, str):
                return {
                    "status": "error",
                    "error": "service_name is required when source='journalctl'.",
                    "timestamp": ts,
                }
            log_lines = _read_journalctl(service_name.strip(), lines, since_val)
            source_label = f"journalctl::{service_name.strip()}"

        else:  # file
            if not file_path or not isinstance(file_path, str):
                return {
                    "status": "error",
                    "error": "file_path is required when source='file'.",
                    "timestamp": ts,
                }
            fp = file_path.strip()
            if not os.path.isabs(fp):
                return {
                    "status": "error",
                    "error": f"file_path must be an absolute path, got: '{fp}'.",
                    "timestamp": ts,
                }
            log_lines = _read_file(fp, lines)
            source_label = f"file::{fp}"

        return {
            "status": "ok",
            "data": {
                "lines": log_lines,
                "count": len(log_lines),
                "source": source_label,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except FileNotFoundError as exc:
        return {
            "status": "error",
            "error": f"File not found: {exc}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except PermissionError as exc:
        return {
            "status": "error",
            "error": f"Permission denied: {exc}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "error": "journalctl timed out after 15 seconds.",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except RuntimeError as exc:
        return {
            "status": "error",
            "error": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        logger.error("log_reader error: %s", exc)
        return {
            "status": "error",
            "error": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
