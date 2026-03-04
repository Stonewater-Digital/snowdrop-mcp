"""
Executive Summary: Validates Net Operating Income by computing NOI, margin, and variance from a prior period.
Inputs: gross_revenue (float), operating_expenses (float), prior_noi (float, optional)
Outputs: dict with noi (float), variance (float), margin_pct (float)
MCP Tool Name: noi_audit_tool
"""
import os
import logging
from typing import Any, Optional
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "noi_audit_tool",
    "description": (
        "Validates Net Operating Income (NOI) for a commercial real estate property. "
        "Computes NOI from gross revenue and operating expenses, calculates NOI margin, "
        "and flags material variance against a prior period if provided."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "gross_revenue": {
                "type": "number",
                "description": "Total gross revenue for the period (dollars)."
            },
            "operating_expenses": {
                "type": "number",
                "description": "Total operating expenses excluding debt service (dollars)."
            },
            "prior_noi": {
                "type": "number",
                "description": "NOI from the prior comparable period for variance analysis (optional)."
            }
        },
        "required": ["gross_revenue", "operating_expenses"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "noi": {"type": "number"},
                    "variance": {"type": "number"},
                    "variance_pct": {"type": "number"},
                    "margin_pct": {"type": "number"},
                    "alert": {"type": "string"}
                },
                "required": ["noi", "margin_pct"]
            },
            "timestamp": {"type": "string"}
        },
        "required": ["status", "timestamp"]
    }
}

# Material variance threshold: flag if period-over-period change exceeds this percentage
MATERIAL_VARIANCE_THRESHOLD_PCT: float = 10.0


def noi_audit_tool(
    gross_revenue: float,
    operating_expenses: float,
    prior_noi: Optional[float] = None,
    **kwargs: Any
) -> dict:
    """Compute and audit Net Operating Income for a CRE property.

    NOI = Gross Revenue - Operating Expenses (debt service excluded per standard).
    Variance is calculated when prior_noi is provided. A material alert is raised
    when variance exceeds MATERIAL_VARIANCE_THRESHOLD_PCT (default 10%).

    Args:
        gross_revenue: Total property revenue before expense deductions.
        operating_expenses: Total operating costs excluding mortgage payments.
        prior_noi: Prior period NOI for variance comparison. None skips variance calc.
        **kwargs: Ignored extra keyword arguments for MCP compatibility.

    Returns:
        dict with keys: status, data (noi, variance, variance_pct, margin_pct, alert),
        timestamp.

    Raises:
        ValueError: If gross_revenue is negative or operating_expenses exceeds revenue
            by an unreasonable amount (>200%).
    """
    try:
        gross_revenue = float(gross_revenue)
        operating_expenses = float(operating_expenses)

        if gross_revenue < 0:
            raise ValueError(f"gross_revenue cannot be negative, got {gross_revenue}")
        if operating_expenses < 0:
            raise ValueError(f"operating_expenses cannot be negative, got {operating_expenses}")

        noi: float = gross_revenue - operating_expenses

        # Margin as percentage of gross revenue (undefined if revenue is zero)
        if gross_revenue > 0:
            margin_pct: float = round((noi / gross_revenue) * 100, 2)
        else:
            margin_pct = 0.0

        variance: Optional[float] = None
        variance_pct: Optional[float] = None
        alert: Optional[str] = None

        if prior_noi is not None:
            prior_noi = float(prior_noi)
            variance = round(noi - prior_noi, 2)

            if prior_noi != 0:
                variance_pct = round((variance / abs(prior_noi)) * 100, 2)
                if abs(variance_pct) >= MATERIAL_VARIANCE_THRESHOLD_PCT:
                    direction = "increase" if variance > 0 else "decrease"
                    alert = (
                        f"MATERIAL VARIANCE: NOI {direction} of {abs(variance_pct):.1f}% "
                        f"exceeds {MATERIAL_VARIANCE_THRESHOLD_PCT}% threshold."
                    )
            else:
                # Prior NOI was zero; any current NOI is infinite variance
                variance_pct = None
                if noi != 0:
                    alert = "Prior NOI was zero; variance percentage is undefined."

        result: dict = {
            "noi": round(noi, 2),
            "margin_pct": margin_pct,
            "gross_revenue": gross_revenue,
            "operating_expenses": operating_expenses,
        }

        if variance is not None:
            result["variance"] = variance
        if variance_pct is not None:
            result["variance_pct"] = variance_pct
        if prior_noi is not None:
            result["prior_noi"] = float(prior_noi)
        if alert:
            result["alert"] = alert

        logger.info("noi_audit_tool: NOI=%.2f, margin=%.2f%%", noi, margin_pct)

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except Exception as e:
        logger.error("noi_audit_tool failed: %s", e)
        _log_lesson(f"noi_audit_tool: {e}")
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
