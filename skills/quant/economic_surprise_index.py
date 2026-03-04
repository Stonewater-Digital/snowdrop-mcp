"""Construct an economic surprise index from release data."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable

TOOL_META: dict[str, Any] = {
    "name": "economic_surprise_index",
    "description": "Computes weighted surprise index using normalized release beats/misses.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "releases": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "actual": {"type": "number"},
                        "consensus": {"type": "number"},
                        "std_dev": {"type": "number"},
                        "weight": {"type": "number", "default": 1.0},
                    },
                    "required": ["name", "actual", "consensus", "std_dev"],
                },
            }
        },
        "required": ["releases"],
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


def economic_surprise_index(releases: Iterable[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return weighted index of normalized surprises."""
    try:
        release_list = list(releases)
        if not release_list:
            raise ValueError("releases cannot be empty")
        surprises = []
        weighted_sum = 0.0
        weight_total = 0.0
        for entry in release_list:
            std_dev = float(entry.get("std_dev", 0))
            if std_dev <= 0:
                raise ValueError("std_dev must be positive for all releases")
            surprise = (float(entry["actual"]) - float(entry["consensus"])) / std_dev
            weight = float(entry.get("weight", 1.0))
            weighted_sum += surprise * weight
            weight_total += weight
            surprises.append({"name": entry["name"], "z_score": round(surprise, 2), "weight": weight})
        index_value = weighted_sum / weight_total if weight_total else 0.0
        data = {
            "release_surprises": surprises,
            "surprise_index": round(index_value, 2),
            "signal": "strong" if index_value > 0.5 else "weak" if index_value < -0.5 else "neutral",
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        _log_lesson(f"economic_surprise_index: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
