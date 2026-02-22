"""Track and update Snowdrop operational incidents with SLA awareness."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "incident_tracker",
    "description": "Opens, updates, or lists incidents with SLA tracking and JSONL logging.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["open", "update", "list"],
                "description": "Operation to perform on the incident ledger.",
            },
            "incident": {
                "type": "object",
                "description": "Incident payload for open/update operations.",
            },
        },
        "required": ["operation"],
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


_SLA_MINUTES = {"sev1": 15, "sev2": 60, "sev3": 240, "sev4": 1440}
_LOG_PATH = Path("logs/incidents.jsonl")


def incident_tracker(
    operation: str,
    incident: dict[str, Any] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Manage incident lifecycle operations."""
    try:
        operation = operation.lower()
        incidents = _read_incidents()
        if operation == "list":
            enriched = [_enrich_incident(rec) for rec in incidents]
            data = {"incidents": enriched}
        elif operation in {"open", "update"}:
            if incident is None:
                raise ValueError("incident payload required for open/update")
            if "incident_id" not in incident:
                raise ValueError("incident_id required in incident payload")
            record = _prepare_record(operation, incident, incidents)
            _append_incident(record)
            data = _enrich_incident(record)
        else:
            raise ValueError("operation must be open, update, or list")

        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("incident_tracker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _read_incidents() -> list[dict[str, Any]]:
    if not _LOG_PATH.exists():
        return []
    records: list[dict[str, Any]] = []
    with _LOG_PATH.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return records


def _append_incident(record: dict[str, Any]) -> None:
    _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record) + "\n")


def _prepare_record(
    operation: str,
    incoming: dict[str, Any],
    history: list[dict[str, Any]],
) -> dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat()
    severity = str(incoming.get("severity", "sev3")).lower()
    base: dict[str, Any] = {}
    if operation == "update":
        for record in reversed(history):
            if record.get("incident_id") == incoming["incident_id"]:
                base = record.copy()
                break
        if not base:
            raise ValueError("Cannot update unknown incident_id")
    else:
        required_fields = [
            "severity",
            "title",
            "description",
            "affected_systems",
            "opened_at",
            "status",
        ]
        missing = [field for field in required_fields if field not in incoming]
        if missing:
            raise ValueError(f"Missing incident fields: {', '.join(missing)}")
        base = {
            "incident_id": incoming["incident_id"],
            "opened_at": incoming["opened_at"],
        }

    merged = {**base, **incoming, "severity": severity, "last_updated": now}
    return merged


def _enrich_incident(record: dict[str, Any]) -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    opened_at = _parse_datetime(record.get("opened_at"))
    time_open_minutes = max((now - opened_at).total_seconds() / 60, 0)
    sla_minutes = _SLA_MINUTES.get(record.get("severity", "sev3"), 240)
    sla_breached = time_open_minutes > sla_minutes and record.get("status") != "resolved"
    enriched = record.copy()
    enriched.update(
        {
            "time_open_minutes": round(time_open_minutes, 2),
            "sla_minutes": sla_minutes,
            "sla_breached": sla_breached,
        }
    )
    return enriched


def _parse_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if not isinstance(value, str):
        raise ValueError("opened_at must be an ISO timestamp string")
    parsed = datetime.fromisoformat(value)
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
