"""Produce heuristic optimized weights using return and risk forecasts."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable

TOOL_META: dict[str, Any] = {
    "name": "portfolio_optimization_tool",
    "description": "Builds heuristic mean-variance weights using return expectations and volatilities.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "assets": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "expected_return_pct": {"type": "number"},
                        "volatility_pct": {"type": "number", "description": "Must be > 0."},
                    },
                    "required": ["name", "expected_return_pct", "volatility_pct"],
                },
            },
            "risk_free_rate_pct": {"type": "number", "default": 0.0},
        },
        "required": ["assets"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "data": {
                "type": "object",
                "properties": {
                    "weights": {"type": "object"},
                    "expected_return_pct": {"type": "number"},
                    "approx_volatility_pct": {"type": "number"},
                    "sharpe_ratio": {"type": "number"},
                    "excluded_assets": {"type": "array", "items": {"type": "string"}},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def portfolio_optimization_tool(
    assets: Iterable[dict[str, Any]],
    risk_free_rate_pct: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Return heuristic tangency weights and portfolio stats.

    Weights are proportional to excess_return / vol^2 (Sharpe-maximising
    heuristic for uncorrelated assets). Only assets with positive excess
    return are included; assets with zero or negative excess return are
    excluded and reported separately.

    Args:
        assets: List of assets with name, expected_return_pct, volatility_pct.
        risk_free_rate_pct: Risk-free rate as a percentage.

    Returns:
        dict with weights, expected_return_pct, approx_volatility_pct,
        sharpe_ratio, excluded_assets.
    """
    try:
        asset_list = list(assets)
        if len(asset_list) < 2:
            raise ValueError("Need at least two assets")

        valid_scores: list[dict[str, Any]] = []
        excluded: list[str] = []

        for asset in asset_list:
            vol = float(asset["volatility_pct"])
            if vol <= 0:
                raise ValueError(f"volatility_pct must be positive for asset '{asset['name']}'")
            excess = float(asset["expected_return_pct"]) - risk_free_rate_pct
            if excess <= 0:
                # Cannot allocate positive weight to asset with non-positive excess return
                excluded.append(str(asset["name"]))
                continue
            score = excess / (vol ** 2)
            valid_scores.append({
                "name": str(asset["name"]),
                "score": score,
                "vol": vol,
                "expected": float(asset["expected_return_pct"]),
            })

        if not valid_scores:
            raise ValueError(
                "No assets have positive excess return over the risk-free rate; "
                "cannot construct a meaningful portfolio"
            )

        total_score = sum(item["score"] for item in valid_scores)
        weights = {item["name"]: item["score"] / total_score for item in valid_scores}

        # Weighted average return and vol (diagonal covariance approximation)
        portfolio_return = sum(
            weights[item["name"]] * item["expected"] for item in valid_scores
        )
        # Approximate portfolio vol: sqrt(sum(w_i^2 * sigma_i^2)) [no correlation]
        portfolio_var = sum(
            (weights[item["name"]] * item["vol"]) ** 2 for item in valid_scores
        )
        import math as _math
        portfolio_vol = _math.sqrt(portfolio_var) if portfolio_var > 0 else 0.0

        sharpe = (portfolio_return - risk_free_rate_pct) / portfolio_vol if portfolio_vol else 0.0

        data = {
            "weights": {name: round(weight, 4) for name, weight in weights.items()},
            "expected_return_pct": round(portfolio_return, 2),
            "approx_volatility_pct": round(portfolio_vol, 2),
            "sharpe_ratio": round(sharpe, 4),
            "excluded_assets": excluded,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson(f"portfolio_optimization_tool: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
