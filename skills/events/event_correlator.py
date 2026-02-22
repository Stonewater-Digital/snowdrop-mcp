"""Correlate multiple events to detect compound incidents."""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "event_correlator",
    "description": "Evaluates correlation rules to surface compound incidents.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "events": {
                "type": "array",
                "items": {"type": "object"},
            },
            "correlation_rules": {
                "type": "array",
                "items": {"type": "object"},
            },
        },
        "required": ["events", "correlation_rules"],
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


_SEVERITY_ORDER = {"low": 1, "medium": 2, "high": 3, "critical": 4}


def event_correlator(
    events: list[dict[str, Any]],
    correlation_rules: list[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    """Apply correlation rules to event streams."""
    try:
        parsed_events = [_parse_event(event) for event in events]
        parsed_events.sort(key=lambda item: item["timestamp"])

        incidents: list[dict[str, Any]] = []
        for rule in correlation_rules:
            if not isinstance(rule, dict):
                raise ValueError("each correlation rule must be a dict")
            required = [typ.lower() for typ in rule.get("required_events", [])]
            if not required:
                continue
            window_minutes = int(rule.get("time_window_minutes", 10))
            min_count = int(rule.get("min_count", len(required)))
            rule_name = str(rule.get("name", "unnamed_rule"))
            rule_incidents = _apply_rule(parsed_events, required, window_minutes, min_count, rule_name)
            incidents.extend(rule_incidents)

        result = {
            "correlated_incidents": incidents,
            "false_alarm_check": len(incidents) == 0,
        }
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("event_correlator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _apply_rule(
    events: list[dict[str, Any]],
    required_events: list[str],
    window_minutes: int,
    min_count: int,
    rule_name: str,
) -> list[dict[str, Any]]:
    window = timedelta(minutes=window_minutes)
    incidents: list[dict[str, Any]] = []
    seen_windows: set[tuple[str, str]] = set()

    for idx, event in enumerate(events):
        end_time = event["timestamp"]
        start_time = end_time - window
        window_events = [ev for ev in events if start_time <= ev["timestamp"] <= end_time]
        counts = Counter(ev["type"] for ev in window_events if ev["type"] in required_events)
        if all(counts.get(req, 0) >= 1 for req in required_events) and len(window_events) >= min_count:
            window_key = (start_time.isoformat(), end_time.isoformat())
            if window_key in seen_windows:
                continue
            seen_windows.add(window_key)
            incidents.append(
                {
                    "rule": rule_name,
                    "window_start": start_time.isoformat(),
                    "window_end": end_time.isoformat(),
                    "event_count": len(window_events),
                    "severity": _max_severity(window_events),
                    "events": [ev["original"] for ev in window_events],
                }
            )
    return incidents


def _max_severity(window_events: list[dict[str, Any]]) -> str:
    max_score = 0
    max_label = "low"
    for event in window_events:
        score = _SEVERITY_ORDER.get(event.get("severity", "low"), 1)
        if score > max_score:
            max_score = score
            max_label = event.get("severity", "low")
    return max_label


def _parse_event(event: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(event, dict):
        raise ValueError("events must be dicts")
    try:
        ts = datetime.fromisoformat(str(event.get("timestamp")))
    except ValueError as exc:  # noqa: B904
        raise ValueError(f"Invalid event timestamp: {event.get('timestamp')}") from exc
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    return {
        "type": str(event.get("type", "unknown")).lower(),
        "timestamp": ts,
        "severity": str(event.get("severity", "low")).lower(),
        "source": event.get("source"),
        "original": event,
    }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
