"""
Executive Smary: Estimates U.S. self-employment tax and deductible portion.
Inputs: net_self_employment_income (float)
Outputs: se_tax (float), social_security_portion (float), medicare_portion (float), additional_medicare (float), deductible_half (float), effective_se_rate (float)
MCP Tool Name: self_employment_tax_calculator
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

SE_CAP = 168600

TOOL_META = {
    "name": "self_employment_tax_calculator",
    "description": (
        "Computes Social Security and Medicare self-employment tax components, "
        "including the deductible half and additional Medicare surtax."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "net_self_employment_income": {
                "type": "number",
                "description": "Schedule C or partnership net earnings subject to SE tax.",
            }
        },
        "required": ["net_self_employment_income"],
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


def self_employment_tax_calculator(**kwargs: Any) -> dict:
    """Estimate self-employment tax components for a given net income."""
    try:
        net_income = float(kwargs["net_self_employment_income"])
        if net_income < 0:
            raise ValueError("net_self_employment_income must be non-negative")

        se_earnings = net_income * 0.9235
        ss_taxable = min(se_earnings, SE_CAP)
        social_security = ss_taxable * 0.124
        medicare = se_earnings * 0.029
        additional_medicare = max(se_earnings - 200000, 0.0) * 0.009
        se_tax = social_security + medicare + additional_medicare
        deductible_half = se_tax / 2
        effective_rate = se_tax / net_income if net_income > 0 else 0.0

        return {
            "status": "success",
            "data": {
                "se_tax": se_tax,
                "social_security_portion": social_security,
                "medicare_portion": medicare,
                "additional_medicare": additional_medicare,
                "deductible_half": deductible_half,
                "effective_se_rate": effective_rate,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"self_employment_tax_calculator failed: {e}")
        _log_lesson(f"self_employment_tax_calculator: {e}")
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
