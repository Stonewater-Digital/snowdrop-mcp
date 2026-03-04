"""
Executive Summary: Estimates recovery rates by seniority using weighted historical observations.
Inputs: seniority_levels (list[str]), historical_recoveries (list[float])
Outputs: status (str), timestamp (str), data (dict)
MCP Tool Name: recovery_rate_estimator
"""
import logging
import statistics
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "recovery_rate_estimator",
    "description": "Computes seniority-specific recovery estimates using historical averages and dispersion statistics.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "seniority_levels": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of instrument seniority labels (e.g., 'Sr Secured', 'Unsecured')."
            },
            "historical_recoveries": {
                "type": "array",
                "items": {"type": "number"},
                "description": "Historical recovery realizations in decimal form."
            }
        },
        "required": ["seniority_levels", "historical_recoveries"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"}
        },
        "required": ["status", "timestamp"]
    }
}


def recovery_rate_estimator(**kwargs: Any) -> dict[str, Any]:
    try:
        levels = _clean_levels(kwargs["seniority_levels"])
        recoveries = _clean_recoveries(kwargs["historical_recoveries"])
        if len(levels) != len(recoveries):
            raise ValueError("seniority_levels and historical_recoveries must align")

        grouped: dict[str, list[float]] = defaultdict(list)
        for lvl, rec in zip(levels, recoveries):
            grouped[lvl].append(rec)

        summary: dict[str, Any] = {}
        for lvl, values in grouped.items():
            mean_rec = statistics.fmean(values)
            volatility = statistics.pstdev(values) if len(values) > 1 else 0.0
            percentile_low = sorted(values)[max(0, int(0.1 * len(values)) - 1)]
            percentile_high = sorted(values)[min(len(values) - 1, int(0.9 * len(values)))]
            summary[lvl] = {
                "mean_recovery": mean_rec,
                "volatility": volatility,
                "p10": percentile_low,
                "p90": percentile_high,
                "observations": len(values)
            }

        blended = statistics.fmean(recoveries)
        data = {
            "seniority_estimates": summary,
            "portfolio_average_recovery": blended,
            "observation_count": len(recoveries)
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError, KeyError) as e:
        logger.error("recovery_rate_estimator failed: %s", e)
        _log_lesson(f"recovery_rate_estimator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _clean_levels(values: Sequence[Any]) -> list[str]:
    if not values:
        raise ValueError("seniority_levels must be non-empty")
    return [str(v).strip() for v in values]


def _clean_recoveries(values: Sequence[Any]) -> list[float]:
    if not values:
        raise ValueError("historical_recoveries must be non-empty")
    cleaned = []
    for val in values:
        rec = float(val)
        if not 0.0 <= rec <= 1.0:
            raise ValueError("recoveries must lie in [0,1]")
        cleaned.append(rec)
    return cleaned


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as file:
            file.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
