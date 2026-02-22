"""Liveness and readiness heartbeat for Snowdrop."""
from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "heartbeat",
    "description": (
        "Checks Ghost Ledger readiness, required API keys, and reconciliation freshness before"
        " writing HEARTBEAT.md with the current timestamp."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "required_keys": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Additional API key env vars to verify.",
            },
            "last_reconciliation_path": {
                "type": "string",
                "description": "File containing the last reconciliation ISO timestamp.",
                "default": "logs/last_reconciliation.txt",
            },
        },
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "data": {"type": "object"},
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def heartbeat(
    required_keys: list[str] | None = None,
    last_reconciliation_path: str = "logs/last_reconciliation.txt",
    **_: Any,
) -> dict[str, Any]:
    """Perform a liveness pulse and document it in HEARTBEAT.md.

    Args:
        required_keys: Optional list of env vars to check in addition to the baseline ones.
        last_reconciliation_path: Path to a file containing the last reconciliation timestamp.

    Returns:
        Envelope with health diagnostics and the latest heartbeat timestamp.
    """

    try:
        now = datetime.now(timezone.utc)
        ghost_ledger_reachable = Path("skills/ghost_ledger.py").exists()
        baseline_keys = ["MERCURY_API_TOKEN", "KRAKEN_API_KEY", "DATABASE_URL"]
        keys_to_check = sorted(set(baseline_keys + (required_keys or [])))
        missing_keys = [env for env in keys_to_check if not os.getenv(env)]

        last_reconciliation_status: dict[str, Any] = {
            "path": last_reconciliation_path,
            "age_hours": None,
            "status": "missing",
            "timestamp": None,
        }

        reconciliation_file = Path(last_reconciliation_path)
        if reconciliation_file.exists():
            content = reconciliation_file.read_text(encoding="utf-8").strip()
            if content:
                try:
                    recon_ts = datetime.fromisoformat(content)
                    age_hours = (now - recon_ts).total_seconds() / 3600
                    last_reconciliation_status = {
                        "path": last_reconciliation_path,
                        "age_hours": round(age_hours, 2),
                        "status": "fresh" if age_hours <= 24 else "stale",
                        "timestamp": recon_ts.isoformat(),
                    }
                except ValueError:
                    last_reconciliation_status = {
                        "path": last_reconciliation_path,
                        "age_hours": None,
                        "status": "parse_error",
                        "timestamp": content,
                    }

        heartbeat_lines = [
            "# Snowdrop Heartbeat",
            f"- Timestamp: {now.isoformat()}",
            f"- Ghost Ledger Reachable: {ghost_ledger_reachable}",
            f"- Missing Keys: {', '.join(missing_keys) if missing_keys else 'None'}",
            (
                "- Reconciliation Status: "
                f"{last_reconciliation_status['status']}"
            ),
        ]
        Path("HEARTBEAT.md").write_text("\n".join(heartbeat_lines) + "\n", encoding="utf-8")

        health_report = {
            "ghost_ledger": ghost_ledger_reachable,
            "api_keys": {
                "checked": keys_to_check,
                "missing": missing_keys,
            },
            "last_reconciliation": last_reconciliation_status,
        }

        return {
            "status": "success",
            "data": health_report,
            "timestamp": now.isoformat(),
        }
    except Exception as exc:
        _log_lesson("heartbeat", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    """Append a Ralph Wiggum lesson entry."""
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
