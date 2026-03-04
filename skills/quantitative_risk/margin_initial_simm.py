"""
Executive Summary: ISDA SIMM initial margin calculator using risk-class sensitivities and concentration thresholds.
Inputs: sensitivities (list[dict]), concentration_thresholds (dict[str,float])
Outputs: simm_im (float), risk_class_margin (dict), concentration_addons (dict)
MCP Tool Name: margin_initial_simm
"""
import logging
from datetime import datetime, timezone
from math import sqrt
from typing import Any, Dict, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "margin_initial_simm",
    "description": "Approximates ISDA SIMM initial margin by aggregating weighted sensitivities per risk class.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "sensitivities": {
                "type": "array",
                "description": "List of sensitivities (delta/vega) per risk class bucket.",
                "items": {
                    "type": "object",
                    "properties": {
                        "risk_class": {"type": "string", "description": "IR, FX, Credit, Equity, Commodity"},
                        "bucket": {"type": "string", "description": "SIMM bucket identifier"},
                        "amount": {"type": "number", "description": "Weighted sensitivity amount"},
                    },
                    "required": ["risk_class", "bucket", "amount"],
                },
            },
            "concentration_thresholds": {
                "type": "object",
                "description": "Threshold per risk class for concentration add-on.",
                "additionalProperties": {
                    "type": "number",
                    "description": "Threshold amount",
                },
            },
            "correlation": {
                "type": "number",
                "description": "Assumed correlation across buckets (default 0.5).",
                "default": 0.5,
            },
        },
        "required": ["sensitivities"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "SIMM output"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def margin_initial_simm(
    sensitivities: List[Dict[str, Any]],
    concentration_thresholds: Dict[str, float] | None = None,
    correlation: float = 0.5,
    **_: Any,
) -> dict[str, Any]:
    try:
        if not sensitivities:
            raise ValueError("sensitivities required")
        concentrations = concentration_thresholds or {}
        risk_buckets: Dict[str, List[float]] = {}
        for entry in sensitivities:
            risk_buckets.setdefault(entry["risk_class"], []).append(entry["amount"])
        risk_margins = {}
        concentration_addons = {}
        total_im = 0.0
        corr = max(min(correlation, 0.99), -0.99)
        for risk_class, bucket_amounts in risk_buckets.items():
            sum_sq = sum(amount ** 2 for amount in bucket_amounts)
            cross = 0.0
            for i in range(len(bucket_amounts)):
                for j in range(i + 1, len(bucket_amounts)):
                    cross += 2 * corr * bucket_amounts[i] * bucket_amounts[j]
            base_margin = sqrt(max(sum_sq + cross, 0.0))
            threshold = concentrations.get(risk_class, float("inf"))
            concentration = max(base_margin / threshold, 1.0) if threshold != float("inf") else 1.0
            margin = base_margin * concentration
            risk_margins[risk_class] = round(margin, 2)
            concentration_addons[risk_class] = round(margin - base_margin, 2)
            total_im += margin
        data = {
            "simm_im": round(total_im, 2),
            "risk_class_margin": risk_margins,
            "concentration_addons": concentration_addons,
            "assumed_correlation": corr,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"margin_initial_simm failed: {e}")
        _log_lesson(f"margin_initial_simm: {e}")
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
