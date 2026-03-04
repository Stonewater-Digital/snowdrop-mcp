"""
Executive Summary: Standardized Measurement Approach for operational risk per Basel III, combining Business Indicator Component and Loss Component.
Inputs: business_indicator_components (dict), ilm_scaling_factors (dict), internal_loss_history (list[float])
Outputs: sma_capital (float), business_indicator (float), bic (float), ilm (float)
MCP Tool Name: operational_risk_sma
"""
import logging
from datetime import datetime, timezone
from math import log
from typing import Any, Dict, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "operational_risk_sma",
    "description": "Calculates SMA capital = BIC * ILM with Basel thresholds and loss component adjustments.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "business_indicator_components": {
                "type": "object",
                "description": "Values for interest, service, and financial components (ILDC, SC, FC).",
                "properties": {
                    "ildc": {"type": "number", "description": "Interest, leases, dividend component"},
                    "sc": {"type": "number", "description": "Services component"},
                    "fc": {"type": "number", "description": "Financial component"},
                },
                "required": ["ildc", "sc", "fc"],
            },
            "ilm_scaling_factors": {
                "type": "object",
                "description": "Optional tuning for ILM formula constants.",
                "properties": {
                    "lower_bound": {"type": "number", "description": "Minimum ILM", "default": 1.0},
                    "upper_bound": {"type": "number", "description": "Maximum ILM", "default": 1.5},
                },
            },
            "internal_loss_history": {
                "type": "array",
                "description": "Annual operational losses used for loss component (LC).",
                "items": {"type": "number"},
            },
        },
        "required": ["business_indicator_components", "internal_loss_history"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "SMA output"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def _bic(bi: float) -> float:
    first = min(bi, 1_000_000_000) * 0.12
    if bi <= 1_000_000_000:
        return first
    second = min(bi - 1_000_000_000, 29_000_000_000) * 0.15
    third = max(bi - 30_000_000_000, 0) * 0.18
    return 120_000_000 + second + third


def operational_risk_sma(
    business_indicator_components: Dict[str, float],
    internal_loss_history: List[float],
    ilm_scaling_factors: Dict[str, float] | None = None,
    **_: Any,
) -> dict[str, Any]:
    try:
        bi = sum(business_indicator_components.values())
        if bi <= 0:
            raise ValueError("business indicator must be positive")
        bic = _bic(bi)
        losses = [loss for loss in internal_loss_history if loss > 0]
        loss_component = (sum(losses) / len(losses)) * 15 if losses else 0.0
        ilm = 1.0
        if loss_component > 0 and bic > 0:
            ilm = max(1.0, min(1.5, 1 + log(loss_component / bic)))
        if ilm_scaling_factors:
            lower = ilm_scaling_factors.get("lower_bound", 1.0)
            upper = ilm_scaling_factors.get("upper_bound", 1.5)
            ilm = max(lower, min(ilm, upper))
        sma_capital = bic * ilm
        data = {
            "business_indicator": round(bi, 2),
            "bic": round(bic, 2),
            "loss_component": round(loss_component, 2),
            "ilm": round(ilm, 4),
            "sma_capital": round(sma_capital, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"operational_risk_sma failed: {e}")
        _log_lesson(f"operational_risk_sma: {e}")
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
