"""Monte Carlo approximation of the efficient frontier."""
from __future__ import annotations

import math
import random
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "efficient_frontier_calculator",
    "description": "Generates random portfolios to approximate the efficient frontier and key points.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "assets": {"type": "array", "items": {"type": "object"}},
            "correlation_matrix": {"type": "object"},
            "num_portfolios": {"type": "integer", "default": 500},
            "risk_free_rate": {"type": "number", "default": 0.05},
        },
        "required": ["assets", "correlation_matrix"],
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


def efficient_frontier_calculator(
    assets: list[dict[str, Any]],
    correlation_matrix: dict[str, dict[str, float]],
    num_portfolios: int = 500,
    risk_free_rate: float = 0.05,
    **_: Any,
) -> dict[str, Any]:
    """Return sampled efficient frontier, max Sharpe, and min variance portfolio data."""
    try:
        if len(assets) < 2:
            raise ValueError("At least two assets required")
        rng = random.Random(42)
        portfolios = []
        best_sharpe = None
        min_variance = None
        for _ in range(max(10, num_portfolios)):
            weights = _random_weights(len(assets), rng)
            expected_return = sum(
                weights[i] * float(assets[i].get("expected_return", 0.0))
                for i in range(len(assets))
            )
            variance = _portfolio_variance(weights, assets, correlation_matrix)
            std_dev = math.sqrt(variance)
            sharpe = (expected_return - risk_free_rate) / std_dev if std_dev else 0.0
            snapshot = {
                "weights": dict(zip([asset["name"] for asset in assets], weights)),
                "expected_return": round(expected_return, 4),
                "risk": round(std_dev, 4),
                "sharpe": round(sharpe, 4),
            }
            portfolios.append(snapshot)
            if not best_sharpe or sharpe > best_sharpe["sharpe"]:
                best_sharpe = snapshot
            if not min_variance or std_dev < min_variance["risk"]:
                min_variance = snapshot

        data = {
            "frontier": portfolios,
            "max_sharpe": best_sharpe,
            "min_variance": min_variance,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("efficient_frontier_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _random_weights(n: int, rng: random.Random) -> list[float]:
    raw = [rng.random() for _ in range(n)]
    total = sum(raw)
    return [value / total for value in raw]


def _portfolio_variance(
    weights: list[float],
    assets: list[dict[str, Any]],
    correlation_matrix: dict[str, dict[str, float]],
) -> float:
    variance = 0.0
    for i, asset_i in enumerate(assets):
        for j, asset_j in enumerate(assets):
            corr = correlation_matrix.get(asset_i["name"], {}).get(asset_j["name"], 0.0)
            sigma_i = float(asset_i.get("volatility", 0.0))
            sigma_j = float(asset_j.get("volatility", 0.0))
            variance += weights[i] * weights[j] * sigma_i * sigma_j * corr
    return variance


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
