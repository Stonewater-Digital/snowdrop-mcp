"""
Execuve Summary: Builds a pairwise correlation matrix for multiple assets.
Inputs: return_series (dict[str, list[float]])
Outputs: correlation_matrix (dict), highest_correlation_pair (tuple), lowest_correlation_pair (tuple), average_correlation (float), diversification_score (float)
MCP Tool Name: correlation_matrix_builder
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "correlation_matrix_builder",
    "description": "Computes Pearson correlations across multiple return series to assess diversification.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "return_series": {"type": "object", "description": "Mapping of asset name to return list."}
        },
        "required": ["return_series"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def correlation_matrix_builder(**kwargs: Any) -> dict:
    """Generates pairwise correlation matrix and summary stats."""
    try:
        return_series = kwargs.get("return_series")
        if not isinstance(return_series, dict) or len(return_series) < 2:
            raise ValueError("return_series must be dict with at least two assets")

        assets = list(return_series.keys())
        length_set = {len(series) for series in return_series.values() if isinstance(series, list)}
        if len(length_set) != 1:
            raise ValueError("all return series must have equal length")
        length = length_set.pop()
        if length < 2:
            raise ValueError("return series must contain at least two observations")

        cleaned = {}
        for name, series in return_series.items():
            if not isinstance(series, list):
                raise ValueError("each asset must map to a list of returns")
            cleaned[name] = [float(val) for val in series]

        correlation_matrix = {name: {} for name in assets}
        highest_pair = None
        lowest_pair = None
        sum_corr = 0.0
        count = 0

        def _correlation(a: list[float], b: list[float]) -> float:
            mean_a = sum(a) / len(a)
            mean_b = sum(b) / len(b)
            numerator = sum((x - mean_a) * (y - mean_b) for x, y in zip(a, b))
            denom_a = math.sqrt(sum((x - mean_a) ** 2 for x in a))
            denom_b = math.sqrt(sum((y - mean_b) ** 2 for y in b))
            denominator = denom_a * denom_b
            if denominator == 0:
                return 0.0
            return numerator / denominator

        for i, asset_a in enumerate(assets):
            correlation_matrix[asset_a][asset_a] = 1.0
            for asset_b in assets[i + 1:]:
                corr = _correlation(cleaned[asset_a], cleaned[asset_b])
                correlation_matrix[asset_a][asset_b] = corr
                correlation_matrix[asset_b][asset_a] = corr
                pair = (asset_a, asset_b)
                if highest_pair is None or corr > highest_pair[2]:
                    highest_pair = (asset_a, asset_b, corr)
                if lowest_pair is None or corr < lowest_pair[2]:
                    lowest_pair = (asset_a, asset_b, corr)
                sum_corr += corr
                count += 1

        average_correlation = sum_corr / count if count else 0.0
        diversification_score = 1 - min(1, abs(average_correlation))

        return {
            "status": "success",
            "data": {
                "correlation_matrix": correlation_matrix,
                "highest_correlation_pair": highest_pair,
                "lowest_correlation_pair": lowest_pair,
                "average_correlation": average_correlation,
                "diversification_score": diversification_score
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"correlation_matrix_builder failed: {e}")
        _log_lesson(f"correlation_matrix_builder: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
