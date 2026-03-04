"""
Executive Summary: IFRS 17 risk adjustment via confidence level technique using claim distribution inputs.
Inputs: claim_distribution (list[float]), confidence_level (float), coefficient_of_variation_pct (float)
Outputs: risk_adjustment (float), equivalent_confidence_level_pct (float)
MCP Tool Name: ifrs17_risk_adjustment
"""
import logging
from datetime import datetime, timezone
from statistics import NormalDist
from typing import Any, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "ifrs17_risk_adjustment",
    "description": "Computes risk adjustment as VaR minus expected loss using the confidence level technique.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "claim_distribution": {
                "type": "array",
                "description": "Simulated claim amounts or scenario losses.",
                "items": {"type": "number"},
            },
            "confidence_level": {"type": "number", "description": "Target confidence level (e.g., 0.75)."},
            "coefficient_of_variation_pct": {"type": "number", "description": "Coefficient of variation per risk type."},
        },
        "required": ["claim_distribution", "confidence_level", "coefficient_of_variation_pct"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "Risk adjustment output"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def ifrs17_risk_adjustment(
    claim_distribution: List[float],
    confidence_level: float,
    coefficient_of_variation_pct: float,
    **_: Any,
) -> dict[str, Any]:
    try:
        if not claim_distribution:
            raise ValueError("claim_distribution required")
        sorted_losses = sorted(claim_distribution)
        idx = min(max(int(confidence_level * len(sorted_losses)) - 1, 0), len(sorted_losses) - 1)
        var = sorted_losses[idx]
        expected_loss = sum(claim_distribution) / len(claim_distribution)
        risk_adjustment = var - expected_loss
        # Equivalent CL using normal approximation
        cov = coefficient_of_variation_pct / 100.0
        std_dev = expected_loss * cov
        equivalent_cl = NormalDist().cdf(risk_adjustment / std_dev) if std_dev > 0 else confidence_level
        data = {
            "risk_adjustment": round(max(risk_adjustment, 0.0), 2),
            "expected_loss": round(expected_loss, 2),
            "var": round(var, 2),
            "equivalent_confidence_level_pct": round(equivalent_cl * 100, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"ifrs17_risk_adjustment failed: {e}")
        _log_lesson(f"ifrs17_risk_adjustment: {e}")
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
