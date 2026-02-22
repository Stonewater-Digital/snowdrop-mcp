"""
Executive Summary: Systemd user service status checker. Queries `systemctl --user show`
for detailed property key/value output and `systemctl --user is-active` for a simple
active/inactive boolean. Returns ActiveState, SubState, LoadState, Description, and
the timestamp of the last activation.
Inputs: service_name (str)
Outputs: {"active": bool, "status": str, "sub_state": str, "load_state": str,
          "description": str, "since": str}
MCP Tool Name: service_status
"""
import logging
import subprocess
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "service_status",
    "description": (
        "Check the status of a systemd user service. "
        "Returns active state, sub-state, load state, description, and last activation timestamp. "
        "Example service names: 'snowdrop-mcp', 'openclaw-gateway'."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "service_name": {
                "type": "string",
                "description": "Systemd user service name, e.g. 'snowdrop-mcp'.",
            },
        },
        "required": ["service_name"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "active": {"type": "boolean"},
                    "status": {"type": "string"},
                    "sub_state": {"type": "string"},
                    "load_state": {"type": "string"},
                    "description": {"type": "string"},
                    "since": {"type": "string"},
                },
            },
            "timestamp": {"type": "string"},
        },
        "required": ["status", "timestamp"],
    },
}

# Properties we care about from `systemctl --user show`
_WANTED_PROPS = (
    "ActiveState",
    "SubState",
    "LoadState",
    "Description",
    "ActiveEnterTimestamp",
)


def _parse_show_output(raw: str) -> dict[str, str]:
    """Parse key=value lines from `systemctl --user show` output.

    Args:
        raw: Full stdout string from systemctl show.

    Returns:
        Dict mapping property names to their string values.
    """
    props: dict[str, str] = {}
    for line in raw.splitlines():
        if "=" in line:
            key, _, value = line.partition("=")
            props[key.strip()] = value.strip()
    return props


def _run(argv: list[str], timeout: int = 10) -> tuple[str, str, int]:
    """Run a subprocess and return (stdout, stderr, returncode).

    Args:
        argv: Command and arguments list.
        timeout: Seconds before SIGKILL.

    Returns:
        Tuple of (stdout text, stderr text, return code).
    """
    result = subprocess.run(
        argv,
        shell=False,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return result.stdout, result.stderr, result.returncode


def service_status(service_name: str) -> dict:
    """Query the status of a systemd user service.

    Runs two commands:
    1. ``systemctl --user show <service_name> --no-pager`` — parses key=value properties.
    2. ``systemctl --user is-active <service_name>`` — determines boolean active flag.

    Args:
        service_name: Systemd user service name (e.g. "snowdrop-mcp").

    Returns:
        Dict with keys:
            status (str): "ok" or "error".
            data (dict):
                active (bool): True if the service is currently active/running.
                status (str): ActiveState value (e.g. "active", "inactive", "failed").
                sub_state (str): SubState value (e.g. "running", "dead", "exited").
                load_state (str): LoadState value (e.g. "loaded", "not-found").
                description (str): Human-readable service description.
                since (str): Timestamp of last activation (ActiveEnterTimestamp).
            error (str): Error message if status is "error".
            timestamp (str): ISO-8601 UTC timestamp.
    """
    ts = datetime.now(timezone.utc).isoformat()

    # --- Input validation ---
    if not service_name or not isinstance(service_name, str):
        return {
            "status": "error",
            "error": "service_name must be a non-empty string.",
            "timestamp": ts,
        }
    service_name = service_name.strip()
    if not service_name:
        return {
            "status": "error",
            "error": "service_name must be a non-empty string.",
            "timestamp": ts,
        }

    try:
        # 1. Detailed properties
        show_stdout, show_stderr, show_rc = _run(
            ["systemctl", "--user", "show", service_name, "--no-pager"]
        )
        props = _parse_show_output(show_stdout)

        # 2. Simple active check
        is_active_stdout, _, is_active_rc = _run(
            ["systemctl", "--user", "is-active", service_name]
        )
        # is-active returns "active" on stdout if running; exit 0 = active
        active_flag = is_active_rc == 0 or is_active_stdout.strip() == "active"

        active_state = props.get("ActiveState", "unknown")
        sub_state = props.get("SubState", "unknown")
        load_state = props.get("LoadState", "unknown")
        description = props.get("Description", "")
        since = props.get("ActiveEnterTimestamp", "")

        # If LoadState is "not-found", the service doesn't exist
        if load_state == "not-found":
            return {
                "status": "error",
                "error": f"Service '{service_name}' not found in systemd user scope.",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        return {
            "status": "ok",
            "data": {
                "active": active_flag,
                "status": active_state,
                "sub_state": sub_state,
                "load_state": load_state,
                "description": description,
                "since": since,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "error": "systemctl timed out.",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except FileNotFoundError:
        return {
            "status": "error",
            "error": "systemctl executable not found — is this a systemd system?",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        logger.error("service_status error: %s", exc)
        return {
            "status": "error",
            "error": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
