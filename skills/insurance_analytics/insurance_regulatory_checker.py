"""Insurance regulatory compliance checker.

Checks NAIC Risk-Based Capital (RBC) ratios and surplus adequacy against
standard regulatory thresholds for P&C insurers under NAIC Model Law.
"""
from __future__ import annotations

from typing import Any

from skills.utils import get_iso_timestamp, log_lesson

# NAIC RBC Action Level thresholds (expressed as Total Adjusted Capital / ACL RBC ratio)
# Source: NAIC Property/Casualty Risk-Based Capital Report
# ACL = Authorized Control Level RBC
# TAC/ACL ratio thresholds:
#   > 200% (2.0x): No action
#   150–200% (1.5–2.0x): Regulatory Action Level (RAL) — regulator may investigate
#   100–150% (1.0–1.5x): Authorized Control Level (ACL) — regulator may seize control
#   75–100% (0.75–1.0x): Mandatory Control Level (MCL) — regulator MUST seize
#   < 75%: Mandatory Control Level breach — insolvency proceedings

_RBC_ACTION_LEVELS = [
    (2.00, "no_action"),
    (1.50, "regulatory_action_level"),
    (1.00, "authorized_control_level"),
    (0.75, "mandatory_control_level"),
]

TOOL_META: dict[str, Any] = {
    "name": "insurance_regulatory_checker",
    "description": (
        "Checks NAIC Risk-Based Capital (RBC) ratio and NWP-to-surplus leverage against "
        "standard P&C regulatory thresholds. Returns action level classification, "
        "surplus adequacy assessment, and list of regulatory concerns."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "line_of_business": {
                "type": "string",
                "description": "Primary line of business (e.g., 'Workers Compensation', 'Commercial Auto', 'Homeowners').",
            },
            "net_written_premium": {
                "type": "number",
                "description": "Annual net written premium. Must be >= 0.",
                "minimum": 0.0,
            },
            "policyholder_surplus": {
                "type": "number",
                "description": "Total statutory policyholder surplus (net assets). May be negative (insolvency indicator).",
            },
            "total_adjusted_capital": {
                "type": "number",
                "description": (
                    "Total Adjusted Capital (TAC) = policyholder surplus + Asset Valuation Reserve "
                    "and other NAIC adjustments. Used as numerator in RBC ratio. Must be >= 0."
                ),
                "minimum": 0.0,
            },
            "authorized_control_level_rbc": {
                "type": "number",
                "description": (
                    "Authorized Control Level (ACL) RBC — the denominator of the NAIC RBC ratio. "
                    "Typically = Company Action Level RBC / 2. Must be > 0."
                ),
                "exclusiveMinimum": 0.0,
            },
            "prior_year_surplus": {
                "type": "number",
                "description": "Prior year-end policyholder surplus for surplus change analysis. Optional.",
            },
        },
        "required": [
            "line_of_business",
            "net_written_premium",
            "policyholder_surplus",
            "total_adjusted_capital",
            "authorized_control_level_rbc",
        ],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "line_of_business": {"type": "string"},
            "rbc_ratio_pct": {
                "type": "number",
                "description": "Total Adjusted Capital / ACL RBC × 100. NAIC expects > 200%.",
            },
            "nwp_to_surplus_ratio": {
                "type": "number",
                "description": "NWP / policyholder surplus. NAIC guideline max: 3.0x for most lines.",
            },
            "rbc_action_level": {
                "type": "string",
                "enum": [
                    "no_action",
                    "regulatory_action_level",
                    "authorized_control_level",
                    "mandatory_control_level",
                    "mandatory_control_level_breach",
                ],
            },
            "surplus_adequacy": {
                "type": "string",
                "enum": ["adequate", "warning", "deficient", "insolvent"],
            },
            "concerns": {
                "type": "array",
                "description": "List of specific regulatory concerns flagged.",
                "items": {"type": "string"},
            },
            "surplus_change_pct": {
                "type": "number",
                "description": "Year-over-year surplus change % if prior_year_surplus provided.",
            },
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def insurance_regulatory_checker(
    line_of_business: str,
    net_written_premium: float,
    policyholder_surplus: float,
    total_adjusted_capital: float,
    authorized_control_level_rbc: float,
    prior_year_surplus: float | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Check NAIC RBC ratios and surplus adequacy for a P&C insurer.

    NAIC RBC Ratio = Total Adjusted Capital / Authorized Control Level RBC × 100%
    Action levels (TAC/ACL):
      > 200%: No action required
      150–200%: Regulatory Action Level — regulator may investigate/require plan
      100–150%: Authorized Control Level — regulator authorized to take control
      75–100%: Mandatory Control Level — regulator must take control
      < 75%: Mandatory Control Level breach — insolvency/liquidation proceedings

    Args:
        line_of_business: Primary line written.
        net_written_premium: Annual NWP. Must be >= 0.
        policyholder_surplus: Statutory surplus (may be negative).
        total_adjusted_capital: NAIC TAC (surplus + adjustments). Must be >= 0.
        authorized_control_level_rbc: ACL RBC denominator. Must be > 0.
        prior_year_surplus: Prior year-end surplus for change analysis; optional.

    Returns:
        dict with status "success" and regulatory assessment, or status "error".
    """
    try:
        if net_written_premium < 0:
            raise ValueError(f"net_written_premium must be >= 0, got {net_written_premium}")
        if total_adjusted_capital < 0:
            raise ValueError(f"total_adjusted_capital must be >= 0, got {total_adjusted_capital}")
        if authorized_control_level_rbc <= 0:
            raise ValueError(f"authorized_control_level_rbc must be positive, got {authorized_control_level_rbc}")

        rbc_ratio = total_adjusted_capital / authorized_control_level_rbc
        rbc_ratio_pct = rbc_ratio * 100.0

        # NAIC action level classification
        if rbc_ratio >= 2.00:
            action_level = "no_action"
        elif rbc_ratio >= 1.50:
            action_level = "regulatory_action_level"
        elif rbc_ratio >= 1.00:
            action_level = "authorized_control_level"
        elif rbc_ratio >= 0.75:
            action_level = "mandatory_control_level"
        else:
            action_level = "mandatory_control_level_breach"

        # NWP to surplus (use policyholder_surplus, not TAC)
        nwp_to_surplus = (
            net_written_premium / policyholder_surplus
            if policyholder_surplus > 0
            else float("inf")
        )

        concerns: list[str] = []

        if policyholder_surplus <= 0:
            concerns.append(f"Negative or zero policyholder surplus ({policyholder_surplus:,.0f}) — insolvency indicator")
        if rbc_ratio < 2.00:
            concerns.append(f"RBC ratio {rbc_ratio_pct:.1f}% below no-action level (200%): {action_level}")
        if policyholder_surplus > 0 and nwp_to_surplus > 3.0:
            concerns.append(f"NWP/surplus ratio {nwp_to_surplus:.2f}x exceeds NAIC 3.0x guideline")
        if prior_year_surplus is not None and prior_year_surplus > 0:
            surplus_chg = (policyholder_surplus - prior_year_surplus) / prior_year_surplus * 100
            if surplus_chg < -10.0:
                concerns.append(f"Surplus declined {abs(surplus_chg):.1f}% year-over-year (>10% decline flagged)")
        else:
            surplus_chg = None

        # Surplus adequacy classification
        if policyholder_surplus <= 0:
            surplus_adequacy = "insolvent"
        elif action_level in ("mandatory_control_level", "mandatory_control_level_breach"):
            surplus_adequacy = "deficient"
        elif concerns:
            surplus_adequacy = "warning"
        else:
            surplus_adequacy = "adequate"

        result: dict[str, Any] = {
            "status": "success",
            "line_of_business": line_of_business,
            "rbc_ratio_pct": round(rbc_ratio_pct, 2),
            "nwp_to_surplus_ratio": round(nwp_to_surplus, 3) if policyholder_surplus > 0 else None,
            "rbc_action_level": action_level,
            "surplus_adequacy": surplus_adequacy,
            "concerns": concerns,
            "timestamp": get_iso_timestamp(),
        }
        if surplus_chg is not None:
            result["surplus_change_pct"] = round(surplus_chg, 2)

        return result

    except (ValueError, TypeError, ZeroDivisionError) as exc:
        log_lesson(f"insurance_regulatory_checker: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": get_iso_timestamp()}
