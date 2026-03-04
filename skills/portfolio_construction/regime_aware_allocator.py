"""
Executive Summary: Regime-aware allocator using a two-state hidden Markov filter to toggle portfolios across macro regimes.
Inputs: return_series (list[float]), regime_allocations (dict), transition_matrix (list[list[float]]), observation_vol (float)
Outputs: current_regime (str), regime_probabilities (dict), recommended_weights (list[dict]), forward_return_estimate (float)
MCP Tool Name: regime_aware_allocator
"""
import logging
from datetime import datetime, timezone
from math import exp, pi, sqrt
from typing import Any, Dict, List

import numpy as np

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "regime_aware_allocator",
    "description": (
        "Fits a two-state hidden Markov model to realized returns and allocates according to risk-on/risk-off "
        "regime targets similar to Norges Bank's conditional allocation process."),
    "inputSchema": {
        "type": "object",
        "properties": {
            "return_series": {
                "type": "array",
                "description": "Chronological list of realized portfolio returns (decimal).",
                "items": {"type": "number"},
            },
            "regime_allocations": {
                "type": "object",
                "description": "Mapping of regime label to asset weight dictionary.",
                "additionalProperties": {
                    "type": "object",
                    "additionalProperties": {"type": "number"},
                },
            },
            "transition_matrix": {
                "type": "array",
                "description": "2x2 Markov transition matrix [[p00,p01],[p10,p11]].",
                "items": {
                    "type": "array",
                    "items": {"type": "number"},
                },
            },
            "observation_vol": {
                "type": "number",
                "description": "Scaling parameter for observation noise (default estimated from data).",
            },
        },
        "required": ["return_series", "regime_allocations"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "Execution status"},
            "data": {"type": "object", "description": "Regime allocation output"},
            "timestamp": {"type": "string", "description": "UTC timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def _gaussian_pdf(value: float, mean: float, std: float) -> float:
    return exp(-0.5 * ((value - mean) / std) ** 2) / (std * sqrt(2 * pi))


def regime_aware_allocator(
    return_series: List[float],
    regime_allocations: Dict[str, Dict[str, float]],
    transition_matrix: List[List[float]] | None = None,
    observation_vol: float | None = None,
    **_: Any,
) -> dict[str, Any]:
    try:
        returns = np.asarray(return_series, dtype=float)
        if returns.size < 12:
            raise ValueError("return_series must have at least 12 observations")
        regimes = sorted(regime_allocations.keys())
        if len(regimes) < 2:
            raise ValueError("Provide at least two regime allocation dictionaries")
        if transition_matrix is None:
            transition_matrix = [[0.9, 0.1], [0.2, 0.8]]
        trans = np.asarray(transition_matrix, dtype=float)
        if trans.shape != (2, 2):
            raise ValueError("transition_matrix must be 2x2")
        if observation_vol is None:
            observation_vol = float(np.std(returns[-60:])) or 0.02
        high_mean = float(np.mean(returns[-60:]))
        low_mean = float(np.percentile(returns, 20))
        std_high = max(observation_vol / 2, 1e-4)
        std_low = max(observation_vol * 1.5, 1e-4)
        posterior = np.array([0.5, 0.5])
        for r in returns:
            likelihood = np.array([
                _gaussian_pdf(r, low_mean, std_low),
                _gaussian_pdf(r, high_mean, std_high),
            ])
            prior = trans.T @ posterior
            posterior = prior * likelihood
            if posterior.sum() == 0:
                posterior = np.array([0.5, 0.5])
            else:
                posterior /= posterior.sum()
        risk_off_prob, risk_on_prob = posterior
        transitional_prob = max(0.0, 1 - (risk_off_prob + risk_on_prob))
        probabilities = {
            "risk_off": round(float(risk_off_prob), 4),
            "risk_on": round(float(risk_on_prob), 4),
            "transitional": round(float(transitional_prob), 4),
        }
        if risk_on_prob > 0.6:
            regime = "risk_on"
        elif risk_off_prob > 0.6:
            regime = "risk_off"
        else:
            regime = "transitional"
        allocation_template = regime_allocations.get(regime) or regime_allocations[regimes[0]]
        weights = []
        for asset, weight in allocation_template.items():
            weights.append({"asset": asset, "weight": round(weight, 4)})
        forward_return = risk_on_prob * high_mean + risk_off_prob * low_mean
        data = {
            "current_regime": regime,
            "regime_probabilities": probabilities,
            "recommended_weights": weights,
            "forward_return_estimate": round(float(forward_return), 6),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"regime_aware_allocator failed: {e}")
        _log_lesson(f"regime_aware_allocator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as file:
            file.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
