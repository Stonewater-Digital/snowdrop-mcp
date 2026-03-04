"""
Executive Summary: Model risk validation pack computing AUROC, Gini, KS, and PSI metrics compared to a benchmark.
Inputs: model_predictions (list[float]), actuals (list[int]), benchmark_predictions (list[float])
Outputs: gini (float), auroc (float), ks_statistic (float), psi (float)
MCP Tool Name: model_risk_validator
"""
import logging
from datetime import datetime, timezone
from math import log
from typing import Any, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "model_risk_validator",
    "description": "Computes discrimination and stability metrics for regulatory model validation.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "model_predictions": {
                "type": "array",
                "description": "Model PD or score outputs.",
                "items": {"type": "number"},
            },
            "actuals": {
                "type": "array",
                "description": "Observed outcomes (1=default).",
                "items": {"type": "number"},
            },
            "benchmark_predictions": {
                "type": "array",
                "description": "Benchmark or prior-period predictions for PSI.",
                "items": {"type": "number"},
            },
            "num_bins": {
                "type": "integer",
                "description": "Number of bins for PSI calculation (default 10).",
                "default": 10,
            },
        },
        "required": ["model_predictions", "actuals", "benchmark_predictions"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "Validation metrics"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def _auc(actuals: List[int], scores: List[float]) -> float:
    positives = sum(actuals)
    negatives = len(actuals) - positives
    if positives == 0 or negatives == 0:
        return 0.5
    # Rank sum method
    paired = list(zip(scores, actuals))
    paired.sort(key=lambda x: x[0])
    ranks = []
    i = 0
    while i < len(paired):
        j = i
        while j < len(paired) and paired[j][0] == paired[i][0]:
            j += 1
        avg_rank = (i + j + 1) / 2
        ranks.extend([avg_rank] * (j - i))
        i = j
    sum_ranks_positive = sum(rank for rank, (_, actual) in zip(ranks, paired) if actual == 1)
    auc = (sum_ranks_positive - positives * (positives + 1) / 2) / (positives * negatives)
    return max(min(auc, 1.0), 0.0)


def _ks(actuals: List[int], scores: List[float]) -> float:
    pairs = sorted(zip(scores, actuals), reverse=True)
    positives = sum(actuals)
    negatives = len(actuals) - positives
    cum_pos = cum_neg = 0.0
    ks = 0.0
    for _, actual in pairs:
        if actual == 1 and positives:
            cum_pos += 1 / positives
        elif negatives:
            cum_neg += 1 / negatives
        ks = max(ks, abs(cum_pos - cum_neg))
    return ks


def _psi(expected: List[float], actual: List[float], bins: int) -> float:
    if bins <= 0:
        raise ValueError("num_bins must be positive")
    combined = expected + actual
    if not combined:
        return 0.0
    minimum, maximum = min(combined), max(combined)
    if minimum == maximum:
        return 0.0
    edges = [minimum + i * (maximum - minimum) / bins for i in range(bins + 1)]
    psi = 0.0
    for i in range(bins):
        lower, upper = edges[i], edges[i + 1]
        exp_count = sum(1 for val in expected if lower <= val <= upper)
        act_count = sum(1 for val in actual if lower <= val <= upper)
        exp_pct = exp_count / len(expected) if expected else 0.0
        act_pct = act_count / len(actual) if actual else 0.0
        exp_pct = exp_pct or 1e-6
        act_pct = act_pct or 1e-6
        psi += (act_pct - exp_pct) * log(act_pct / exp_pct)
    return psi


def model_risk_validator(
    model_predictions: List[float],
    actuals: List[int],
    benchmark_predictions: List[float],
    num_bins: int = 10,
    **_: Any,
) -> dict[str, Any]:
    try:
        if not (len(model_predictions) == len(actuals)):
            raise ValueError("model_predictions and actuals must align")
        if not benchmark_predictions:
            raise ValueError("benchmark_predictions required")
        auc = _auc(actuals, model_predictions)
        gini = 2 * auc - 1
        ks = _ks(actuals, model_predictions)
        psi = _psi(benchmark_predictions, model_predictions, num_bins)
        data = {
            "gini": round(gini, 4),
            "auroc": round(auc, 4),
            "ks_statistic": round(ks, 4),
            "psi": round(psi, 4),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"model_risk_validator failed: {e}")
        _log_lesson(f"model_risk_validator: {e}")
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
