"""
Executive Summary: Audits green building eligibility for ITC (solar), 179D energy deductions, and state-level ESG incentives.
Inputs: building_data (dict: leed_level, energy_star_score, solar_capacity_kw, sqft, location_state)
Outputs: dict with eligible_credits (list of dicts: program, estimated_value), total_value (float), requirements_met (list)
MCP Tool Name: green_building_subsidy_audit
"""
import os
import logging
from typing import Any, Optional
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "green_building_subsidy_audit",
    "description": (
        "Audits a commercial building's eligibility for green building tax incentives "
        "including the Investment Tax Credit (ITC) for solar, Section 179D energy "
        "efficiency deduction, and a curated set of state-level ESG incentives. "
        "Returns eligible programs, estimated values, and requirements met."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "building_data": {
                "type": "object",
                "properties": {
                    "leed_level":          {"type": "string", "description": "LEED certification: None, Certified, Silver, Gold, Platinum."},
                    "energy_star_score":   {"type": "number", "description": "Energy Star score 1-100 (75+ = certified)."},
                    "solar_capacity_kw":   {"type": "number", "description": "Installed solar PV capacity in kilowatts."},
                    "sqft":                {"type": "number", "description": "Gross building area in square feet."},
                    "location_state":      {"type": "string", "description": "Two-letter US state abbreviation (e.g., 'CA')."}
                },
                "required": ["leed_level", "energy_star_score", "solar_capacity_kw", "sqft", "location_state"]
            }
        },
        "required": ["building_data"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "eligible_credits":  {"type": "array"},
                    "total_value":       {"type": "number"},
                    "requirements_met":  {"type": "array"},
                    "ineligible_notes":  {"type": "array"}
                },
                "required": ["eligible_credits", "total_value", "requirements_met"]
            },
            "timestamp": {"type": "string"}
        },
        "required": ["status", "timestamp"]
    }
}

# ITC (Inflation Reduction Act §48): Solar base rate 30%, bonus adders available
ITC_BASE_RATE: float = 0.30
ITC_DOMESTIC_CONTENT_BONUS: float = 0.10  # +10% for domestic content
ITC_ENERGY_COMMUNITY_BONUS: float = 0.10  # +10% for energy communities
SOLAR_COST_PER_KW: float = 2_500.0        # Conservative installed cost assumption $/kW

# 179D: Energy Efficient Commercial Buildings Deduction (IRA-enhanced)
# $0.50–$1.00 base per sqft (pre-IRA); up to $5.00/sqft (IRA enhanced for prevailing wage)
DEDUCTION_179D_BASE_PER_SQFT: float = 1.00         # Minimum qualifying
DEDUCTION_179D_ENHANCED_PER_SQFT: float = 5.00     # Prevailing wage + apprenticeship
DEDUCTION_179D_MIN_ENERGY_STAR: int = 75

# LEED score mapping (for program eligibility reference)
LEED_HIERARCHY: list[str] = ["none", "certified", "silver", "gold", "platinum"]

# State incentive database (curated subset — 2025/2026 programs)
# Structure: state -> list of program dicts
STATE_INCENTIVES: dict[str, list[dict]] = {
    "CA": [
        {
            "program": "California Self-Generation Incentive Program (SGIP)",
            "description": "Battery storage incentive paired with solar.",
            "estimated_value_per_kw": 400.0,
            "condition": "solar_capacity_kw > 0",
            "requires_storage": True
        },
        {
            "program": "California Property Tax Exclusion — Solar",
            "description": "Solar equipment excluded from property tax assessment.",
            "estimated_value_per_kw": 200.0,  # NPV approximation
            "condition": "solar_capacity_kw > 0",
            "requires_storage": False
        }
    ],
    "NY": [
        {
            "program": "NY-Sun Incentive Program",
            "description": "NYSERDA rebate for commercial solar installations.",
            "estimated_value_per_kw": 300.0,
            "condition": "solar_capacity_kw > 0",
            "requires_storage": False
        },
        {
            "program": "NYC Green Roof Tax Abatement",
            "description": "Tax abatement for green roofs in NYC.",
            "estimated_value_flat": 100_000.0,
            "condition": "leed_level in ['gold','platinum']",
            "requires_storage": False
        }
    ],
    "TX": [
        {
            "program": "Texas Property Tax Exemption — Renewable Energy",
            "description": "Solar and wind equipment exempt from school property taxes.",
            "estimated_value_per_kw": 150.0,
            "condition": "solar_capacity_kw > 0",
            "requires_storage": False
        }
    ],
    "CO": [
        {
            "program": "Colorado C-PACE Financing",
            "description": "Commercial Property Assessed Clean Energy — low-rate financing for energy improvements.",
            "estimated_value_flat": 50_000.0,
            "condition": "energy_star_score >= 75 or leed_level != 'none'",
            "requires_storage": False
        }
    ],
    "MA": [
        {
            "program": "Massachusetts SMART Program (Solar)",
            "description": "Declining block incentive for commercial solar production.",
            "estimated_value_per_kw": 350.0,
            "condition": "solar_capacity_kw > 0",
            "requires_storage": False
        }
    ],
    "WA": [
        {
            "program": "Washington Sales Tax Exemption — Solar",
            "description": "Sales tax exemption on solar equipment purchases.",
            "estimated_value_per_kw": 125.0,
            "condition": "solar_capacity_kw > 0",
            "requires_storage": False
        }
    ],
    "FL": [
        {
            "program": "Florida Property Tax Exemption — Renewable Energy",
            "description": "100% property tax exemption on renewable energy improvements.",
            "estimated_value_per_kw": 175.0,
            "condition": "solar_capacity_kw > 0",
            "requires_storage": False
        }
    ],
}


def green_building_subsidy_audit(
    building_data: dict,
    **kwargs: Any
) -> dict:
    """Audit green building eligibility for federal and state tax incentives.

    Federal programs evaluated:
    - ITC §48: 30% base + bonuses on solar installation cost.
    - 179D: Energy efficiency deduction $1.00–$5.00/sqft for qualifying buildings.

    State programs: Evaluated for the building's location_state from curated database.

    Args:
        building_data: Dict with leed_level (str), energy_star_score (int/float),
            solar_capacity_kw (float), sqft (float), location_state (str).
        **kwargs: Ignored extra keyword arguments for MCP compatibility.

    Returns:
        dict with keys: status, data (eligible_credits, total_value,
        requirements_met, ineligible_notes), timestamp.

    Raises:
        ValueError: If required fields are missing or sqft/solar_capacity_kw are negative.
    """
    try:
        required = ["leed_level", "energy_star_score", "solar_capacity_kw", "sqft", "location_state"]
        for field in required:
            if field not in building_data:
                raise ValueError(f"building_data missing required field '{field}'.")

        leed_level: str = str(building_data["leed_level"]).lower().strip()
        energy_star_score: float = float(building_data["energy_star_score"])
        solar_kw: float = float(building_data["solar_capacity_kw"])
        sqft: float = float(building_data["sqft"])
        state: str = str(building_data["location_state"]).upper().strip()

        if sqft <= 0:
            raise ValueError(f"sqft must be positive, got {sqft}")
        if solar_kw < 0:
            raise ValueError(f"solar_capacity_kw cannot be negative, got {solar_kw}")
        if not (0 <= energy_star_score <= 100):
            raise ValueError(f"energy_star_score must be 0-100, got {energy_star_score}")

        eligible_credits: list[dict] = []
        requirements_met: list[str] = []
        ineligible_notes: list[str] = []

        # -----------------------------------------------------------------------
        # PROGRAM 1: Investment Tax Credit (ITC) §48 — Solar
        # -----------------------------------------------------------------------
        if solar_kw > 0:
            solar_cost_estimate: float = solar_kw * SOLAR_COST_PER_KW
            itc_base_value: float = solar_cost_estimate * ITC_BASE_RATE
            itc_total_rate: float = ITC_BASE_RATE
            itc_notes: list[str] = [
                f"Base ITC rate: {ITC_BASE_RATE * 100:.0f}% of installed cost.",
                f"Estimated system cost at ${SOLAR_COST_PER_KW:,.0f}/kW: ${solar_cost_estimate:,.0f}."
            ]

            # Bonus adder notes (user must confirm eligibility)
            itc_notes.append(
                f"Domestic Content Bonus (+{ITC_DOMESTIC_CONTENT_BONUS * 100:.0f}%): "
                "Available if steel, iron, and manufactured products are US-produced."
            )
            itc_notes.append(
                f"Energy Community Bonus (+{ITC_ENERGY_COMMUNITY_BONUS * 100:.0f}%): "
                "Available if located in a qualifying energy community (brownfield, coal closure, etc.)."
            )

            eligible_credits.append({
                "program": "Federal Investment Tax Credit (ITC) §48 — Solar",
                "category": "federal",
                "estimated_value": round(itc_base_value, 2),
                "base_rate_pct": ITC_BASE_RATE * 100,
                "max_rate_with_bonuses_pct": (ITC_BASE_RATE + ITC_DOMESTIC_CONTENT_BONUS + ITC_ENERGY_COMMUNITY_BONUS) * 100,
                "max_value_with_bonuses": round(solar_cost_estimate * (ITC_BASE_RATE + ITC_DOMESTIC_CONTENT_BONUS + ITC_ENERGY_COMMUNITY_BONUS), 2),
                "solar_kw": solar_kw,
                "notes": itc_notes
            })
            requirements_met.append(f"Solar capacity {solar_kw:.1f} kW qualifies for ITC §48.")
        else:
            ineligible_notes.append("ITC §48 Solar: No solar capacity reported (solar_capacity_kw = 0).")

        # -----------------------------------------------------------------------
        # PROGRAM 2: Section 179D — Energy Efficient Commercial Buildings Deduction
        # -----------------------------------------------------------------------
        qualifies_179d: bool = False
        deduction_179d_rate: float = 0.0

        if energy_star_score >= DEDUCTION_179D_MIN_ENERGY_STAR:
            qualifies_179d = True
            deduction_179d_rate = DEDUCTION_179D_ENHANCED_PER_SQFT
            requirements_met.append(
                f"Energy Star score {energy_star_score:.0f} >= {DEDUCTION_179D_MIN_ENERGY_STAR} "
                "qualifies for enhanced 179D deduction."
            )
        elif leed_level in ("silver", "gold", "platinum"):
            qualifies_179d = True
            deduction_179d_rate = DEDUCTION_179D_BASE_PER_SQFT
            requirements_met.append(
                f"LEED {leed_level.title()} certification qualifies for 179D base deduction."
            )

        if qualifies_179d:
            deduction_179d_value: float = sqft * deduction_179d_rate
            eligible_credits.append({
                "program": "Section 179D Energy Efficient Commercial Buildings Deduction",
                "category": "federal",
                "estimated_value": round(deduction_179d_value, 2),
                "rate_per_sqft": deduction_179d_rate,
                "sqft": sqft,
                "notes": [
                    f"Deduction rate: ${deduction_179d_rate:.2f}/sqft (up to ${DEDUCTION_179D_ENHANCED_PER_SQFT:.2f}/sqft with prevailing wage).",
                    "179D is a deduction, not a credit; tax benefit = deduction * marginal tax rate.",
                    "Requires certification by a licensed engineer or contractor."
                ]
            })
        else:
            ineligible_notes.append(
                f"Section 179D: Energy Star score {energy_star_score:.0f} is below {DEDUCTION_179D_MIN_ENERGY_STAR} "
                f"and LEED level '{leed_level}' does not meet minimum Silver. Not eligible."
            )

        # -----------------------------------------------------------------------
        # PROGRAM 3: State Incentives
        # -----------------------------------------------------------------------
        if state in STATE_INCENTIVES:
            for prog in STATE_INCENTIVES[state]:
                # Evaluate condition string
                condition_met = _eval_condition(
                    prog.get("condition", "True"),
                    leed_level=leed_level,
                    energy_star_score=energy_star_score,
                    solar_kw=solar_kw,
                    sqft=sqft
                )

                if condition_met:
                    value: float = 0.0
                    if "estimated_value_per_kw" in prog and solar_kw > 0:
                        value = prog["estimated_value_per_kw"] * solar_kw
                    elif "estimated_value_flat" in prog:
                        value = prog["estimated_value_flat"]

                    eligible_credits.append({
                        "program": prog["program"],
                        "category": f"state_{state}",
                        "estimated_value": round(value, 2),
                        "description": prog.get("description", ""),
                        "notes": [f"State: {state}. Verify current program status with state agency."]
                    })
                    requirements_met.append(f"State program '{prog['program']}' eligibility confirmed.")
                else:
                    ineligible_notes.append(
                        f"State program '{prog['program']}' condition not met."
                    )
        else:
            ineligible_notes.append(
                f"No curated state incentive data for state '{state}'. "
                "Check DSIRE (dsireusa.org) for current programs."
            )

        # -----------------------------------------------------------------------
        # Totals
        # -----------------------------------------------------------------------
        total_value: float = sum(c["estimated_value"] for c in eligible_credits)

        result: dict = {
            "building_data_summary": {
                "leed_level": leed_level,
                "energy_star_score": energy_star_score,
                "solar_capacity_kw": solar_kw,
                "sqft": sqft,
                "location_state": state
            },
            "eligible_credits": eligible_credits,
            "total_value": round(total_value, 2),
            "eligible_program_count": len(eligible_credits),
            "requirements_met": requirements_met,
            "ineligible_notes": ineligible_notes,
            "disclaimer": (
                "Estimated values are illustrative. Actual credits/deductions depend on "
                "prevailing wage certification, energy modeling reports, final tax basis, "
                "and current IRS/state agency rules. Consult a tax professional."
            )
        }

        logger.info(
            "green_building_subsidy_audit: state=%s, programs=%d, total_value=$%.2f",
            state, len(eligible_credits), total_value
        )

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except Exception as e:
        logger.error("green_building_subsidy_audit failed: %s", e)
        _log_lesson(f"green_building_subsidy_audit: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _eval_condition(
    condition: str,
    leed_level: str,
    energy_star_score: float,
    solar_kw: float,
    sqft: float
) -> bool:
    """Safely evaluate a simple string condition for state program eligibility.

    Supports: solar_capacity_kw, energy_star_score, leed_level, sqft comparisons.
    Only allows safe subset of Python expression evaluation.

    Args:
        condition: Condition string (e.g., "solar_capacity_kw > 0").
        leed_level: Building's LEED certification level (lowercased).
        energy_star_score: Energy Star score (0-100).
        solar_kw: Solar capacity in kW.
        sqft: Building area in square feet.

    Returns:
        True if condition evaluates to True, False otherwise.
    """
    try:
        # Provide safe local namespace for eval
        local_ns = {
            "solar_capacity_kw": solar_kw,
            "energy_star_score": energy_star_score,
            "leed_level": leed_level,
            "sqft": sqft,
            "True": True,
            "False": False
        }
        # Restrict to safe builtins only
        result = eval(condition, {"__builtins__": {}}, local_ns)  # noqa: S307
        return bool(result)
    except Exception as exc:
        logger.warning("_eval_condition failed for '%s': %s", condition, exc)
        return False


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
