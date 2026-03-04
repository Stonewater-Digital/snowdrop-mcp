"""
Executive Smary: Computes real returns versus inflation for a multi-year investment.
Inputs: nominal_return (float), inflation_rate (float), years (float), initial_investment (float)
Outputs: real_return (float), nominal_fv (float), real_fv (float), purchasing_power_loss (float)
MCP Tool Name: inflation_adjusted_return
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "inflation_adjusted_return",
    "description": (
        "Calculates nominal versus real returns by discounting investment growth for "
        "inflation and highlighting purchasing power erosion."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "nominal_return": {
                "type": "number",
                "description": "Nominal annual return as decimal.",
            },
            "inflation_rate": {
                "type": "number",
                "description": "Annual inflation rate as decimal.",
            },
            "years": {
                "type": "number",
                "description": "Investment horizon in years.",
            },
            "initial_investment": {
                "type": "number",
                "description": "Starting principal in dollars, must be positive.",
            },
        },
        "required": ["nominal_return", "inflation_rate", "years", "initial_investment"],
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


def inflation_adjusted_return(**kwargs: Any) -> dict:
    """Convert nominal returns into real returns accounting for inflation."""
    try:
        nominal_return = float(kwargs["nominal_return"])
        inflation_rate = float(kwargs["inflation_rate"])
        years = float(kwargs["years"])
        initial_investment = float(kwargs["initial_investment"])

        if years < 0:
            raise ValueError("years must be non-negative")
        if initial_investment <= 0:
            raise ValueError("initial_investment must be positive")

        nominal_fv = initial_investment * (1 + nominal_return) ** years
        inflation_factor = (1 + inflation_rate) ** years
        real_fv = nominal_fv / inflation_factor
        real_return_rate = (real_fv / initial_investment) ** (1 / years) - 1 if years > 0 else 0
        purchasing_power_loss = nominal_fv - real_fv

        return {
            "status": "success",
            "data": {
                "real_return": real_return_rate,
                "nominal_fv": nominal_fv,
                "real_fv": real_fv,
                "purchasing_power_loss": purchasing_power_loss,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"inflation_adjusted_return failed: {e}")
        _log_lesson(f"inflation_adjusted_return: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
