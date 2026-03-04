"""Constrained asset allocation optimizer."""
from __future__ import annotations

import math
import random
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "asset_allocation_optimizer",
    "description": "Finds feasible allocations that hit target return/risk under constraints.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "assets": {"type": "array", "items": {"type": "object"}},
            "constraints": {"type": "object"},
            "target_return": {"type": ["number", "null"]},
            "target_risk": {"type": ["number", "null"]},
        },
        "required": ["assets", "constraints"],
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


def asset_allocation_optimizer(
    assets: list[dict[str, Any]],
    constraints: dict[str, Any],
    target_return: float | None = None,
    target_risk: float | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Return the allocation with best Sharpe ratio satisfying constraints."""
    try:
        if not assets:
            raise ValueError("assets cannot be empty")
        rng = random.Random(8)
        min_weight = float(constraints.get("min_weight", 0.0))
        max_weight = float(constraints.get("max_weight", 1.0))
        max_single = float(constraints.get("max_single_position", max_weight))
        required_assets = set(constraints.get("required_assets", []))

        best_portfolio = None
        for _ in range(2000):
            weights = _random_feasible_weights(len(assets), min_weight, max_weight, rng)
            if not weights:
                continue
            allocation = dict(zip([asset["name"] for asset in assets], weights))
            if not required_assets.issubset({name for name, w in allocation.items() if w > 0}):
                continue
            if any(weight > max_single for weight in allocation.values()):
                continue
            exp_return = sum(weight * float(asset.get("expected_return", 0.0)) for asset, weight in zip(assets, weights))
            variance = sum((weight * float(asset.get("volatility", 0.0))) ** 2 for asset, weight in zip(assets, weights))
            risk = math.sqrt(max(variance, 0.0))
            if target_return and exp_return < target_return:
                continue
            if target_risk and risk > target_risk:
                continue
            sharpe = exp_return / risk if risk else 0.0
            portfolio = {
                "weights": allocation,
                "expected_return": round(exp_return, 4),
                "expected_risk": round(risk, 4),
                "sharpe": round(sharpe, 4),
            }
            if not best_portfolio or sharpe > best_portfolio["sharpe"]:
                best_portfolio = portfolio

        if not best_portfolio:
            raise ValueError("No feasible allocation met the targets")
        data = best_portfolio
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("asset_allocation_optimizer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _random_feasible_weights(
    n: int, min_weight: float, max_weight: float, rng: random.Random
) -> list[float] | None:
    weights = [rng.uniform(min_weight, max_weight) for _ in range(n)]
    total = sum(weights)
    if total == 0:
        return None
    weights = [weight / total for weight in weights]
    if any(weight < min_weight or weight > max_weight for weight in weights):
        return None
    return weights


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
