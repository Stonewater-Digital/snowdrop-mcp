"""
Executive Summary: Builds lineage graphs for upstream datasets and highlights stale or missing dependencies.

Inputs: artifacts (list[dict]), staleness_minutes (int, optional)
Outputs: status (str), data (graph/missing/stale/summary), timestamp (str)
MCP Tool Name: data_provenance_map
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

TOOL_META: dict[str, Any] = {
    "name": "data_provenance_map",
    "description": "Construct lineage graph from ingestion artifacts and flag stale datasets or missing dependencies.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "artifacts": {
                "type": "array",
                "items": {"type": "object"},
                "description": "Lineage nodes with dataset, source_system, dependencies, last_updated.",
            },
            "staleness_minutes": {
                "type": "integer",
                "default": 180,
                "description": "Minutes after which a dataset is considered stale.",
            },
        },
        "required": ["artifacts"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["ok", "error"]},
            "data": {
                "type": "object",
                "properties": {
                    "graph": {"type": "object"},
                    "stale_nodes": {"type": "array", "items": {"type": "string"}},
                    "missing_dependencies": {"type": "array", "items": {"type": "string"}},
                    "summary": {"type": "object"},
                },
            },
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def data_provenance_map(
    artifacts: list[dict[str, Any]],
    staleness_minutes: int = 180,
) -> dict[str, Any]:
    """Produce lineage metadata for ingestion datasets.

    Args:
        artifacts: Lineage descriptions for datasets.
        staleness_minutes: Threshold in minutes to mark nodes stale.

    Returns:
        Snowdrop response dict with lineage graph and summary stats.

    Raises:
        ValueError: When inputs are invalid.
    """
    emitter = SkillTelemetryEmitter(
        "data_provenance_map",
        {"artifacts": len(artifacts or []), "staleness_minutes": staleness_minutes},
    )
    try:
        if not isinstance(artifacts, list):
            raise ValueError("artifacts must be a list of dicts")
        if staleness_minutes <= 0:
            raise ValueError("staleness_minutes must be positive")

        graph: dict[str, dict[str, Any]] = {}
        known_datasets: set[str] = set()
        now = datetime.now(timezone.utc)

        for artifact in artifacts:
            if not isinstance(artifact, dict):
                continue
            dataset = str(artifact.get("dataset") or "").strip()
            if not dataset:
                continue
            dependencies = [str(dep) for dep in (artifact.get("dependencies") or []) if dep]
            last_updated = _parse_timestamp(artifact.get("last_updated"))
            graph[dataset] = {
                "source_system": artifact.get("source_system"),
                "dependencies": dependencies,
                "record_count": artifact.get("record_count"),
                "last_updated": last_updated.isoformat() if last_updated else None,
            }
            known_datasets.add(dataset)

        missing_dependencies = sorted(
            {
                dep
                for details in graph.values()
                for dep in details["dependencies"]
                if dep not in known_datasets
            }
        )

        stale_nodes = []
        for dataset, details in graph.items():
            updated_at = _parse_timestamp(details["last_updated"])
            age_minutes = (
                (now - updated_at).total_seconds() / 60 if updated_at else float("inf")
            )
            if age_minutes > staleness_minutes:
                stale_nodes.append(dataset)
                details["stale_minutes"] = round(age_minutes, 2)

        summary = {
            "nodes": len(graph),
            "missing_dependencies": len(missing_dependencies),
            "stale_nodes": len(stale_nodes),
        }
        emitter.record(
            "ok",
            {"stale_nodes": len(stale_nodes), "missing_dependencies": len(missing_dependencies)},
        )
        data = {
            "graph": graph,
            "stale_nodes": stale_nodes,
            "missing_dependencies": missing_dependencies,
            "summary": summary,
        }
        return {"status": "ok", "data": data, "timestamp": get_iso_timestamp()}
    except Exception as exc:  # noqa: BLE001
        logger.error(f"data_provenance_map failed: {exc}")
        _log_lesson("data_provenance_map", str(exc))
        emitter.record("error", {"error": str(exc)})
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": get_iso_timestamp()}


def _parse_timestamp(value: Any) -> datetime | None:
    """Parse ISO timestamps to UTC."""
    if value in (None, ""):
        return None
    try:
        ts = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        return ts.astimezone(timezone.utc)
    except (ValueError, TypeError):
        return None


def _log_lesson(skill_name: str, error: str) -> None:
    """Proxy shared logger."""
    _shared_log_lesson(skill_name, error)
