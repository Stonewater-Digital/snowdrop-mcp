"""
Executive Summary: Solvency II SCR aggregation using risk module SCRs and correlation matrix.
Inputs: risk_modules (list[dict]), correlation_matrix (dict[str,dict[str,float]])
Outputs: scr_by_module (dict), diversification_benefit (float), total_scr (float), solvency_ratio (float)
MCP Tool Name: solvency_ii_scr
"""
import logging
from datetime import datetime, timezone
from math import sqrt
from typing import Any, Dict, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "solvency_ii_scr",
    "description": "Aggregates market, counterparty, life, health, and non-life SCRs with standard correlations.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "risk_modules": {
                "type": "array",
                "description": "SCR per risk module in base currency.",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Risk module name"},
                        "scr": {"type": "number", "description": "SCR amount"},
                    },
                    "required": ["name", "scr"],
                },
            },
            "correlation_matrix": {
                "type": "object",
                "description": "Correlation coefficients keyed by risk module name.",
                "additionalProperties": {
                    "type": "object",
                    "additionalProperties": {"type": "number", "description": "Correlation"},
                },
            },
            "own_funds": {
                "type": "number",
                "description": "Available own funds for solvency ratio.",
                "default": 0.0,
            },
        },
        "required": ["risk_modules", "correlation_matrix"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "SCR outputs"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def solvency_ii_scr(
    risk_modules: List[Dict[str, Any]],
    correlation_matrix: Dict[str, Dict[str, float]],
    own_funds: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    try:
        names = [module["name"] for module in risk_modules]
        scr_values = {module["name"]: module["scr"] for module in risk_modules}
        total_variance = 0.0
        for i, name_i in enumerate(names):
            for j, name_j in enumerate(names):
                corr = correlation_matrix.get(name_i, {}).get(name_j, 1.0 if i == j else 0.0)
                total_variance += scr_values[name_i] * scr_values[name_j] * corr
        total_scr = sqrt(max(total_variance, 0.0))
        sum_of_modules = sum(scr_values.values())
        diversification = sum_of_modules - total_scr
        solvency_ratio = own_funds / total_scr if total_scr else 0.0
        data = {
            "scr_by_module": {k: round(v, 2) for k, v in scr_values.items()},
            "total_scr": round(total_scr, 2),
            "diversification_benefit": round(diversification, 2),
            "solvency_ratio": round(solvency_ratio * 100, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"solvency_ii_scr failed: {e}")
        _log_lesson(f"solvency_ii_scr: {e}")
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
