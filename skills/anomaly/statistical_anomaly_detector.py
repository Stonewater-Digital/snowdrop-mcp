"""Detect time-series anomalies using Z-scores."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "statistical_anomaly_detector",
    "description": "Flags z-score anomalies across global or rolling windows.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "values": {"type": "array", "items": {"type": "number"}},
            "labels": {"type": "array", "items": {"type": "string"}},
            "z_threshold": {"type": "number", "default": 2.5},
            "window": {"type": ["integer", "null"], "default": None},
        },
        "required": ["values", "labels"],
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


def statistical_anomaly_detector(
    values: list[float],
    labels: list[str],
    z_threshold: float = 2.5,
    window: int | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Flag points with z-score magnitude exceeding the threshold."""
    try:
        if len(values) != len(labels):
            raise ValueError("values and labels must align")
        if not values:
            raise ValueError("values cannot be empty")
        if z_threshold <= 0:
            raise ValueError("z_threshold must be positive")
        if window is not None and window <= 1:
            raise ValueError("window must be greater than 1 when provided")

        anomalies = []
        means = []
        stds = []
        for idx, value in enumerate(values):
            start = 0 if window is None else max(0, idx - window + 1)
            window_slice = values[start : idx + 1]
            mean = sum(window_slice) / len(window_slice)
            variance = sum((val - mean) ** 2 for val in window_slice) / max(len(window_slice) - 1, 1)
            std_dev = math.sqrt(variance)
            z_score = 0.0 if std_dev == 0 else (value - mean) / std_dev
            means.append(mean)
            stds.append(std_dev)
            if abs(z_score) > z_threshold:
                anomalies.append(
                    {
                        "label": labels[idx],
                        "value": value,
                        "z_score": round(z_score, 4),
                    }
                )

        data = {
            "anomalies": anomalies,
            "mean": round(sum(values) / len(values), 4),
            "std_dev": round(math.sqrt(sum((v - (sum(values) / len(values))) ** 2 for v in values) / (len(values) - 1)), 4)
            if len(values) > 1
            else 0.0,
            "anomaly_rate_pct": round(len(anomalies) / len(values) * 100, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("statistical_anomaly_detector", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
