"""
Executive Smary: Compares continuous compounding results against discrete schedules.
Inputs: principal (float), annual_rate (float), years (float)
Outputs: future_value (float), vs_annual_compounding (float), vs_monthly_compounding (float), marginal_benefit (float)
MCP Tool Name: continuous_compounding_calculator
"""
import logging
from datetime import datetime, timezone
from math import e
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "continuous_compounding_calculator",
    "description": (
        "Applies Pe^rt to compute the continuously compounded future value and compares "
        "it to annual and monthly compounding scenarios."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "principal": {
                "type": "number",
                "description": "Initial dollars invested, must be positive.",
            },
            "annual_rate": {
                "type": "number",
                "description": "Annual growth rate as decimal.",
            },
            "years": {
                "type": "number",
                "description": "Holding period in years.",
            },
        },
        "required": ["principal", "annual_rate", "years"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"},
        },
        "required": ["status", "timestamp"],
    },
}


def continuous_compounding_calculator(**kwargs: Any) -> dict:
    """Compute continuous compounding and difference versus discrete compounding."""
    try:
        principal = float(kwargs["principal"])
        annual_rate = float(kwargs["annual_rate"])
        years = float(kwargs["years"])

        if principal <= 0:
            raise ValueError("principal must be positive")
        if years < 0:
            raise ValueError("years must be non-negative")

        future_value = principal * (e ** (annual_rate * years))
        annual_compounding = principal * (1 + annual_rate) ** years
        monthly_compounding = principal * (1 + annual_rate / 12) ** (12 * years)
        marginal_benefit = future_value - monthly_compounding

        return {
            "status": "success",
            "data": {
                "future_value": future_value,
                "vs_annual_compounding": future_value - annual_compounding,
                "vs_monthly_compounding": future_value - monthly_compounding,
                "marginal_benefit": marginal_benefit,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as exc:
        logger.error(f"continuous_compounding_calculator failed: {exc}")
        _log_lesson(f"continuous_compounding_calculator: {exc}")
        return {
            "status": "error",
            "error": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
