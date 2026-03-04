"""
Execuve Summary: Ranks assets by momentum across multiple lookback periods.
Inputs: assets (dict[str, list[float]]), lookback_periods (list[int])
Outputs: composite_rank (list[tuple[str, float]]), rank_per_period (dict), top_quintile (list[str]), bottom_quintile (list[str])
MCP Tool Name: relative_strength_ranker
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "relative_strength_ranker",
    "description": "Computes total returns over multiple lookbacks and ranks assets by composite score.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "assets": {"type": "object", "description": "Mapping of asset name to price series."},
            "lookback_periods": {"type": "array", "description": "List of lookback windows (in bars)."}
        },
        "required": ["assets", "lookback_periods"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def relative_strength_ranker(**kwargs: Any) -> dict:
    """Ranks assets using momentum scores across user-defined periods."""
    try:
        assets = kwargs.get("assets")
        periods = kwargs.get("lookback_periods")
        if not isinstance(assets, dict) or not assets:
            raise ValueError("assets must be non-empty dict")
        if not isinstance(periods, list) or not periods:
            raise ValueError("lookback_periods must be non-empty list")
        for period in periods:
            if not isinstance(period, int) or period <= 0:
                raise ValueError("lookback periods must be positive integers")

        rank_per_period: dict[str, dict[str, float]] = {}
        composite_scores = {}
        for period in periods:
            period_scores = {}
            for name, prices in assets.items():
                if not isinstance(prices, list) or len(prices) < period + 1:
                    continue
                start_price = prices[-period - 1]
                end_price = prices[-1]
                if start_price == 0:
                    continue
                total_return = end_price / start_price - 1
                period_scores[name] = total_return
            sorted_assets = sorted(period_scores.items(), key=lambda item: item[1], reverse=True)
            rank_per_period[str(period)] = {name: score for name, score in sorted_assets}
            for rank, (name, score) in enumerate(sorted_assets):
                composite_scores.setdefault(name, 0)
                composite_scores[name] += (len(sorted_assets) - rank)

        composite_rank = sorted(composite_scores.items(), key=lambda item: item[1], reverse=True)
        quintile_size = max(1, len(composite_rank) // 5)
        top_quintile = [name for name, _ in composite_rank[:quintile_size]]
        bottom_quintile = [name for name, _ in composite_rank[-quintile_size:]]

        return {
            "status": "success",
            "data": {
                "composite_rank": composite_rank,
                "rank_per_period": rank_per_period,
                "top_quintile": top_quintile,
                "bottom_quintile": bottom_quintile
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"relative_strength_ranker failed: {e}")
        _log_lesson(f"relative_strength_ranker: {e}")
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
