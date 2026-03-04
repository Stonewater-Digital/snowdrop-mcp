"""
Executive Summary: Scores inbound datasets for completeness, duplication, and freshness to unblock NAV workflows.

Inputs: datasets (list[dict]), thresholds (dict[str, float], optional)
Outputs: status (str), data (scorecards/summary), timestamp (str)
MCP Tool Name: data_quality_scorecard
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

DEFAULT_THRESHOLDS: dict[str, float] = {
    "max_null_pct": 5.0,
    "max_dup_pct": 1.0,
    "max_staleness_minutes": 60,
}

TOOL_META: dict[str, Any] = {
    "name": "data_quality_scorecard",
    "description": "Compute null/duplication/freshness scores for administrator datasets and flag breaches.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "datasets": {
                "type": "array",
                "items": {"type": "object"},
                "description": "Dataset payloads with keys: name, row_count, null_counts, duplicate_rows, last_refresh.",
            },
            "thresholds": {
                "type": "object",
                "description": "Overrides for max_null_pct, max_dup_pct, max_staleness_minutes.",
            },
        },
        "required": ["datasets"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["ok", "error"]},
            "data": {
                "type": "object",
                "properties": {
                    "scorecards": {"type": "array", "items": {"type": "object"}},
                    "summary": {"type": "object"},
                },
            },
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def data_quality_scorecard(
    datasets: list[dict[str, Any]],
    thresholds: dict[str, float] | None = None,
) -> dict[str, Any]:
    """Return per-dataset scores for completeness, duplication, and freshness.

    Args:
        datasets: Dataset stats emitted by upstream ingestion steps.
        thresholds: Optional overrides for scoring thresholds.

    Returns:
        Snowdrop response dict containing scorecards and aggregate summary metrics.

    Raises:
        ValueError: If datasets is not a list.
    """
    emitter = SkillTelemetryEmitter(
        "data_quality_scorecard",
        {"datasets": len(datasets or [])},
    )
    try:
        if not isinstance(datasets, list):
            raise ValueError("datasets must be a list of dict payloads")
        merged_thresholds = {**DEFAULT_THRESHOLDS, **(thresholds or {})}
        scorecards: list[dict[str, Any]] = []
        failing = 0
        now = datetime.now(timezone.utc)

        for payload in datasets:
            if not isinstance(payload, dict):
                continue
            name = str(payload.get("name") or "unknown")
            row_count = max(int(payload.get("row_count") or 0), 0)
            null_counts = payload.get("null_counts") or {}
            duplicate_rows = max(int(payload.get("duplicate_rows") or 0), 0)
            last_refresh = _parse_timestamp(payload.get("last_refresh"))

            null_pct = {
                field: _percentage(count, row_count)
                for field, count in null_counts.items()
                if row_count
            }
            null_issues = {
                field: round(pct, 2)
                for field, pct in null_pct.items()
                if pct > merged_thresholds["max_null_pct"]
            }

            dup_pct = _percentage(duplicate_rows, row_count) if row_count else 0.0
            stale_minutes = (
                (now - last_refresh).total_seconds() / 60 if last_refresh else None
            )
            stale_issue = (
                stale_minutes is None
                or stale_minutes > merged_thresholds["max_staleness_minutes"]
            )

            score = 100.0
            score -= len(null_issues) * 5.0
            score -= max(0.0, dup_pct - merged_thresholds["max_dup_pct"])
            if stale_minutes is None:
                score -= 20.0
            else:
                score -= max(
                    0.0,
                    (stale_minutes - merged_thresholds["max_staleness_minutes"]) * 0.2,
                )
            score = max(0.0, round(score, 2))

            status = (
                "pass"
                if not null_issues
                and dup_pct <= merged_thresholds["max_dup_pct"]
                and not stale_issue
                else "fail"
            )
            if status == "fail":
                failing += 1

            scorecards.append(
                {
                    "dataset": name,
                    "row_count": row_count,
                    "score": score,
                    "null_issues": null_issues,
                    "dup_pct": round(dup_pct, 2),
                    "stale_minutes": round(stale_minutes or 0.0, 2),
                    "status": status,
                }
            )

        avg_score = (
            round(sum(card["score"] for card in scorecards) / len(scorecards), 2)
            if scorecards
            else 0.0
        )
        summary = {
            "datasets": len(scorecards),
            "failing": failing,
            "avg_score": avg_score,
            "thresholds": merged_thresholds,
        }
        emitter.record("ok", {"failing": failing, "avg_score": avg_score})
        data = {"scorecards": scorecards, "summary": summary}
        return {"status": "ok", "data": data, "timestamp": get_iso_timestamp()}
    except Exception as exc:  # noqa: BLE001
        logger.error(f"data_quality_scorecard failed: {exc}")
        _log_lesson("data_quality_scorecard", str(exc))
        emitter.record("error", {"error": str(exc)})
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": get_iso_timestamp()}


def _percentage(count: int, denominator: int) -> float:
    """Return 0-100 percentage helper."""
    if not denominator:
        return 0.0
    return (count / denominator) * 100.0


def _parse_timestamp(raw: Any) -> datetime | None:
    """Parse ISO timestamps while tolerating None."""
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


def _log_lesson(skill_name: str, error: str) -> None:
    """Proxy shared lesson logger."""
    _shared_log_lesson(skill_name, error)
