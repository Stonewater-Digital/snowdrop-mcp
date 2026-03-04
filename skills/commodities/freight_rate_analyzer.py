"""Analyze freight trends and route spreads."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any, Iterable, Sequence

TOOL_META: dict[str, Any] = {
    "name": "freight_rate_analyzer",
    "description": (
        "Evaluates shipping freight index momentum, route-level rate dispersion, "
        "and market tightness signals for dry bulk, tanker, or container markets."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "index_history": {
                "type": "array",
                "items": {"type": "number"},
                "description": "Freight index time series (e.g. Baltic Dry Index), oldest to newest. Min 2 points.",
                "minItems": 2,
            },
            "route_rates": {
                "type": "array",
                "description": "Current rate observations by route.",
                "items": {
                    "type": "object",
                    "properties": {
                        "route": {
                            "type": "string",
                            "description": "Route identifier (e.g. 'C3_Tubarao_Qingdao').",
                        },
                        "rate": {
                            "type": "number",
                            "description": "Current rate for this route (must be >= 0).",
                        },
                    },
                    "required": ["route", "rate"],
                },
                "minItems": 1,
            },
            "tightness_threshold_pct": {
                "type": "number",
                "default": 20.0,
                "description": "% gain from start of series to flag 'tight' market. Default 20%.",
            },
        },
        "required": ["index_history", "route_rates"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "index_change_pct": {"type": "number"},
            "series_change_pct": {"type": "number"},
            "index_volatility_pct": {"type": "number"},
            "avg_route_rate": {"type": "number"},
            "route_dispersion_pct": {"type": "number"},
            "highest_rate_route": {"type": "object"},
            "lowest_rate_route": {"type": "object"},
            "tightness_signal": {"type": "string"},
            "timestamp": {"type": "string"},
        },
    },
}


def freight_rate_analyzer(
    index_history: Sequence[float],
    route_rates: Iterable[dict[str, Any]],
    tightness_threshold_pct: float = 20.0,
    **_: Any,
) -> dict[str, Any]:
    """Return momentum and dispersion metrics for freight markets.

    Args:
        index_history: Freight index time series, oldest to newest (>= 2 points, all > 0).
        route_rates: List of route dicts with 'route' name and current 'rate'.
        tightness_threshold_pct: % gain over full series to label market 'tight'. Default 20%.

    Returns:
        dict with status, index_change_pct (latest vs prior), series_change_pct (latest vs first),
        index_volatility_pct (realized vol of index changes), avg_route_rate, route_dispersion_pct
        (coefficient of variation of route rates), highest/lowest rate routes, and tightness_signal.

    Route dispersion = std_dev(rates) / mean(rates) * 100 (coefficient of variation).
    Index volatility = std_dev of period-over-period % changes in index.
    """
    try:
        history = [float(v) for v in index_history]
        if len(history) < 2:
            raise ValueError("index_history needs at least 2 data points")
        if any(v <= 0 for v in history):
            raise ValueError("All index_history values must be positive")

        route_list = list(route_rates)
        if not route_list:
            raise ValueError("route_rates cannot be empty")
        for r in route_list:
            if float(r["rate"]) < 0:
                raise ValueError(f"Route rate must be >= 0 for route '{r['route']}'")

        latest = history[-1]
        prior = history[-2]
        first = history[0]

        # Period-over-period change (most recent)
        index_change_pct = (latest / prior - 1.0) * 100.0 if prior > 0 else 0.0
        # Full-series change
        series_change_pct = (latest / first - 1.0) * 100.0 if first > 0 else 0.0

        # Realized index volatility from all period returns
        period_returns = [(history[i] / history[i - 1] - 1.0) * 100.0 for i in range(1, len(history))]
        if len(period_returns) >= 2:
            mean_ret = sum(period_returns) / len(period_returns)
            vol = math.sqrt(sum((r - mean_ret) ** 2 for r in period_returns) / (len(period_returns) - 1))
        else:
            vol = 0.0

        # Route rate statistics
        rates = [float(r["rate"]) for r in route_list]
        avg_rate = sum(rates) / len(rates)
        if len(rates) >= 2:
            mean_r = avg_rate
            std_r = math.sqrt(sum((r - mean_r) ** 2 for r in rates) / (len(rates) - 1))
            dispersion_pct = std_r / avg_rate * 100.0 if avg_rate > 0 else 0.0
        else:
            dispersion_pct = 0.0

        highest = max(route_list, key=lambda item: float(item["rate"]))
        lowest = min(route_list, key=lambda item: float(item["rate"]))

        tightness_signal = "tight" if series_change_pct >= tightness_threshold_pct else "soft"

        return {
            "status": "success",
            "index_change_pct": round(index_change_pct, 2),
            "series_change_pct": round(series_change_pct, 2),
            "index_volatility_pct": round(vol, 2),
            "avg_route_rate": round(avg_rate, 2),
            "route_dispersion_pct": round(dispersion_pct, 2),
            "highest_rate_route": {"route": highest["route"], "rate": float(highest["rate"])},
            "lowest_rate_route": {"route": lowest["route"], "rate": float(lowest["rate"])},
            "tightness_signal": tightness_signal,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("freight_rate_analyzer", str(exc))
        return {
            "status": "error",
            "error": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
