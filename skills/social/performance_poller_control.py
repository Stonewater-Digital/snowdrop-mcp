"""
Performance Poller Control skill — Snowdrop's interface to the A2A Performance Poller subagent.

The Performance Poller runs every 2 hours on snowdrop-node via cron, polling Moltbook
for upvotes and comments on all logged posts. This skill lets Snowdrop observe, trigger,
and read logs from the poller without waiting for the next cron tick.

A2A agent card: https://snowdrop-mcp.fly.dev/.well-known/agent-performance-poller.json
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

TOOL_META = {
    "name": "performance_poller_control",
    "description": (
        "Observe, trigger, or read the status of the Snowdrop Performance Poller subagent (A2A protocol). "
        "Actions: 'status' (last run time, posts polled, errors), 'trigger' (run poller immediately via subprocess), "
        "'read_card' (return the A2A agent card JSON), 'read_log' (last N lines of poller log). "
        "The poller normally runs every 2h via cron but can be triggered on-demand."
    ),
}

AGENT_ID = "performance-poller/1.0"
AGENT_CARD_URL = "https://snowdrop-mcp.fly.dev/.well-known/agent-performance-poller.json"

# Paths — relative to the snowdrop-mcp repo root
_REPO_ROOT = Path(__file__).parent.parent.parent
_STATE_FILE = _REPO_ROOT / "state" / "poller_state.json"
_POLLER_SCRIPT = _REPO_ROOT / "scripts" / "performance_poller.py"
_AGENT_CARD_FILE = _REPO_ROOT / ".well-known" / "agent-performance-poller.json"
_LOG_FILE = Path("/tmp/performance_poller.log")


def performance_poller_control(action: str, limit: int = 50) -> dict:
    """
    Observe and control the Performance Poller subagent.

    Args:
        action: One of 'status' | 'trigger' | 'read_card' | 'read_log'
        limit: For 'read_log' — number of recent log lines to return (default 50)
    """
    ts = datetime.now(timezone.utc).isoformat()

    try:
        if action == "status":
            return _status(ts)
        elif action == "trigger":
            return _trigger(ts)
        elif action == "read_card":
            return _read_card(ts)
        elif action == "read_log":
            return _read_log(ts, limit)
        else:
            return {
                "status": "error",
                "data": {"message": f"Unknown action: {action}. Use: status|trigger|read_card|read_log"},
                "timestamp": ts,
            }
    except Exception as e:
        return {
            "status": "error",
            "data": {"message": str(e)},
            "timestamp": ts,
        }


def _status(ts: str) -> dict:
    """Return A2A-structured status of the poller."""
    state = {}
    if _STATE_FILE.exists():
        try:
            state = json.loads(_STATE_FILE.read_text())
        except Exception:
            state = {}

    # Check if poller process is currently running
    poller_running = False
    try:
        result = subprocess.run(
            ["pgrep", "-f", "performance_poller.py"],
            capture_output=True, text=True, timeout=5
        )
        poller_running = result.returncode == 0
    except Exception:
        pass

    return {
        "status": "ok",
        "data": {
            "agent_id": AGENT_ID,
            "agent_card_url": AGENT_CARD_URL,
            "last_run": state.get("last_run", "never"),
            "last_run_id": state.get("last_run_id", ""),
            "posts_polled_last_run": state.get("posts_polled_last_run", 0),
            "run_count": state.get("run_count", 0),
            "total_posts_polled": state.get("total_posts_polled", 0),
            "state": "running" if poller_running else "idle",
            "errors_last_run": state.get("errors_last_run", []),
            "state_file": str(_STATE_FILE),
            "log_file": str(_LOG_FILE),
        },
        "timestamp": ts,
    }


def _trigger(ts: str) -> dict:
    """Launch poller as non-blocking subprocess."""
    if not _POLLER_SCRIPT.exists():
        return {
            "status": "error",
            "data": {"message": f"Poller script not found: {_POLLER_SCRIPT}"},
            "timestamp": ts,
        }

    try:
        python = sys.executable
        proc = subprocess.Popen(
            [python, str(_POLLER_SCRIPT)],
            stdout=open(_LOG_FILE, "a"),
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        return {
            "status": "ok",
            "data": {
                "triggered": True,
                "pid": proc.pid,
                "script": str(_POLLER_SCRIPT),
                "log_file": str(_LOG_FILE),
                "note": "Poller running in background. Use action='read_log' to monitor progress.",
            },
            "timestamp": ts,
        }
    except Exception as e:
        return {
            "status": "error",
            "data": {"message": f"Failed to trigger poller: {e}"},
            "timestamp": ts,
        }


def _read_card(ts: str) -> dict:
    """Return the A2A agent card JSON."""
    if not _AGENT_CARD_FILE.exists():
        return {
            "status": "error",
            "data": {"message": f"Agent card not found at {_AGENT_CARD_FILE}"},
            "timestamp": ts,
        }
    try:
        card = json.loads(_AGENT_CARD_FILE.read_text())
        return {
            "status": "ok",
            "data": {"agent_card": card, "source": str(_AGENT_CARD_FILE)},
            "timestamp": ts,
        }
    except Exception as e:
        return {
            "status": "error",
            "data": {"message": str(e)},
            "timestamp": ts,
        }


def _read_log(ts: str, limit: int) -> dict:
    """Return the last N lines from the poller log."""
    if not _LOG_FILE.exists():
        return {
            "status": "ok",
            "data": {"lines": [], "note": "Log file does not exist yet — poller has not run."},
            "timestamp": ts,
        }

    lines = _LOG_FILE.read_text(errors="replace").splitlines()
    recent = lines[-limit:] if len(lines) > limit else lines

    # Parse JSON lines where possible for structured output
    parsed = []
    for line in recent:
        line = line.strip()
        if not line:
            continue
        try:
            parsed.append(json.loads(line))
        except Exception:
            parsed.append({"raw": line})

    return {
        "status": "ok",
        "data": {
            "lines": parsed,
            "total_lines": len(lines),
            "showing": len(parsed),
            "log_file": str(_LOG_FILE),
        },
        "timestamp": ts,
    }
