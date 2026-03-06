"""
Executive Summary: Aggregate health status of all Snowdrop daemons, timers, and cron jobs into a single dashboard view.

Inputs: None
Outputs: A dictionary containing health status of daemons, timers, logs, and state files.
MCP Tool Name: daemon_health_dashboard
"""
import os
import time
from pathlib import Path
from datetime import datetime, timezone
import subprocess

TOOL_META = {
    "name": "daemon_health_dashboard",
    "description": "Aggregate health status of all Snowdrop daemons, timers, and cron jobs into a single dashboard view.",
    "inputSchema": {"type": "object", "properties": {}, "required": []},
}

_REPO_ROOT = Path(__file__).parent.parent.parent.resolve()

def _get_systemd_status(unit: str, is_timer: bool = False) -> dict:
    try:
        props_to_get = ["ActiveState", "SubState"]
        if is_timer:
            props_to_get.append("Result")
            
        result = subprocess.run(
            ["systemctl", "--user", "show", unit, f"--property={','.join(props_to_get)}"],
            capture_output=True, text=True, timeout=5
        )
        props = {}
        for line in result.stdout.strip().splitlines():
            if "=" in line:
                k, v = line.split("=", 1)
                props[k.strip()] = v.strip()
        return props
    except Exception as e:
        return {"error": str(e)}

def _check_freshness(items: list[tuple[str, int]]) -> dict:
    results = {}
    now = time.time()
    for rel_path, max_age_hours in items:
        p = _REPO_ROOT / rel_path
        if p.exists():
            age_hours = (now - os.path.getmtime(p)) / 3600
            results[rel_path] = "healthy" if age_hours <= max_age_hours else f"stale ({age_hours:.1f}h old)"
        else:
            results[rel_path] = "missing"
    return results

def daemon_health_dashboard() -> dict:
    """Aggregates health status of Snowdrop systems."""
    services = ["snowdrop-mcp.service", "openclaw-gateway.service", "snowdrop-chat.service"]
    timers = ["snowdrop-intel.timer", "snowdrop-integrity.timer", "snowdrop-recruiting.timer"]
    
    logs = [
        ("logs/cron/engagement_daemon.log", 1),
        ("logs/cron/gmail_monitor.log", 1),
        ("logs/cron/chat_daemon.log", 1),
    ]
    
    states = [
        ("state/gmail_state.json", 1),
        ("state/chat_state.json", 1),
        ("state/engagement/rate_limit.json", 1),
    ]
    
    dashboard = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "systemd_services": {s: _get_systemd_status(s) for s in services},
        "systemd_timers": {t: _get_systemd_status(t, is_timer=True) for t in timers},
        "cron_logs": _check_freshness(logs),
        "state_files": _check_freshness(states)
    }
    
    return {"status": "ok", "data": dashboard, "timestamp": dashboard["timestamp"]}
