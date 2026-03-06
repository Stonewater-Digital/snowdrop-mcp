"""
Executive Summary
-----------------
Manage Remote Daemon skill for Snowdrop. Abstracts raw SSH and systemctl 
commands for interacting with daemons on snowdrop-node.

Actions:
  status  - get health summary of a daemon
  restart - restart a daemon
  stop    - stop a daemon
  start   - start a daemon

Returns a clean JSON summary instead of raw systemctl outputs.
"""

import subprocess
import json
from datetime import datetime, timezone

TOOL_META = {
    "name": "manage_remote_daemon",
    "description": (
        "Manage remote systemd daemons on snowdrop-node via SSH. "
        "Abstracts systemctl commands to return clean JSON summaries "
        "instead of massive log dumps."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "daemon_name": {
                "type": "string",
                "description": "Name of the systemd service (e.g., 'snowdrop-recruiting').",
            },
            "action": {
                "type": "string",
                "enum": ["status", "restart", "start", "stop"],
                "description": "Action to perform on the daemon.",
            },
            "target_host": {
                "type": "string",
                "description": "SSH target host. Defaults to 'snowdrop-node'.",
            }
        },
        "required": ["daemon_name", "action"],
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

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def _wrap(status: str, data: dict) -> dict:
    return {"status": status, "data": data, "timestamp": _now_iso()}

def _run_ssh_command(host: str, cmd: str) -> subprocess.CompletedProcess:
    # Use BatchMode and ConnectTimeout to avoid hanging on prompt
    ssh_cmd = [
        "ssh",
        "-o", "BatchMode=yes",
        "-o", "ConnectTimeout=10",
        host,
        cmd
    ]
    return subprocess.run(ssh_cmd, capture_output=True, text=True)

def _parse_systemctl_status(output: str) -> dict:
    """Parse raw systemctl status output into a structured dictionary."""
    lines = output.splitlines()
    summary = {
        "active_state": "unknown",
        "sub_state": "unknown",
        "load_state": "unknown",
        "description": "",
        "recent_logs": []
    }
    
    logs_started = False
    
    for line in lines:
        line_stripped = line.strip()
        
        if line.startswith(" * ") or line.startswith("● "):
            summary["description"] = line[2:].strip()
            continue
            
        if "Loaded:" in line:
            parts = line.split("Loaded:", 1)[1].strip().split()
            if parts:
                summary["load_state"] = parts[0]
                
        if "Active:" in line:
            active_part = line.split("Active:", 1)[1].strip()
            # e.g. "active (running) since ..."
            parts = active_part.split()
            if parts:
                summary["active_state"] = parts[0]
                if len(parts) > 1 and parts[1].startswith("("):
                    summary["sub_state"] = parts[1].strip("()")
                    
        # Grab a few recent log lines
        if "CGroup:" in line:
            continue
            
        # Basic heuristic to capture recent logs
        if line_stripped and (":" in line_stripped[:20] or logs_started):
            # Not a robust date check, but typically logs have timestamps at start
            if not any(k in line for k in ["Loaded:", "Active:", "Docs:", "Main PID:", "Tasks:", "Memory:", "CPU:"]):
                summary["recent_logs"].append(line_stripped)
                logs_started = True

    # Limit logs to keep payload small
    summary["recent_logs"] = summary["recent_logs"][-10:]
    return summary

def manage_remote_daemon(
    daemon_name: str,
    action: str,
    target_host: str = "snowdrop-node"
) -> dict:
    """Manage a remote daemon via SSH and systemctl."""
    
    if action not in ["status", "restart", "start", "stop"]:
        return _wrap("error", {"message": f"Invalid action: {action}"})
        
    # Sanitize daemon name to prevent injection
    if not daemon_name.replace("-", "").replace("_", "").replace(".", "").isalnum():
        return _wrap("error", {"message": f"Invalid daemon_name: {daemon_name}"})
        
    try:
        if action == "status":
            cmd = f"systemctl status {daemon_name} --no-pager -n 10"
            result = _run_ssh_command(target_host, cmd)
            
            if result.returncode == 4:
                 return _wrap("error", {"message": f"Daemon '{daemon_name}' not found or no access."})
            
            # systemctl status returns 0 if active, 3 if inactive/failed.
            parsed_status = _parse_systemctl_status(result.stdout or result.stderr)
            return _wrap("ok", {
                "daemon": daemon_name,
                "host": target_host,
                "health": parsed_status,
                "exit_code": result.returncode
            })
            
        else:
            # For start/stop/restart, we need sudo if not running as root, 
            # assuming passwordless sudo is configured or running as root.
            cmd = f"sudo systemctl {action} {daemon_name}"
            result = _run_ssh_command(target_host, cmd)
            
            if result.returncode == 0:
                return _wrap("ok", {
                    "daemon": daemon_name,
                    "action": action,
                    "host": target_host,
                    "result": "success"
                })
            else:
                return _wrap("error", {
                    "message": f"Failed to {action} {daemon_name}",
                    "stderr": result.stderr.strip()[-200:], # keep it small
                    "exit_code": result.returncode
                })
                
    except Exception as exc:
        return _wrap("error", {"message": str(exc)})
