"""
Executive Summary: Normalizes identity access requests into provisioning steps with entitlement mapping and expiry checks.

Inputs: requests (list[dict]), role_matrix (dict[str, list[str]], optional), default_expiry_days (int, optional)
Outputs: status (str), data (instructions/summary), timestamp (str)
MCP Tool Name: identity_access_provisioner
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from skills.utils import (
    SkillTelemetryEmitter,
    get_iso_timestamp,
    logger,
    log_lesson as _shared_log_lesson,
)

TOOL_META: dict[str, Any] = {
    "name": "identity_access_provisioner",
    "description": "Generate provisioning instructions for identity requests with entitlements and expiry validation.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "requests": {
                "type": "array",
                "items": {"type": "object"},
                "description": "Requests with user, roles, system, justification, and requested_until fields.",
            },
            "role_matrix": {
                "type": "object",
                "description": "Mapping of role -> entitlements/groups to assign.",
            },
            "default_expiry_days": {
                "type": "integer",
                "default": 90,
                "description": "Fallback expiry window when not supplied on the request.",
            },
        },
        "required": ["requests"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["ok", "error"]},
            "data": {
                "type": "object",
                "properties": {
                    "instructions": {"type": "array", "items": {"type": "object"}},
                    "summary": {"type": "object"},
                },
            },
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def identity_access_provisioner(
    requests: list[dict[str, Any]],
    role_matrix: dict[str, list[str]] | None = None,
    default_expiry_days: int = 90,
) -> dict[str, Any]:
    """Convert identity requests into actionable provisioning instructions."""
    emitter = SkillTelemetryEmitter(
        "identity_access_provisioner",
        {"requests": len(requests or []), "default_expiry_days": default_expiry_days},
    )
    try:
        if not requests:
            raise ValueError("requests cannot be empty")
        if default_expiry_days <= 0:
            raise ValueError("default_expiry_days must be positive")

        entitlements = {role.lower(): values for role, values in (role_matrix or {}).items()}
        now = datetime.now(timezone.utc)
        instructions: list[dict[str, Any]] = []
        stats = {"high_risk": 0, "total": 0}

        for request in requests:
            user = str(request.get("user") or "unknown")
            roles = [str(role).lower() for role in (request.get("roles") or [])]
            system = str(request.get("system") or "okta")
            justification = request.get("justification") or "missing justification"
            requested_until = _parse_date(request.get("requested_until"))
            expiry = requested_until or (now + timedelta(days=default_expiry_days))
            days_valid = (expiry - now).days

            groups = sorted({group for role in roles for group in entitlements.get(role, [])})
            risk_level = "high" if any("prod" in role or "admin" in role for role in roles) else "standard"
            if risk_level == "high":
                stats["high_risk"] += 1

            instruction = {
                "user": user,
                "system": system,
                "entitlements": groups,
                "roles": roles,
                "expiry": expiry.isoformat(),
                "days_valid": days_valid,
                "risk_level": risk_level,
                "action": "escalate" if risk_level == "high" else "provision",
                "justification": justification,
            }
            instructions.append(instruction)
            stats["total"] += 1

        summary = {
            "requests": stats["total"],
            "high_risk_requests": stats["high_risk"],
            "systems": sorted({item["system"] for item in instructions}),
        }
        emitter.record("ok", summary)
        return {"status": "ok", "data": {"instructions": instructions, "summary": summary}, "timestamp": get_iso_timestamp()}
    except Exception as exc:  # noqa: BLE001
        logger.error(f"identity_access_provisioner failed: {exc}")
        _log_lesson("identity_access_provisioner", str(exc))
        emitter.record("error", {"error": str(exc)})
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": get_iso_timestamp()}


def _parse_date(raw: Any) -> datetime | None:
    """Parse ISO8601 dates to timezone-aware datetime."""
    if not raw:
        return None
    try:
        value = str(raw).replace("Z", "+00:00")
        parsed = datetime.fromisoformat(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed
    except ValueError:
        return None


def _log_lesson(skill_name: str, error: str) -> None:
    """Proxy shared lesson logger."""
    _shared_log_lesson(skill_name, error)
