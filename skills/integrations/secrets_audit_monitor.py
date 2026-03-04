"""
Executive Summary: Audits required integration secrets and reports coverage without exposing values.

Inputs: required_secrets (list[str]), env_source (dict[str, str], optional)
Outputs: status (str), data (results/summary), timestamp (str)
MCP Tool Name: secrets_audit_monitor
"""
from __future__ import annotations

import os
from typing import Any

from skills.utils import (
    SkillTelemetryEmitter,
    get_iso_timestamp,
    logger,
    log_lesson as _shared_log_lesson,
)

TOOL_META: dict[str, Any] = {
    "name": "secrets_audit_monitor",
    "description": "Checks whether required secrets are present in the environment and flags missing/empty variables.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "required_secrets": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Names of env vars that must be set.",
            },
            "env_source": {
                "type": "object",
                "description": "Optional map of env vars (defaults to os.environ).",
            },
        },
        "required": ["required_secrets"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["ok", "error"]},
            "data": {
                "type": "object",
                "properties": {
                    "results": {"type": "array", "items": {"type": "object"}},
                    "summary": {"type": "object"},
                },
            },
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def secrets_audit_monitor(
    required_secrets: list[str],
    env_source: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Verify required secrets are available for integrations."""
    emitter = SkillTelemetryEmitter(
        "secrets_audit_monitor",
        {"required_secrets": len(required_secrets or [])},
    )
    try:
        if not required_secrets:
            raise ValueError("required_secrets cannot be empty")

        env = env_source or dict(os.environ)
        results: list[dict[str, Any]] = []
        status_counts = {"present": 0, "missing": 0, "empty": 0}

        for secret in required_secrets:
            value = env.get(secret)
            if value is None:
                state = "missing"
                status_counts["missing"] += 1
            elif not str(value).strip():
                state = "empty"
                status_counts["empty"] += 1
            else:
                state = "present"
                status_counts["present"] += 1
            results.append(
                {
                    "secret": secret,
                    "status": state,
                }
            )

        summary = {
            "total": len(required_secrets),
            **status_counts,
        }
        emitter.record("ok", summary)
        return {"status": "ok", "data": {"results": results, "summary": summary}, "timestamp": get_iso_timestamp()}
    except Exception as exc:  # noqa: BLE001
        logger.error(f"secrets_audit_monitor failed: {exc}")
        _log_lesson("secrets_audit_monitor", str(exc))
        emitter.record("error", {"error": str(exc)})
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": get_iso_timestamp()}


def _log_lesson(skill_name: str, error: str) -> None:
    """Proxy shared lesson logger."""
    _shared_log_lesson(skill_name, error)
