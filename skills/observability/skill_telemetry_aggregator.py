"""
Executive Summary: Aggregates per-skill telemetry samples, computes health summaries, and flags skills breaching latency or error thresholds.

Inputs: metrics (list[dict]), window_minutes (int, optional), error_threshold_pct (float, optional)
Outputs: status (str), data (summary/outliers/raw_samples), timestamp (str)
MCP Tool Name: skill_telemetry_aggregator
"""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta, timezone
from statistics import fmean
from typing import Any, Callable

from skills.utils import (
    SkillTelemetryEmitter,
    get_iso_timestamp,
    logger,
    log_lesson as _shared_log_lesson,
)

TOOL_META: dict[str, Any] = {
    "name": "skill_telemetry_aggregator",
    "description": "Process telemetry samples from Snowdrop skills and emit aggregated health metrics with outlier detection.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "metrics": {
                "type": "array",
                "items": {"type": "object"},
                "description": "Telemetry samples containing at least skill_name, latency_ms, status, timestamp.",
            },
            "window_minutes": {
                "type": "integer",
                "default": 60,
                "description": "Only samples within this lookback window are considered.",
            },
            "error_threshold_pct": {
                "type": "number",
                "default": 5.0,
                "description": "Error rate percentage that triggers an outlier flag.",
            },
            "notify_on_outliers": {
                "type": "boolean",
                "default": False,
                "description": "Send Thunder alerts via thunder_signal when outliers appear.",
            },
        },
        "required": ["metrics"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["ok", "error"]},
            "data": {
                "type": "object",
                "properties": {
                    "summary": {"type": "object"},
                    "outliers": {"type": "array", "items": {"type": "object"}},
                    "raw_samples": {"type": "array", "items": {"type": "object"}},
                },
            },
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def skill_telemetry_aggregator(
    metrics: list[dict[str, Any]],
    window_minutes: int = 60,
    error_threshold_pct: float = 5.0,
    notify_on_outliers: bool = False,
    alert_hook: Callable[..., Any] | None = None,
) -> dict[str, Any]:
    """Aggregate telemetry samples and identify outlier skills.

    Args:
        metrics: Telemetry samples from skills.
        window_minutes: Sliding window for considering samples.
        error_threshold_pct: Error rate percentage that triggers an outlier flag.
        notify_on_outliers: When True, send a Thunder alert if outliers exist.
        alert_hook: Optional override for thunder_signal (used for tests).

    Returns:
        Snowdrop skill response dict containing aggregate metrics and outliers.

    Raises:
        ValueError: If metrics input is invalid.
    """
    emitter = SkillTelemetryEmitter(
        "skill_telemetry_aggregator",
        {
            "window_minutes": window_minutes,
            "error_threshold_pct": error_threshold_pct,
            "metrics_received": len(metrics) if isinstance(metrics, list) else 0,
        },
    )
    try:
        if not isinstance(metrics, list):
            raise ValueError("metrics must be a list of dict samples")
        if window_minutes <= 0:
            raise ValueError("window_minutes must be > 0")
        if error_threshold_pct < 0:
            raise ValueError("error_threshold_pct must be >= 0")

        lookback_cutoff = datetime.now(timezone.utc) - timedelta(minutes=window_minutes)
        cleaned_samples, invalid_count = _clean_samples(metrics, lookback_cutoff)
        overall_summary, outliers = _summaries(cleaned_samples, error_threshold_pct)

        if metrics and invalid_count / len(metrics) > 0.1:
            _log_lesson(
                "skill_telemetry_aggregator",
                f"High invalid sample ratio ({invalid_count}/{len(metrics)})",
            )

        data = {
            "summary": overall_summary,
            "outliers": outliers,
            "raw_samples": cleaned_samples,
        }
        emitter.record("ok", {"outliers": len(outliers), "invalid_samples": invalid_count})
        if outliers and (notify_on_outliers or alert_hook):
            _notify_outliers(outliers, overall_summary, alert_hook=alert_hook)
        return {"status": "ok", "data": data, "timestamp": get_iso_timestamp()}
    except Exception as exc:
        msg = f"skill_telemetry_aggregator failed: {exc}"
        logger.error(msg)
        _log_lesson("skill_telemetry_aggregator", str(exc))
        emitter.record("error", {"error": str(exc)})
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": get_iso_timestamp()}


def _clean_samples(
    metrics: list[dict[str, Any]],
    cutoff: datetime,
) -> tuple[list[dict[str, Any]], int]:
    """Normalize metrics and exclude ones outside the time window."""
    cleaned: list[dict[str, Any]] = []
    invalid = 0
    for sample in metrics:
        if not isinstance(sample, dict):
            invalid += 1
            continue

        timestamp = _parse_timestamp(sample.get("timestamp")) or datetime.now(timezone.utc)
        if timestamp < cutoff:
            continue

        skill_name = str(sample.get("skill_name", "unknown")).strip()
        latency = _to_float(sample.get("latency_ms"))
        status = str(sample.get("status", "unknown")).lower()
        if status not in {"ok", "error"}:
            status = "unknown"

        if latency is None:
            invalid += 1
            continue

        cleaned.append(
            {
                "skill_name": skill_name or "unknown",
                "latency_ms": latency,
                "status": status,
                "timestamp": timestamp.isoformat(),
            }
        )
    return cleaned, invalid


def _summaries(
    samples: list[dict[str, Any]],
    error_threshold_pct: float,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Compute aggregate metrics and identify outlier skills."""
    if not samples:
        return (
            {
                "total_samples": 0,
                "ok_count": 0,
                "error_count": 0,
                "avg_latency_ms": 0.0,
                "p95_latency_ms": 0.0,
            },
            [],
        )

    per_skill: dict[str, list[dict[str, Any]]] = defaultdict(list)
    latencies = []
    ok_count = 0
    error_count = 0

    for sample in samples:
        per_skill[sample["skill_name"]].append(sample)
        latencies.append(sample["latency_ms"])
        if sample["status"] == "error":
            error_count += 1
        elif sample["status"] == "ok":
            ok_count += 1

    avg_latency = fmean(latencies)
    p95_latency = _percentile(latencies, 0.95)

    outliers: list[dict[str, Any]] = []
    for skill, skill_samples in per_skill.items():
        error_rate = (
            sum(1 for sample in skill_samples if sample["status"] == "error")
            / len(skill_samples)
            * 100
        )
        avg_skill_latency = fmean(sample["latency_ms"] for sample in skill_samples)
        reasons = []
        if error_rate >= error_threshold_pct:
            reasons.append(f"error_rate={error_rate:.2f}%")
        if p95_latency and avg_skill_latency > p95_latency:
            reasons.append(
                f"latency_exceeds_p95 ({avg_skill_latency:.1f}ms > {p95_latency:.1f}ms)"
            )
        if reasons:
            outliers.append(
                {
                    "skill_name": skill,
                    "sample_count": len(skill_samples),
                    "error_rate_pct": round(error_rate, 2),
                    "avg_latency_ms": round(avg_skill_latency, 2),
                    "reasons": reasons,
                }
            )

    overall = {
        "total_samples": len(samples),
        "ok_count": ok_count,
        "error_count": error_count,
        "avg_latency_ms": round(avg_latency, 2),
        "p95_latency_ms": round(p95_latency, 2),
        "window_samples": len(samples),
    }
    return overall, outliers


def _percentile(values: list[float], percentile: float) -> float:
    """Return percentile using linear interpolation."""
    if not values:
        return 0.0
    sorted_values = sorted(values)
    k = (len(sorted_values) - 1) * percentile
    lower = int(k)
    upper = min(lower + 1, len(sorted_values) - 1)
    weight = k - lower
    return sorted_values[lower] * (1 - weight) + sorted_values[upper] * weight


def _parse_timestamp(raw: Any) -> datetime | None:
    """Parse ISO timestamp safely."""
    if raw is None:
        return None
    try:
        ts = str(raw).replace("Z", "+00:00")
        parsed = datetime.fromisoformat(ts)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except (ValueError, TypeError):
        return None


def _to_float(value: Any) -> float | None:
    """Convert to float when possible."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _log_lesson(skill_name: str, error: str) -> None:
    """Proxy to shared lesson logger."""
    _shared_log_lesson(skill_name, error)


def _notify_outliers(
    outliers: list[dict[str, Any]],
    summary: dict[str, Any],
    *,
    alert_hook: Callable[..., Any] | None = None,
) -> None:
    """Send a Thunder alert summarizing the outlier skills."""
    try:
        hook = alert_hook
        if hook is None:
            from skills.thunder_signal import thunder_signal as hook  # pylint: disable=import-outside-toplevel

        critical = any(item.get("error_rate_pct", 0) >= 25 for item in outliers)
        severity = "CRITICAL" if critical else "WARNING"
        top = sorted(outliers, key=lambda item: item.get("error_rate_pct", 0), reverse=True)[:5]
        lines = [
            "Telemetry outliers detected:",
            f"Samples={summary.get('total_samples', 0)}, Errors={summary.get('error_count', 0)}",
        ]
        for item in top:
            reason_text = ", ".join(item.get("reasons", []))
            lines.append(
                f"- {item['skill_name']} err={item['error_rate_pct']}% "
                f"lat={item['avg_latency_ms']}ms ({reason_text})"
            )
        message = "\n".join(lines)
        hook(severity=severity, message=message)
        logger.info(
            "skill_telemetry_aggregator dispatched Thunder alert severity=%s outliers=%d",
            severity,
            len(outliers),
        )
    except Exception as exc:  # noqa: BLE001
        logger.error(f"skill_telemetry_aggregator alert failed: {exc}")
        _log_lesson("skill_telemetry_aggregator", f"Alert dispatch failed: {exc}")
