"""
Executive Summary: Computes REIT Funds From Operations (FFO) and Adjusted FFO (AFFO) per NAREIT standards.
Inputs: net_income (float), depreciation (float), amortization (float), gains_on_sales (float), shares_outstanding (float)
Outputs: dict with ffo (float), ffo_per_share (float), affo (float)
MCP Tool Name: reit_ffo_calculator
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "reit_ffo_calculator",
    "description": (
        "Calculates REIT Funds From Operations (FFO) and Adjusted FFO (AFFO) "
        "per NAREIT standards. FFO adds back real estate depreciation and "
        "amortization to GAAP net income and excludes gains/losses on property sales."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "net_income": {
                "type": "number",
                "description": "GAAP net income for the period (dollars)."
            },
            "depreciation": {
                "type": "number",
                "description": "Real estate depreciation added back (dollars)."
            },
            "amortization": {
                "type": "number",
                "description": "Real estate amortization added back (dollars)."
            },
            "gains_on_sales": {
                "type": "number",
                "description": "Net gains on property sales to be excluded (dollars)."
            },
            "shares_outstanding": {
                "type": "number",
                "description": "Weighted-average diluted shares outstanding."
            }
        },
        "required": ["net_income", "depreciation", "amortization", "gains_on_sales", "shares_outstanding"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "ffo": {"type": "number"},
                    "ffo_per_share": {"type": "number"},
                    "affo": {"type": "number"},
                    "affo_per_share": {"type": "number"},
                    "maintenance_capex_estimate": {"type": "number"},
                    "inputs_summary": {"type": "object"}
                },
                "required": ["ffo", "ffo_per_share", "affo", "affo_per_share"]
            },
            "timestamp": {"type": "string"}
        },
        "required": ["status", "timestamp"]
    }
}


def reit_ffo_calculator(
    net_income: float,
    depreciation: float,
    amortization: float,
    gains_on_sales: float,
    shares_outstanding: float,
    **kwargs: Any
) -> dict:
    """Calculate FFO and AFFO for a REIT per NAREIT standards.

    FFO = Net Income + Depreciation + Amortization - Gains on Sales
    AFFO = FFO - Maintenance CapEx Estimate (5% of depreciation proxy)

    Args:
        net_income: GAAP net income for the period in dollars.
        depreciation: Real estate depreciation to add back in dollars.
        amortization: Real estate amortization to add back in dollars.
        gains_on_sales: Net gains on property sales to exclude in dollars.
        shares_outstanding: Weighted-average diluted shares outstanding.
        **kwargs: Ignored extra keyword arguments for MCP compatibility.

    Returns:
        dict with keys: status, data (ffo, ffo_per_share, affo, affo_per_share,
        maintenance_capex_estimate, inputs_summary), timestamp.

    Raises:
        ValueError: If shares_outstanding is zero or negative.
    """
    try:
        net_income = float(net_income)
        depreciation = float(depreciation)
        amortization = float(amortization)
        gains_on_sales = float(gains_on_sales)
        shares_outstanding = float(shares_outstanding)

        if shares_outstanding <= 0:
            raise ValueError(f"shares_outstanding must be positive, got {shares_outstanding}")
        if depreciation < 0:
            raise ValueError(f"depreciation cannot be negative, got {depreciation}")
        if amortization < 0:
            raise ValueError(f"amortization cannot be negative, got {amortization}")

        # Core FFO calculation per NAREIT white paper
        ffo: float = net_income + depreciation + amortization - gains_on_sales
        ffo_per_share: float = ffo / shares_outstanding

        # AFFO: subtract a conservative maintenance CapEx proxy (5% of depreciation)
        # In practice this is disclosed; 5% is the Snowdrop default estimate
        maintenance_capex_estimate: float = depreciation * 0.05
        affo: float = ffo - maintenance_capex_estimate
        affo_per_share: float = affo / shares_outstanding

        result = {
            "ffo": round(ffo, 2),
            "ffo_per_share": round(ffo_per_share, 4),
            "affo": round(affo, 2),
            "affo_per_share": round(affo_per_share, 4),
            "maintenance_capex_estimate": round(maintenance_capex_estimate, 2),
            "inputs_summary": {
                "net_income": net_income,
                "depreciation": depreciation,
                "amortization": amortization,
                "gains_on_sales": gains_on_sales,
                "shares_outstanding": shares_outstanding
            }
        }

        logger.info(
            "reit_ffo_calculator: FFO=%.2f, FFO/share=%.4f, AFFO=%.2f",
            ffo, ffo_per_share, affo
        )

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except Exception as e:
        logger.error("reit_ffo_calculator failed: %s", e)
        _log_lesson(f"reit_ffo_calculator: {e}")
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
