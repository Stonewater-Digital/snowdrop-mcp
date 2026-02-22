"""Track prompt A/B test results and declare winners."""
from __future__ import annotations

import json
import os
import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "prompt_ab_tester",
    "description": "Appends prompt experiment outcomes and computes per-variant stats.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "test_name": {"type": "string"},
            "variant": {"type": "string", "enum": ["A", "B"]},
            "result": {"type": "object"},
        },
        "required": ["test_name", "variant", "result"],
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

STATS_PATH = "logs/prompt_ab_tests.json"


def prompt_ab_tester(
    test_name: str,
    variant: str,
    result: dict[str, Any],
    **_: Any,
) -> dict[str, Any]:
    """Return aggregated stats after recording the latest result."""

    try:
        stats = _load_stats()
        test = stats.setdefault(test_name, {"A": _empty_stats(), "B": _empty_stats()})
        bucket = test[variant]
        bucket["samples"] += 1
        bucket["successes"] += 1 if result.get("success") else 0
        bucket["quality_total"] += float(result.get("quality_score", 0))
        bucket["tokens_total"] += int(result.get("tokens_used", 0))
        bucket["latency_total_ms"] += int(result.get("latency_ms", 0))
        _save_stats(stats)

        metrics = {key: _compute_metrics(value) for key, value in test.items()}
        winner = _winner(metrics)
        data = {"metrics": metrics, "winner": winner}
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("prompt_ab_tester", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _empty_stats() -> dict[str, Any]:
    return {"samples": 0, "successes": 0, "quality_total": 0.0, "tokens_total": 0, "latency_total_ms": 0}


def _compute_metrics(stat: dict[str, Any]) -> dict[str, Any]:
    samples = stat["samples"]
    success_rate = stat["successes"] / samples if samples else 0.0
    avg_quality = stat["quality_total"] / samples if samples else 0.0
    avg_cost = stat["tokens_total"] / samples if samples else 0.0
    avg_latency = stat["latency_total_ms"] / samples if samples else 0.0
    return {
        "sample_size": samples,
        "success_rate": round(success_rate, 4),
        "avg_quality": round(avg_quality, 3),
        "avg_cost_tokens": round(avg_cost, 2),
        "avg_latency_ms": round(avg_latency, 1),
    }


def _winner(metrics: dict[str, dict[str, Any]]) -> str | None:
    a = metrics["A"]
    b = metrics["B"]
    if a["sample_size"] < 30 or b["sample_size"] < 30:
        return None
    z = _z_score(a["success_rate"], b["success_rate"], a["sample_size"], b["sample_size"])
    if z is None:
        return None
    if z > 1.96:
        return "A"
    if z < -1.96:
        return "B"
    return None


def _z_score(p1: float, p2: float, n1: int, n2: int) -> float | None:
    pooled = (p1 * n1 + p2 * n2) / (n1 + n2)
    variance = pooled * (1 - pooled) * (1 / n1 + 1 / n2)
    if variance == 0:
        return None
    return (p1 - p2) / math.sqrt(variance)


def _load_stats() -> dict[str, Any]:
    if not os.path.exists(STATS_PATH):
        return {}
    with open(STATS_PATH, "r", encoding="utf-8") as handle:
        try:
            return json.load(handle)
        except json.JSONDecodeError:
            return {}


def _save_stats(stats: dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(STATS_PATH), exist_ok=True)
    with open(STATS_PATH, "w", encoding="utf-8") as handle:
        json.dump(stats, handle, indent=2)


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
