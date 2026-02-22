"""
Executive Summary: Safe shell command executor with an allowlist of permitted command prefixes.
Only commands starting with an approved prefix (curl, wget, python3, python, git,
systemctl --user, journalctl, ps, top, df, free, uptime, cat, ls, find) are executed.
All others are rejected outright. Uses subprocess with shell=False and enforces a timeout.
Inputs: command (str), timeout (int, default 30)
Outputs: {"stdout": str, "stderr": str, "exit_code": int, "command": str}
MCP Tool Name: shell_exec
"""
import logging
import shlex
import subprocess
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "shell_exec",
    "description": (
        "Run a shell command on the local system and return stdout, stderr, and exit code. "
        "Only commands whose first token(s) match an approved allowlist are permitted. "
        "Allowed prefixes: curl, wget, python3, python, git, systemctl --user, "
        "journalctl, ps, top, df, free, uptime, cat, ls, find."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "The shell command to run. Must start with an approved prefix.",
            },
            "timeout": {
                "type": "integer",
                "description": "Timeout in seconds before the command is killed (default 30).",
                "default": 30,
            },
        },
        "required": ["command"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "stdout": {"type": "string"},
                    "stderr": {"type": "string"},
                    "exit_code": {"type": "integer"},
                    "command": {"type": "string"},
                },
            },
            "timestamp": {"type": "string"},
        },
        "required": ["status", "timestamp"],
    },
}

# Allowlist of permitted command prefixes.
# Each entry is a tuple of tokens that must match the START of the parsed command argv.
# Single-token entries match on argv[0]; two-token entries also check argv[1].
_ALLOWED_PREFIXES: list[tuple[str, ...]] = [
    ("curl",),
    ("wget",),
    ("python3",),
    ("python",),
    ("git",),
    ("systemctl", "--user"),  # systemctl --user only — no bare systemctl
    ("journalctl",),
    ("ps",),
    ("top",),
    ("df",),
    ("free",),
    ("uptime",),
    ("cat",),
    ("ls",),
    ("find",),
]

_MAX_TIMEOUT = 120  # Hard ceiling regardless of caller request


def _is_allowed(argv: list[str]) -> bool:
    """Return True if the parsed argv starts with an approved prefix.

    Args:
        argv: List of command tokens from shlex.split.

    Returns:
        True if a matching allowlist prefix is found, False otherwise.
    """
    for prefix in _ALLOWED_PREFIXES:
        n = len(prefix)
        if len(argv) >= n and tuple(argv[:n]) == prefix:
            return True
    return False


def shell_exec(command: str, timeout: int = 30) -> dict:
    """Execute an allowlisted shell command and return its output.

    The command is parsed with shlex.split (shell=False) to prevent shell
    injection. Only commands whose argv prefix matches the ALLOWED_PREFIXES
    list are executed; all others are rejected with status "error".

    Args:
        command: The shell command string to execute.
        timeout: Maximum seconds to wait before sending SIGKILL (capped at 120).

    Returns:
        Dict with keys:
            status (str): "ok" or "error".
            data (dict): stdout, stderr, exit_code, command — present on "ok".
            error (str): Human-readable rejection reason — present on "error".
            timestamp (str): ISO-8601 UTC timestamp.
    """
    ts = datetime.now(timezone.utc).isoformat()

    # --- Input validation ---
    if not command or not isinstance(command, str):
        return {"status": "error", "error": "command must be a non-empty string.", "timestamp": ts}

    command = command.strip()
    if not command:
        return {"status": "error", "error": "command must be a non-empty string.", "timestamp": ts}

    try:
        timeout = int(timeout)
    except (TypeError, ValueError):
        timeout = 30
    timeout = max(1, min(timeout, _MAX_TIMEOUT))

    # --- Parse ---
    try:
        argv = shlex.split(command)
    except ValueError as exc:
        return {"status": "error", "error": f"Failed to parse command: {exc}", "timestamp": ts}

    if not argv:
        return {"status": "error", "error": "command parsed to an empty argument list.", "timestamp": ts}

    # --- Allowlist check ---
    if not _is_allowed(argv):
        return {
            "status": "error",
            "error": (
                f"Command '{argv[0]}' is not on the approved allowlist. "
                "Permitted prefixes: curl, wget, python3, python, git, "
                "systemctl --user, journalctl, ps, top, df, free, uptime, cat, ls, find."
            ),
            "timestamp": ts,
        }

    # --- Execute ---
    try:
        result = subprocess.run(
            argv,
            shell=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "status": "ok",
            "data": {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode,
                "command": command,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "error": f"Command timed out after {timeout} seconds.",
            "data": {"command": command},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except FileNotFoundError:
        return {
            "status": "error",
            "error": f"Executable not found: '{argv[0]}'.",
            "data": {"command": command},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        logger.error("shell_exec error: %s", exc)
        return {
            "status": "error",
            "error": str(exc),
            "data": {"command": command},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
