"""
Executive Summary: Reconciles NNN lease estimated CAM/insurance/tax charges against actuals to determine tenant adjustment.
Inputs: lease_terms (dict: base_rent, cam_estimate, insurance_estimate, tax_estimate), actuals (dict: cam_actual, insurance_actual, tax_actual), period (str)
Outputs: dict with reconciliation_report (dict), total_adjustment (float), tenant_owes (float)
MCP Tool Name: triple_net_reconciliation
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "triple_net_reconciliation",
    "description": (
        "Reconciles estimated NNN (triple-net) lease pass-through charges "
        "(CAM, insurance, property taxes) against actual year-end costs. "
        "Determines per-category variance and whether the tenant owes a "
        "true-up payment or is owed a credit."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "lease_terms": {
                "type": "object",
                "description": "Estimated charges billed to tenant throughout the period.",
                "properties": {
                    "base_rent":           {"type": "number"},
                    "cam_estimate":        {"type": "number"},
                    "insurance_estimate":  {"type": "number"},
                    "tax_estimate":        {"type": "number"}
                },
                "required": ["base_rent", "cam_estimate", "insurance_estimate", "tax_estimate"]
            },
            "actuals": {
                "type": "object",
                "description": "Actual costs incurred by the landlord for the period.",
                "properties": {
                    "cam_actual":        {"type": "number"},
                    "insurance_actual":  {"type": "number"},
                    "tax_actual":        {"type": "number"}
                },
                "required": ["cam_actual", "insurance_actual", "tax_actual"]
            },
            "period": {
                "type": "string",
                "description": "Reconciliation period label (e.g., '2025', 'Q4-2025')."
            }
        },
        "required": ["lease_terms", "actuals", "period"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "reconciliation_report": {"type": "object"},
                    "total_adjustment":      {"type": "number"},
                    "tenant_owes":           {"type": "number"},
                    "period":               {"type": "string"}
                },
                "required": ["reconciliation_report", "total_adjustment", "tenant_owes"]
            },
            "timestamp": {"type": "string"}
        },
        "required": ["status", "timestamp"]
    }
}


def triple_net_reconciliation(
    lease_terms: dict,
    actuals: dict,
    period: str,
    **kwargs: Any
) -> dict:
    """Reconcile NNN lease estimated charges against actual costs.

    For each pass-through category (CAM, insurance, taxes), computes:
      variance = actual - estimate
      positive variance = tenant underpaid (owes more)
      negative variance = tenant overpaid (landlord owes credit)

    Args:
        lease_terms: Dict with base_rent, cam_estimate, insurance_estimate,
            tax_estimate (all floats).
        actuals: Dict with cam_actual, insurance_actual, tax_actual (all floats).
        period: Human-readable label for the reconciliation period.
        **kwargs: Ignored extra keyword arguments for MCP compatibility.

    Returns:
        dict with keys: status, data (reconciliation_report, total_adjustment,
        tenant_owes, period), timestamp.

    Raises:
        ValueError: If any required field is missing from lease_terms or actuals.
    """
    try:
        # Validate required fields
        for field in ("base_rent", "cam_estimate", "insurance_estimate", "tax_estimate"):
            if field not in lease_terms:
                raise ValueError(f"lease_terms missing required field '{field}'.")
        for field in ("cam_actual", "insurance_actual", "tax_actual"):
            if field not in actuals:
                raise ValueError(f"actuals missing required field '{field}'.")

        base_rent: float = float(lease_terms["base_rent"])
        cam_est: float = float(lease_terms["cam_estimate"])
        ins_est: float = float(lease_terms["insurance_estimate"])
        tax_est: float = float(lease_terms["tax_estimate"])

        cam_act: float = float(actuals["cam_actual"])
        ins_act: float = float(actuals["insurance_actual"])
        tax_act: float = float(actuals["tax_actual"])

        def _reconcile_category(estimate: float, actual: float, name: str) -> dict:
            """Build a single-category reconciliation entry."""
            variance = round(actual - estimate, 2)
            variance_pct = round((variance / estimate * 100), 2) if estimate != 0 else None
            return {
                "category": name,
                "estimate": round(estimate, 2),
                "actual": round(actual, 2),
                "variance": variance,
                "variance_pct": variance_pct,
                "status": "underpaid" if variance > 0 else ("overpaid" if variance < 0 else "exact")
            }

        cam_rec = _reconcile_category(cam_est, cam_act, "CAM")
        ins_rec = _reconcile_category(ins_est, ins_act, "Insurance")
        tax_rec = _reconcile_category(tax_est, tax_act, "Property Tax")

        # Total adjustment: positive = tenant owes, negative = credit to tenant
        total_variance: float = round(cam_rec["variance"] + ins_rec["variance"] + tax_rec["variance"], 2)

        # Total pass-throughs estimated vs actual
        total_estimated_nnn: float = round(cam_est + ins_est + tax_est, 2)
        total_actual_nnn: float = round(cam_act + ins_act + tax_act, 2)
        total_rent_collected: float = round(base_rent + total_estimated_nnn, 2)

        reconciliation_report: dict = {
            "period": str(period),
            "base_rent": round(base_rent, 2),
            "categories": [cam_rec, ins_rec, tax_rec],
            "total_estimated_nnn": total_estimated_nnn,
            "total_actual_nnn": total_actual_nnn,
            "total_rent_collected": total_rent_collected,
            "total_variance": total_variance,
            "settlement_direction": (
                "tenant_owes_landlord" if total_variance > 0
                else ("landlord_owes_tenant_credit" if total_variance < 0 else "no_adjustment")
            )
        }

        # tenant_owes is positive when tenant must pay more, negative when owed a credit
        tenant_owes: float = total_variance

        logger.info(
            "triple_net_reconciliation: period=%s, total_variance=%.2f, direction=%s",
            period, total_variance, reconciliation_report["settlement_direction"]
        )

        return {
            "status": "success",
            "data": {
                "reconciliation_report": reconciliation_report,
                "total_adjustment": total_variance,
                "tenant_owes": tenant_owes,
                "period": str(period)
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except Exception as e:
        logger.error("triple_net_reconciliation failed: %s", e)
        _log_lesson(f"triple_net_reconciliation: {e}")
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
