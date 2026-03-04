"""Compute portfolio volatility from weights and covariance."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "portfolio_volatility_calculator",
    "description": "Estimates portfolio variance and volatility from a covariance matrix.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "weights": {"type": "array", "items": {"type": "number"}},
            "covariance_matrix": {
                "type": "array",
                "items": {
                    "type": "array",
                    "items": {"type": "number"},
                },
            },
            "period_label": {"type": "string", "default": "daily"},
        },
        "required": ["weights", "covariance_matrix"],
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


def portfolio_volatility_calculator(
    weights: list[float],
    covariance_matrix: list[list[float]],
    period_label: str = "daily",
    **_: Any,
) -> dict[str, Any]:
    """Return variance, volatility, and contribution breakdown."""
    try:
        if not weights:
            raise ValueError("weights must not be empty")
        n_assets = len(weights)
        if any(len(row) != n_assets for row in covariance_matrix):
            raise ValueError("covariance matrix must be square and match weights length")
        total_weight = sum(weights)
        normalized = [w / total_weight if total_weight else 0.0 for w in weights]
        variance = 0.0
        marginal_risk: list[float] = [0.0 for _ in range(n_assets)]
        for i in range(n_assets):
            for j in range(n_assets):
                contribution = normalized[i] * normalized[j] * covariance_matrix[i][j]
                variance += contribution
        if variance < 0:
            variance = 0.0
        volatility = math.sqrt(variance)
        if volatility > 0:
            for i in range(n_assets):
                marginal = 0.0
                for j in range(n_assets):
                    marginal += covariance_matrix[i][j] * normalized[j]
                marginal_risk[i] = normalized[i] * marginal / volatility
        else:
            marginal_risk = [0.0 for _ in normalized]
        data = {
            "period_label": period_label,
            "portfolio_variance": round(variance, 8),
            "portfolio_volatility_pct": round(volatility * 100, 4),
            "normalized_weights": [round(w, 6) for w in normalized],
            "risk_contributions": [round(value, 6) for value in marginal_risk],
        }
        return {"status": "ok", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        try:
            with open("logs/lessons.md", "a") as _f:
                _f.write(f"- [{datetime.now(timezone.utc).isoformat()}] portfolio_volatility_calculator: {exc}\n")
        except OSError:
            pass
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
