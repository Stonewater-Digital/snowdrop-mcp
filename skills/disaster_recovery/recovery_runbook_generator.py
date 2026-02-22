"""Generate disaster recovery runbooks."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "recovery_runbook_generator",
    "description": "Outputs a step-by-step recovery plan tailored to the failure type.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "failure_type": {
                "type": "string",
                "enum": ["data_loss", "api_compromise", "key_rotation", "full_rebuild"],
            },
            "available_backups": {"type": "array", "items": {"type": "object"}},
            "system_state": {"type": "object"},
        },
        "required": ["failure_type", "available_backups", "system_state"],
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


def recovery_runbook_generator(
    failure_type: str,
    available_backups: list[dict[str, Any]],
    system_state: dict[str, Any],
    **_: Any,
) -> dict[str, Any]:
    """Return recovery steps referencing available backups."""
    try:
        steps = _base_steps(failure_type)
        verified_backup = next((b for b in available_backups if b.get("verified")), None)
        for idx, step in enumerate(steps, start=1):
            step["step"] = idx
            step["requires_thunder"] = step.get("requires_thunder", False)
        if verified_backup:
            steps.insert(
                1,
                {
                    "step": 1,
                    "action": f"Mount verified backup from {verified_backup.get('location')}",
                    "command": "aws s3 cp ...",
                    "requires_thunder": False,
                    "estimated_minutes": 15,
                },
            )
            for idx, step in enumerate(steps, start=1):
                step["step"] = idx
        data = {
            "failure_type": failure_type,
            "steps": steps,
            "system_state": system_state,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("recovery_runbook_generator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _base_steps(failure_type: str) -> list[dict[str, Any]]:
    mapping = {
        "data_loss": [
            {
                "action": "Quarantine affected systems",
                "command": "kubectl cordon ledger-nodes",
                "requires_thunder": True,
                "estimated_minutes": 5,
            },
            {
                "action": "Restore database snapshot",
                "command": "psql < snapshot.sql",
                "requires_thunder": True,
                "estimated_minutes": 45,
            },
        ],
        "api_compromise": [
            {
                "action": "Rotate API keys",
                "command": None,
                "requires_thunder": True,
                "estimated_minutes": 20,
            },
            {
                "action": "Deploy firewall rules",
                "command": "terraform apply firewall.tfplan",
                "requires_thunder": False,
                "estimated_minutes": 30,
            },
        ],
        "key_rotation": [
            {
                "action": "Invalidate old keys",
                "command": None,
                "requires_thunder": True,
                "estimated_minutes": 15,
            },
            {
                "action": "Distribute new keys via KMS",
                "command": None,
                "requires_thunder": True,
                "estimated_minutes": 25,
            },
        ],
        "full_rebuild": [
            {
                "action": "Provision clean infrastructure",
                "command": "terraform apply",
                "requires_thunder": True,
                "estimated_minutes": 60,
            },
            {
                "action": "Redeploy services",
                "command": "ansible-playbook deploy.yaml",
                "requires_thunder": False,
                "estimated_minutes": 90,
            },
        ],
    }
    return mapping.get(failure_type, []).copy()


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
