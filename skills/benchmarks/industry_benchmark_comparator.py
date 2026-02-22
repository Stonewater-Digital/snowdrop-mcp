"""Compare Snowdrop metrics to industry benchmarks."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "industry_benchmark_comparator",
    "description": "Ranks Snowdrop metrics versus benchmark percentiles to highlight strengths and gaps.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "our_metrics": {"type": "object"},
            "benchmarks": {"type": "object"},
        },
        "required": ["our_metrics", "benchmarks"],
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


def industry_benchmark_comparator(
    our_metrics: dict[str, Any],
    benchmarks: dict[str, dict[str, float]],
    **_: Any,
) -> dict[str, Any]:
    """Return percentile rankings with standout metrics."""
    try:
        rankings = []
        above_median = below_median = 0
        standout: list[str] = []
        improvement: list[str] = []
        total_percentile = 0.0
        considered = 0

        for metric, value in our_metrics.items():
            bench = benchmarks.get(metric)
            if not bench:
                continue
            percentile = _percentile(float(value), bench)
            rankings.append(
                {
                    "metric": metric,
                    "value": value,
                    "percentile": percentile,
                }
            )
            considered += 1
            total_percentile += percentile
            if percentile >= 75:
                standout.append(metric)
            if percentile < 50:
                improvement.append(metric)
                below_median += 1
            else:
                above_median += 1

        overall_percentile = total_percentile / considered if considered else 0.0
        data = {
            "rankings": rankings,
            "above_median_count": above_median,
            "below_median_count": below_median,
            "standout_metrics": standout,
            "improvement_areas": improvement,
            "overall_percentile": round(overall_percentile, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("industry_benchmark_comparator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _percentile(value: float, bench: dict[str, float]) -> float:
    p25 = float(bench.get("p25", 0))
    p50 = float(bench.get("p50", p25))
    p75 = float(bench.get("p75", p50))
    p90 = float(bench.get("p90", p75))
    if value <= p25:
        return 25 * (value / p25) if p25 else 10
    if value <= p50:
        return 25 + 25 * ((value - p25) / (p50 - p25 or 1))
    if value <= p75:
        return 50 + 25 * ((value - p50) / (p75 - p50 or 1))
    if value <= p90:
        return 75 + 15 * ((value - p75) / (p90 - p75 or 1))
    return 90 + 10 * ((value - p90) / (p90 or 1))


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
