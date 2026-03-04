"""
Executive Summary: Drawdown-constrained optimizer searching for allocations with maximum expected return subject to peak-to-trough cap.
Inputs: asset_paths (dict[str, list[float]]), drawdown_limit (float), simulations (int)
Outputs: optimal_weights (list[dict]), max_drawdown_pct (float), expected_return (float), path_statistics (dict)
MCP Tool Name: drawdown_constrained_optimizer
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

import numpy as np

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "drawdown_constrained_optimizer",
    "description": (
        "Performs scenario search across asset paths to maximize expected return while enforcing a user-specified "
        "maximum drawdown limit consistent with UCITS risk budgeting guidance."),
    "inputSchema": {
        "type": "object",
        "properties": {
            "asset_paths": {
                "type": "object",
                "description": "Dictionary mapping asset to a path of periodic returns (decimal).",
                "additionalProperties": {
                    "type": "array",
                    "items": {"type": "number"},
                },
            },
            "drawdown_limit": {
                "type": "number",
                "description": "Maximum allowable drawdown in decimal terms (e.g., 0.2 for 20%).",
            },
            "simulations": {
                "type": "integer",
                "description": "Number of random weight draws for search (default 2000).",
            },
            "seed": {
                "type": "integer",
                "description": "Random seed for reproducibility.",
            },
        },
        "required": ["asset_paths", "drawdown_limit"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "Execution status"},
            "data": {"type": "object", "description": "Optimal allocation summary"},
            "timestamp": {"type": "string", "description": "UTC timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def _max_drawdown(series: np.ndarray) -> float:
    cumulative = (1 + series).cumprod()
    running_max = np.maximum.accumulate(cumulative)
    drawdowns = 1 - cumulative / running_max
    return float(np.max(drawdowns))


def drawdown_constrained_optimizer(
    asset_paths: Dict[str, List[float]],
    drawdown_limit: float,
    simulations: int = 2000,
    seed: int | None = 17,
    **_: Any,
) -> dict[str, Any]:
    try:
        if drawdown_limit <= 0 or drawdown_limit >= 1:
            raise ValueError("drawdown_limit must be between 0 and 1")
        if len(asset_paths) < 2:
            raise ValueError("Provide at least two assets")
        lengths = {len(path) for path in asset_paths.values()}
        if len(lengths) != 1:
            raise ValueError("All asset paths must have equal length")
        matrix = np.array(list(asset_paths.values()), dtype=float)
        n_assets, horizon = matrix.shape
        rng = np.random.default_rng(seed)
        best_return = -np.inf
        best_weights = None
        best_drawdown = None
        accepted = 0
        stats = []
        for _ in range(simulations):
            candidate = rng.dirichlet(np.ones(n_assets))
            portfolio_path = (candidate @ matrix)
            drawdown = _max_drawdown(portfolio_path)
            if drawdown <= drawdown_limit:
                mean_return = float(np.mean(portfolio_path))
                accepted += 1
                stats.append({"return": mean_return, "max_drawdown": drawdown})
                if mean_return > best_return:
                    best_return = mean_return
                    best_weights = candidate
                    best_drawdown = drawdown
        if best_weights is None:
            raise ValueError("No feasible portfolio met the drawdown constraint")
        weights_output = [
            {"asset": asset, "weight": round(weight, 6)}
            for asset, weight in zip(asset_paths.keys(), best_weights)
        ]
        data = {
            "optimal_weights": weights_output,
            "expected_return": round(best_return, 6),
            "max_drawdown_pct": round(best_drawdown * 100, 4),
            "accepted_portfolios": accepted,
            "path_statistics": stats[-10:],
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError) as e:
        logger.error(f"drawdown_constrained_optimizer failed: {e}")
        _log_lesson(f"drawdown_constrained_optimizer: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as handle:
            handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
