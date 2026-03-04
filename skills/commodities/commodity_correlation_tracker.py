"""Track correlations among commodity contracts."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "commodity_correlation_tracker",
    "description": (
        "Computes pairwise Pearson correlations across commodity return series, "
        "identifies highest and lowest correlated pairs, and reports diversification score."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "returns_by_contract": {
                "type": "object",
                "description": "Mapping of commodity name to its return series (decimal, same length).",
                "additionalProperties": {
                    "type": "array",
                    "items": {"type": "number"},
                },
            }
        },
        "required": ["returns_by_contract"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "correlations": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "pair": {"type": "array", "items": {"type": "string"}},
                        "correlation": {"type": "number"},
                    },
                },
            },
            "highest_correlation_pair": {"type": "object"},
            "lowest_correlation_pair": {"type": "object"},
            "avg_pairwise_correlation": {"type": "number"},
            "diversification_score": {"type": "number"},
            "timestamp": {"type": "string"},
        },
    },
}


def commodity_correlation_tracker(
    returns_by_contract: dict[str, list[float]],
    **_: Any,
) -> dict[str, Any]:
    """Return pairwise correlations and diversification metrics.

    Args:
        returns_by_contract: Dict mapping commodity names to return series.
            All series must have the same length (>= 3).

    Returns:
        dict with status, pairwise correlations (sorted descending), highest and
        lowest correlated pairs, average pairwise correlation, and diversification_score.

    Pearson correlation:
        ρ(a, b) = Cov(a, b) / (σ_a * σ_b)
        Using population formula consistent across pairs.

    Diversification score:
        1 - avg_pairwise_correlation
        Higher score = better diversification across commodities.
    """
    try:
        contracts = list(returns_by_contract.keys())
        if len(contracts) < 2:
            raise ValueError("Need at least 2 contracts for correlation")
        lengths = {len(series) for series in returns_by_contract.values()}
        if len(lengths) != 1:
            raise ValueError("All return series must have the same length")
        length = lengths.pop()
        if length < 3:
            raise ValueError("Return series must have at least 3 observations")

        normalized: dict[str, list[float]] = {
            name: [float(x) for x in returns_by_contract[name]] for name in contracts
        }
        means = {name: sum(series) / length for name, series in normalized.items()}
        # Population std dev for each series
        stdevs = {
            name: math.sqrt(sum((x - means[name]) ** 2 for x in series) / length)
            for name, series in normalized.items()
        }

        correlations = []
        for i, a in enumerate(contracts):
            for b in contracts[i + 1:]:
                cov = sum(
                    (normalized[a][k] - means[a]) * (normalized[b][k] - means[b])
                    for k in range(length)
                ) / length
                denom = stdevs[a] * stdevs[b]
                corr = cov / denom if denom > 1e-12 else 0.0
                # Clamp to [-1, 1] due to floating point
                corr = max(-1.0, min(1.0, corr))
                correlations.append({"pair": [a, b], "correlation": round(corr, 4)})

        # Sort by correlation descending
        correlations.sort(key=lambda item: item["correlation"], reverse=True)
        highest = correlations[0]
        lowest = correlations[-1]
        avg_corr = sum(item["correlation"] for item in correlations) / len(correlations)
        diversification_score = 1.0 - avg_corr

        return {
            "status": "success",
            "correlations": correlations,
            "highest_correlation_pair": highest,
            "lowest_correlation_pair": lowest,
            "avg_pairwise_correlation": round(avg_corr, 4),
            "diversification_score": round(diversification_score, 4),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("commodity_correlation_tracker", str(exc))
        return {
            "status": "error",
            "error": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
