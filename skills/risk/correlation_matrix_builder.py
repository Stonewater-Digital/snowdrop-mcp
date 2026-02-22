"""Generate pairwise correlation estimates for asset price series."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "correlation_matrix_builder",
    "description": "Build Pearson correlation matrices from asset price histories.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "price_series": {
                "type": "object",
                "additionalProperties": {
                    "type": "array",
                    "items": {"type": "number"},
                },
            }
        },
        "required": ["price_series"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "matrix": {"type": "object"},
                    "highly_correlated": {"type": "array", "items": {"type": "object"}},
                    "inversely_correlated": {"type": "array", "items": {"type": "object"}},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def correlation_matrix_builder(price_series: dict[str, list[float]], **_: Any) -> dict[str, Any]:
    """Compute Pearson correlations between normalized return series."""

    try:
        assets = sorted(price_series)
        if len(assets) < 2:
            raise ValueError("Provide at least two assets to compute correlations")

        returns: dict[str, list[float]] = {}
        for asset, series in price_series.items():
            if len(series) < 2:
                raise ValueError(f"{asset} must have at least two price points")
            returns[asset] = _to_returns(series)

        matrix: dict[str, dict[str, float]] = {asset: {} for asset in assets}
        high: list[dict[str, Any]] = []
        inverse: list[dict[str, Any]] = []
        for i, asset_a in enumerate(assets):
            for asset_b in assets[i:]:
                corr = _pearson(returns[asset_a], returns[asset_b])
                matrix[asset_a][asset_b] = corr
                matrix[asset_b][asset_a] = corr
                if asset_a == asset_b:
                    continue
                description = {"pair": (asset_a, asset_b), "correlation": round(corr, 4)}
                if corr >= 0.8:
                    high.append(description)
                if corr <= -0.5:
                    inverse.append(description)

        data = {
            "matrix": matrix,
            "highly_correlated": high,
            "inversely_correlated": inverse,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("correlation_matrix_builder", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _to_returns(series: list[float]) -> list[float]:
    returns: list[float] = []
    for prev, current in zip(series, series[1:]):
        if prev == 0:
            raise ValueError("Price series cannot contain zero for return calculations")
        returns.append((current - prev) / prev)
    return returns


def _pearson(series_a: list[float], series_b: list[float]) -> float:
    length = min(len(series_a), len(series_b))
    if length < 2:
        return 0.0
    a = series_a[:length]
    b = series_b[:length]
    mean_a = sum(a) / length
    mean_b = sum(b) / length
    numerator = sum((x - mean_a) * (y - mean_b) for x, y in zip(a, b))
    denom_a = math.sqrt(sum((x - mean_a) ** 2 for x in a))
    denom_b = math.sqrt(sum((y - mean_b) ** 2 for y in b))
    if denom_a == 0 or denom_b == 0:
        return 0.0
    return round(numerator / (denom_a * denom_b), 6)


def _log_lesson(skill_name: str, error: str) -> None:
    """Append a Ralph Wiggum lesson entry."""

    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
