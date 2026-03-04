"""
Executive Summary: G-SIB indicator scoring to determine systemic importance bucket and surcharge.
Inputs: indicators (list[dict]), bucket_thresholds (list[dict])
Outputs: gsib_score (float), bucket (int), surcharge_rate (float)
MCP Tool Name: gsib_score_calculator
"""
import logging
from datetime import datetime, timezone
from typing import Any, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "gsib_score_calculator",
    "description": "Computes Basel systemic importance score using indicator values and denominators.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "indicators": {
                "type": "array",
                "description": "Indicator metrics with denominators and weights.",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Indicator name"},
                        "value": {"type": "number", "description": "Bank amount"},
                        "denominator": {"type": "number", "description": "Global denominator"},
                        "weight_pct": {"type": "number", "description": "Indicator weight %"},
                    },
                    "required": ["name", "value", "denominator", "weight_pct"],
                },
            },
            "bucket_thresholds": {
                "type": "array",
                "description": "List of score thresholds with surcharges.",
                "items": {
                    "type": "object",
                    "properties": {
                        "bucket": {"type": "integer", "description": "Bucket number"},
                        "score_threshold": {"type": "number", "description": "Score threshold in bps"},
                        "surcharge_pct": {"type": "number", "description": "Capital surcharge %"},
                    },
                    "required": ["bucket", "score_threshold", "surcharge_pct"],
                },
            },
        },
        "required": ["indicators", "bucket_thresholds"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "G-SIB score outputs"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def gsib_score_calculator(
    indicators: List[dict[str, Any]],
    bucket_thresholds: List[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    try:
        score = 0.0
        indicator_scores = []
        for indicator in indicators:
            ratio = (indicator["value"] / indicator["denominator"]) if indicator["denominator"] else 0.0
            indicator_score = ratio * 10000  # convert to basis points
            weighted = indicator_score * (indicator["weight_pct"] / 100.0)
            score += weighted
            indicator_scores.append({"name": indicator["name"], "score_bps": round(indicator_score, 2), "weighted_bps": round(weighted, 2)})
        bucket_thresholds_sorted = sorted(bucket_thresholds, key=lambda x: x["score_threshold"])
        bucket = bucket_thresholds_sorted[-1]["bucket"]
        surcharge = bucket_thresholds_sorted[-1]["surcharge_pct"]
        for entry in bucket_thresholds_sorted:
            if score <= entry["score_threshold"]:
                bucket = entry["bucket"]
                surcharge = entry["surcharge_pct"]
                break
        data = {
            "gsib_score_bps": round(score, 2),
            "bucket": bucket,
            "surcharge_rate_pct": surcharge,
            "indicator_scores": indicator_scores,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"gsib_score_calculator failed: {e}")
        _log_lesson(f"gsib_score_calculator: {e}")
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
