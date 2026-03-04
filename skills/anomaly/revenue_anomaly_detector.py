"""Highlight daily revenue spikes and drawdowns."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "revenue_anomaly_detector",
    "description": "Monitors rolling revenue patterns for drops and spikes.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "daily_revenue": {"type": "array", "items": {"type": "object"}},
            "sensitivity": {
                "type": "string",
                "enum": ["low", "medium", "high"],
                "default": "medium",
            },
        },
        "required": ["daily_revenue"],
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


def revenue_anomaly_detector(
    daily_revenue: list[dict[str, Any]],
    sensitivity: str = "medium",
    **_: Any,
) -> dict[str, Any]:
    """Detect rolling 7-day deviations."""
    try:
        if not daily_revenue:
            raise ValueError("daily_revenue cannot be empty")
        sensitivity = sensitivity.lower()
        sigma_map = {"high": 1.5, "medium": 2.0, "low": 3.0}
        if sensitivity not in sigma_map:
            raise ValueError("sensitivity must be low, medium, or high")

        ordered = sorted(daily_revenue, key=lambda entry: entry["date"])
        amounts = [float(entry["amount"]) for entry in ordered]
        anomalies = []
        threshold = sigma_map[sensitivity]
        for idx, entry in enumerate(ordered):
            window_start = max(0, idx - 6)
            window_values = amounts[window_start : idx + 1]
            if len(window_values) < 3:
                continue
            mean = sum(window_values) / len(window_values)
            variance = sum((val - mean) ** 2 for val in window_values) / max(len(window_values) - 1, 1)
            std_dev = variance ** 0.5
            if std_dev == 0:
                continue
            deviation = (amounts[idx] - mean) / std_dev
            if abs(deviation) > threshold:
                anomalies.append(
                    {
                        "date": entry["date"],
                        "amount": amounts[idx],
                        "z_score": round(deviation, 3),
                        "direction": "drop" if deviation < 0 else "spike",
                    }
                )

        trend = _describe_trend(amounts)
        decline_days = _consecutive_declines(amounts)
        alert_level = _alert_from_anomalies(anomalies, decline_days)
        data = {
            "anomalies": anomalies,
            "trend": trend,
            "consecutive_decline_days": decline_days,
            "alert_level": alert_level,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("revenue_anomaly_detector", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _describe_trend(amounts: list[float]) -> str:
    if len(amounts) < 2:
        return "stable"
    midpoint = max(1, len(amounts) // 2)
    first_avg = sum(amounts[:midpoint]) / midpoint
    last_avg = sum(amounts[midpoint:]) / (len(amounts) - midpoint)
    if last_avg > first_avg * 1.05:
        return "uptrend"
    if last_avg < first_avg * 0.95:
        return "downtrend"
    return "sideways"


def _consecutive_declines(amounts: list[float]) -> int:
    count = 0
    for idx in range(len(amounts) - 1, 0, -1):
        if amounts[idx] < amounts[idx - 1]:
            count += 1
        else:
            break
    return count


def _alert_from_anomalies(anomalies: list[dict[str, Any]], decline_days: int) -> str:
    if decline_days >= 3 or len(anomalies) >= 3:
        return "high"
    if decline_days == 2 or len(anomalies) == 2:
        return "medium"
    if anomalies:
        return "low"
    return "normal"


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
