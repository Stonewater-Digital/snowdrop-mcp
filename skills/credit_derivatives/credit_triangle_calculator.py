"""
Executive Summary: Links CDS spread, default probability, and recovery using the credit triangle identity.
Inputs: spread_bp (float), hazard_rate (float), recovery_rate (float), tenor_years (float)
Outputs: status (str), timestamp (str), data (dict)
MCP Tool Name: credit_triangle_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "credit_triangle_calculator",
    "description": (
        "Applies the credit triangle (spread ≈ hazard × (1 − recovery)) to reconcile CDS quotes "
        "with implied hazard and loss metrics for a given tenor."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "spread_bp": {
                "type": "number",
                "description": "Observed CDS spread in basis points."
            },
            "hazard_rate": {
                "type": "number",
                "description": "Annualized hazard rate estimate (decimal)."
            },
            "recovery_rate": {
                "type": "number",
                "description": "Recovery assumption in decimal form (0-1)."
            },
            "tenor_years": {
                "type": "number",
                "description": "Tenor used to convert hazard rate into cumulative probability."
            }
        },
        "required": ["spread_bp", "hazard_rate", "recovery_rate", "tenor_years"]
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


def credit_triangle_calculator(**kwargs: Any) -> dict[str, Any]:
    try:
        spread_bp = float(kwargs["spread_bp"])
        hazard_rate = float(kwargs["hazard_rate"])
        recovery = float(kwargs["recovery_rate"])
        tenor = float(kwargs["tenor_years"])
        if not 0.0 <= recovery < 1.0:
            raise ValueError("recovery_rate must be in [0,1)")
        if tenor <= 0:
            raise ValueError("tenor_years must be positive")

        implied_spread_bp = hazard_rate * (1 - recovery) * 10000.0
        implied_hazard = spread_bp / 10000.0 / max(1 - recovery, 1e-8)
        cumulative_pd = 1 - math.exp(-hazard_rate * tenor)
        implied_pd = 1 - math.exp(-implied_hazard * tenor)
        mispricing_bp = spread_bp - implied_spread_bp

        data = {
            "input_spread_bp": spread_bp,
            "hazard_rate": hazard_rate,
            "implied_spread_bp": implied_spread_bp,
            "implied_hazard_rate": implied_hazard,
            "cumulative_default_probability": cumulative_pd,
            "implied_default_probability": implied_pd,
            "mispricing_bp": mispricing_bp
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError, KeyError) as e:
        logger.error("credit_triangle_calculator failed: %s", e)
        _log_lesson(f"credit_triangle_calculator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as file:
            file.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
