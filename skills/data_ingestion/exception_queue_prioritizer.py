"""
Executive Summary: Ranks reconciliation exceptions using severity, staleness, and capital at risk to focus Thunder's pods.

Inputs: exceptions (list[dict]), owner_map (dict[str, str], optional), max_items (int, optional)
Outputs: status (str), data (queue/summary), timestamp (str)
MCP Tool Name: exception_queue_prioritizer
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from skills.utils import (
    SkillTelemetryEmitter,
    get_iso_timestamp,
    logger,
    log_lesson as _shared_log_lesson,
)

SEVERITY_WEIGHTS: dict[str, int] = {
    "critical": 4,
    "high": 3,
    "medium": 2,
    "low": 1,
}

TOOL_META: dict[str, Any] = {
    "name": "exception_queue_prioritizer",
    "description": "Prioritize reconciliation exceptions by severity, financial exposure, and SLA breach risk.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "exceptions": {
                "type": "array",
                "items": {"type": "object"},
                "description": "Exception payloads with fields: id, severity, detected_at, type, attempts, amount_at_risk.",
            },
            "owner_map": {
                "type": "object",
                "description": "Keyword -> owner/team overrides for routing.",
            },
            "max_items": {
                "type": "integer",
                "default": 20,
                "description": "Maximum prioritized exceptions to return.",
            },
        },
        "required": ["exceptions"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["ok", "error"]},
            "data": {
                "type": "object",
                "properties": {
                    "queue": {"type": "array", "items": {"type": "object"}},
                    "summary": {"type": "object"},
                },
            },
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def exception_queue_prioritizer(
    exceptions: list[dict[str, Any]],
    owner_map: dict[str, str] | None = None,
    max_items: int = 20,
) -> dict[str, Any]:
    """Rank exceptions and route them to the best owner.

    Args:
        exceptions: Raw exception payloads.
        owner_map: Keyword heuristics for routing to pods/owners.
        max_items: Maximum number of prioritized entries to emit.

    Returns:
        Snowdrop response dict with prioritized queue items and summary stats.

    Raises:
        ValueError: If inputs are invalid.
    """
    emitter = SkillTelemetryEmitter(
        "exception_queue_prioritizer",
        {"exceptions": len(exceptions or []), "max_items": max_items},
    )
    try:
        if not isinstance(exceptions, list):
            raise ValueError("exceptions must be a list of dicts")
        if max_items <= 0:
            raise ValueError("max_items must be positive")

        normalized_owner_map = _normalize_owner_map(owner_map)
        now = datetime.now(timezone.utc)
        ranked: list[dict[str, Any]] = []

        for payload in exceptions:
            if not isinstance(payload, dict):
                continue
            severity = str(payload.get("severity", "low")).lower()
            severity_weight = SEVERITY_WEIGHTS.get(severity, 1)
            detected_at = _parse_timestamp(payload.get("detected_at"))
            staleness_minutes = (
                (now - detected_at).total_seconds() / 60 if detected_at else 0.0
            )
            attempts = max(int(payload.get("attempts") or 0), 0)
            amount_at_risk = float(payload.get("amount_at_risk") or 0.0)
            priority_score = (
                severity_weight * 100
                + attempts * 15
                + staleness_minutes
                + amount_at_risk / 50_000
            )
            owner = _route_owner(payload, normalized_owner_map)
            ranked.append(
                {
                    "id": payload.get("id"),
                    "type": payload.get("type"),
                    "severity": severity,
                    "owner": owner,
                    "staleness_minutes": round(staleness_minutes, 2),
                    "attempts": attempts,
                    "amount_at_risk": amount_at_risk,
                    "priority_score": round(priority_score, 2),
                    "next_action": _next_action(severity, attempts),
                }
            )

        sorted_queue = sorted(ranked, key=lambda item: item["priority_score"], reverse=True)[
            :max_items
        ]
        summary = {
            "total_exceptions": len(ranked),
            "returned": len(sorted_queue),
            "critical": sum(1 for item in ranked if item["severity"] == "critical"),
        }
        emitter.record("ok", {"returned": len(sorted_queue), "critical": summary["critical"]})
        data = {"queue": sorted_queue, "summary": summary}
        return {"status": "ok", "data": data, "timestamp": get_iso_timestamp()}
    except Exception as exc:  # noqa: BLE001
        logger.error(f"exception_queue_prioritizer failed: {exc}")
        _log_lesson("exception_queue_prioritizer", str(exc))
        emitter.record("error", {"error": str(exc)})
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": get_iso_timestamp()}


def _parse_timestamp(raw: Any) -> datetime | None:
    """Parse timestamps to UTC."""
    if raw is None:
        return None
    try:
        value = str(raw).replace("Z", "+00:00")
        ts = datetime.fromisoformat(value)
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        return ts.astimezone(timezone.utc)
    except (ValueError, TypeError):
        return None


def _normalize_owner_map(owner_map: dict[str, str] | None) -> dict[str, str]:
    """Lower-case keys and filter invalid entries."""
    if not owner_map:
        return {}
    normalized: dict[str, str] = {}
    for key, value in owner_map.items():
        if isinstance(key, str) and isinstance(value, str):
            normalized[key.lower()] = value
    return normalized


def _route_owner(payload: dict[str, Any], owner_map: dict[str, str]) -> str:
    """Return recommended owner based on type + hints."""
    hint = str(payload.get("owner_hint", "")).lower()
    exception_type = str(payload.get("type", "")).lower()
    text = f"{hint} {exception_type}"
    for keyword, owner in owner_map.items():
        if keyword in text:
            return owner
    return hint or "ops_triage"


def _next_action(severity: str, attempts: int) -> str:
    """Return human-readable recommendation."""
    if severity == "critical":
        return "Escalate to Thunder immediately"
    if attempts >= 3:
        return "Call administrator; auto retries exhausted"
    if severity == "high":
        return "Assign to fund_ops within 15 minutes"
    return "Queue for batch remediation"


def _log_lesson(skill_name: str, error: str) -> None:
    """Proxy shared logger."""
    _shared_log_lesson(skill_name, error)
