"""
Executive Summary: Calculates monthly mortgage escrow amounts for property taxes and insurance from millage rate and assessed value.
Inputs: assessed_value (float), tax_rate (float, millage), annual_insurance (float, optional)
Outputs: dict with monthly_escrow (float), annual_tax (float), annual_total (float)
MCP Tool Name: real_estate_tax_escrow
"""
import os
import logging
from typing import Any, Optional
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "real_estate_tax_escrow",
    "description": (
        "Calculates monthly escrow reserve requirements for property taxes and "
        "insurance. Uses the millage rate system (mills per $1,000 of assessed value). "
        "Outputs monthly escrow, annual tax, and combined annual total."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "assessed_value": {
                "type": "number",
                "description": "Assessed property value for tax purposes (dollars)."
            },
            "tax_rate": {
                "type": "number",
                "description": "Property tax rate in mills (e.g., 25 = $25 per $1,000 assessed value)."
            },
            "annual_insurance": {
                "type": "number",
                "description": "Annual property insurance premium (dollars, optional)."
            }
        },
        "required": ["assessed_value", "tax_rate"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "monthly_escrow":   {"type": "number"},
                    "annual_tax":       {"type": "number"},
                    "annual_total":     {"type": "number"},
                    "annual_insurance": {"type": "number"},
                    "effective_tax_rate_pct": {"type": "number"}
                },
                "required": ["monthly_escrow", "annual_tax", "annual_total"]
            },
            "timestamp": {"type": "string"}
        },
        "required": ["status", "timestamp"]
    }
}

MILLS_DIVISOR: float = 1_000.0
MONTHS_PER_YEAR: int = 12

# RESPA-compliant escrow cushion: 2-month reserve allowed
RESPA_CUSHION_MONTHS: int = 2


def real_estate_tax_escrow(
    assessed_value: float,
    tax_rate: float,
    annual_insurance: Optional[float] = None,
    **kwargs: Any
) -> dict:
    """Compute monthly PITI escrow for property taxes and insurance.

    Formula:
      annual_tax = assessed_value * (tax_rate / 1000)
      annual_total = annual_tax + annual_insurance (if provided)
      monthly_escrow = annual_total / 12
      respa_cushion = monthly_escrow * 2  (2-month RESPA reserve)

    Effective tax rate = annual_tax / assessed_value * 100 (as a percentage).

    Args:
        assessed_value: Assessed value of the property for tax calculation purposes.
        tax_rate: Millage rate in mills (mills = dollars per $1,000 of assessed value).
        annual_insurance: Annual hazard/property insurance premium in dollars (optional).
        **kwargs: Ignored extra keyword arguments for MCP compatibility.

    Returns:
        dict with keys: status, data (monthly_escrow, annual_tax, annual_total,
        annual_insurance, effective_tax_rate_pct, respa_2_month_cushion), timestamp.

    Raises:
        ValueError: If assessed_value or tax_rate is negative.
    """
    try:
        assessed_value = float(assessed_value)
        tax_rate = float(tax_rate)

        if assessed_value < 0:
            raise ValueError(f"assessed_value cannot be negative, got {assessed_value}")
        if tax_rate < 0:
            raise ValueError(f"tax_rate (millage) cannot be negative, got {tax_rate}")

        # Core tax calculation
        annual_tax: float = assessed_value * (tax_rate / MILLS_DIVISOR)
        effective_tax_rate_pct: float = (
            round((annual_tax / assessed_value) * 100, 4) if assessed_value > 0 else 0.0
        )

        # Insurance handling
        insurance_amount: float = 0.0
        if annual_insurance is not None:
            insurance_amount = float(annual_insurance)
            if insurance_amount < 0:
                raise ValueError(f"annual_insurance cannot be negative, got {insurance_amount}")

        annual_total: float = annual_tax + insurance_amount
        monthly_escrow: float = annual_total / MONTHS_PER_YEAR
        respa_cushion: float = monthly_escrow * RESPA_CUSHION_MONTHS

        result: dict = {
            "assessed_value": assessed_value,
            "tax_rate_mills": tax_rate,
            "annual_tax": round(annual_tax, 2),
            "annual_insurance": round(insurance_amount, 2),
            "annual_total": round(annual_total, 2),
            "monthly_escrow": round(monthly_escrow, 2),
            "effective_tax_rate_pct": effective_tax_rate_pct,
            "respa_2_month_cushion": round(respa_cushion, 2),
            "includes_insurance": annual_insurance is not None
        }

        logger.info(
            "real_estate_tax_escrow: annual_tax=%.2f, monthly_escrow=%.2f",
            annual_tax, monthly_escrow
        )

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except Exception as e:
        logger.error("real_estate_tax_escrow failed: %s", e)
        _log_lesson(f"real_estate_tax_escrow: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _log_lesson(message: str) -> None:
    """Append a lesson-learned entry to the shared lessons log.

    Args:
        message: Description of the error or lesson to record.
    """
    try:
        os.makedirs("logs", exist_ok=True)
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError as log_err:
        logger.warning("Could not write to lessons.md: %s", log_err)
