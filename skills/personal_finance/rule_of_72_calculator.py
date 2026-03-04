"""
Executive Smary: Estimates money doubling and growth timelines using rule-of-72 and exact math.
Inputs: annual_rate (float)
Outputs: doubling_years (float), exact_doubling_years (float), tripling_years (float), quadrupling_years (float)
MCP Tool Name: rule_of_72_calculator
"""
import logging
from datetime import datetime, timezone
from math import log
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "rule_of_72_calculator",
    "description": (
        "Uses the rule of 72 alongside logarithmic growth math to estimate doubling, "
        "tripling, and quadrupling timelines for an annual return."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "annual_rate": {
                "type": "number",
                "description": "Annual compound growth rate as decimal (e.g., 0.08).",
            }
        },
        "required": ["annual_rate"],
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


def rule_of_72_calculator(**kwargs: Any) -> dict:
    """Provide rule-of-72 approximations and log-based exact compounding timelines."""
    try:
        rate = float(kwargs["annual_rate"])
        if rate <= -1:
            raise ValueError("annual_rate must be greater than -1")
        if rate == 0:
            raise ValueError("annual_rate must be non-zero to compute doubling time")

        rate_pct = rate * 100
        doubling_years = 72 / rate_pct
        exact_doubling_years = log(2) / log(1 + rate)
        tripling_years = log(3) / log(1 + rate)
        quadrupling_years = log(4) / log(1 + rate)

        return {
            "status": "success",
            "data": {
                "doubling_years": doubling_years,
                "exact_doubling_years": exact_doubling_years,
                "tripling_years": tripling_years,
                "quadrupling_years": quadrupling_years,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"rule_of_72_calculator failed: {e}")
        _log_lesson(f"rule_of_72_calculator: {e}")
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
