"""Measure cross-asset correlations for diversification checks."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "cross_asset_correlation",
    "description": "Computes pairwise correlations across asset classes and flags concentration risks.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "asset_class_returns": {
                "type": "object",
                "additionalProperties": {
                    "type": "array",
                    "items": {"type": "number"},
                },
            }
        },
        "required": ["asset_class_returns"],
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


def cross_asset_correlation(asset_class_returns: dict[str, list[float]], **_: Any) -> dict[str, Any]:
    """Return correlation pairs and diversification score."""
    try:
        classes = list(asset_class_returns)
        if len(classes) < 2:
            raise ValueError("Need at least two asset classes")
        length_set = {len(asset_class_returns[name]) for name in classes}
        if len(length_set) != 1:
            raise ValueError("All series must be same length")
        length = length_set.pop()
        if length < 2:
            raise ValueError("Each series requires >=2 observations")
        normalized = {name: [float(r) for r in asset_class_returns[name]] for name in classes}
        means = {name: sum(series) / length for name, series in normalized.items()}
        correlations = []
        for i, a in enumerate(classes):
            for b in classes[i + 1 :]:
                cov = sum((normalized[a][k] - means[a]) * (normalized[b][k] - means[b]) for k in range(length))
                var_a = sum((normalized[a][k] - means[a]) ** 2 for k in range(length))
                var_b = sum((normalized[b][k] - means[b]) ** 2 for k in range(length))
                corr = cov / ((var_a * var_b) ** 0.5) if var_a and var_b else 0.0
                correlations.append({"pair": [a, b], "correlation": round(corr, 3)})
        avg_abs = sum(abs(item["correlation"]) for item in correlations) / len(correlations)
        data = {
            "pairwise_correlations": correlations,
            "average_absolute_correlation": round(avg_abs, 3),
            "diversification_score": round(1 - avg_abs, 3),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        _log_lesson(f"cross_asset_correlation: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
