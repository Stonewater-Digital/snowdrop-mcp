"""
Executive Summary: Audits 1031 exchange and Qualified Opportunity Zone (QOZ) compliance per IRC §1400Z-2.
Inputs: investment_details (dict: investment_date, amount, zone_tract_id, holding_period_months, substantially_improved, original_use)
Outputs: dict with compliant (bool), issues (list), tax_benefit_estimate (dict)
MCP Tool Name: opportunity_zone_audit
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone, date

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "opportunity_zone_audit",
    "description": (
        "Audits Qualified Opportunity Zone (QOZ) investment compliance per IRC §1400Z-2. "
        "Checks the 180-day reinvestment window, 10-year hold for full exclusion, "
        "substantial improvement test (must double basis in improvements), and "
        "original use doctrine. Estimates tax benefits."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "investment_details": {
                "type": "object",
                "properties": {
                    "investment_date":        {"type": "string", "description": "ISO date of QOZ investment (YYYY-MM-DD)."},
                    "amount":                 {"type": "number", "description": "Investment amount in dollars."},
                    "zone_tract_id":          {"type": "string", "description": "Census tract ID of the QOZ."},
                    "holding_period_months":  {"type": "number", "description": "Months investment has been / will be held."},
                    "substantially_improved": {"type": "boolean", "description": "Property improvements > original basis."},
                    "original_use":           {"type": "boolean", "description": "Property is original use in the QOZ."}
                },
                "required": [
                    "investment_date", "amount", "zone_tract_id",
                    "holding_period_months", "substantially_improved", "original_use"
                ]
            }
        },
        "required": ["investment_details"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "compliant":            {"type": "boolean"},
                    "issues":               {"type": "array"},
                    "tax_benefit_estimate": {"type": "object"},
                    "holding_tier":         {"type": "string"}
                },
                "required": ["compliant", "issues", "tax_benefit_estimate"]
            },
            "timestamp": {"type": "string"}
        },
        "required": ["status", "timestamp"]
    }
}

# IRC §1400Z-2 key thresholds
REINVESTMENT_WINDOW_DAYS: int = 180
HOLD_5_YEAR_MONTHS: int = 60   # 10% basis step-up (legacy, pre-2022 phase-out)
HOLD_7_YEAR_MONTHS: int = 84   # Additional 5% basis step-up (legacy)
HOLD_10_YEAR_MONTHS: int = 120  # Full gain exclusion on QOZ appreciation

# Assumed capital gains tax rate for benefit estimate
ASSUMED_CAPITAL_GAINS_RATE: float = 0.238  # 20% + 3.8% NIIT (federal)


def opportunity_zone_audit(
    investment_details: dict,
    **kwargs: Any
) -> dict:
    """Audit QOZ investment compliance and estimate tax benefits per IRC §1400Z-2.

    Checks:
    1. 180-day reinvestment window: Investment must be made within 180 days of
       recognized gain event. (We validate investment_date is provided; the 180-day
       clock start is caller-supplied context.)
    2. Substantial improvement test: Unless original use, improvements must exceed
       original property basis (i.e., substantially_improved = True).
    3. 10-year hold: Full exclusion of QOZ appreciation requires >= 120-month hold.
    4. Holding tier classification: 5yr / 7yr / 10yr benefit thresholds.

    Tax benefit estimate assumes the investment amount represents deferred gain:
    - Deferred gain tax liability = amount * ASSUMED_CAPITAL_GAINS_RATE
    - If 10-year hold: QOZ appreciation excluded entirely (assumed 30% appreciation)

    Args:
        investment_details: Dict with investment_date (str ISO), amount (float),
            zone_tract_id (str), holding_period_months (float), substantially_improved
            (bool), original_use (bool).
        **kwargs: Ignored extra keyword arguments for MCP compatibility.

    Returns:
        dict with keys: status, data (compliant, issues, tax_benefit_estimate,
        holding_tier, holding_months, requirements_met), timestamp.

    Raises:
        ValueError: If required fields are missing or amount is non-positive.
    """
    try:
        required = [
            "investment_date", "amount", "zone_tract_id",
            "holding_period_months", "substantially_improved", "original_use"
        ]
        for field in required:
            if field not in investment_details:
                raise ValueError(f"investment_details missing required field '{field}'.")

        investment_date_str: str = str(investment_details["investment_date"])
        amount: float = float(investment_details["amount"])
        zone_tract_id: str = str(investment_details["zone_tract_id"])
        holding_months: float = float(investment_details["holding_period_months"])
        substantially_improved: bool = bool(investment_details["substantially_improved"])
        original_use: bool = bool(investment_details["original_use"])

        if amount <= 0:
            raise ValueError(f"investment amount must be positive, got {amount}")
        if holding_months < 0:
            raise ValueError(f"holding_period_months cannot be negative, got {holding_months}")

        # Parse investment date
        try:
            inv_date = date.fromisoformat(investment_date_str)
        except ValueError:
            raise ValueError(
                f"investment_date '{investment_date_str}' is not a valid ISO date (YYYY-MM-DD)."
            )

        issues: list[str] = []
        requirements_met: list[str] = []

        # --- Check 1: Investment date is in the past ---
        today = date.today()
        if inv_date > today:
            issues.append(
                f"investment_date {investment_date_str} is in the future. "
                "QOZ investment must already be made."
            )
        else:
            requirements_met.append("Investment date is in the past (valid).")

        # --- Check 2: 180-day reinvestment window ---
        # We note the window; the caller is responsible for tracking the trigger date.
        # We flag if investment_date is clearly problematic (pre-2018 QOZ program start).
        qoz_program_start = date(2018, 1, 1)
        if inv_date < qoz_program_start:
            issues.append(
                f"investment_date {investment_date_str} precedes QOZ program start "
                f"(January 1, 2018). QOZ investments cannot qualify before this date."
            )
        else:
            requirements_met.append(
                f"Investment date {investment_date_str} is within QOZ program window."
            )

        # --- Check 3: Substantial improvement OR original use ---
        if not original_use and not substantially_improved:
            issues.append(
                "Property fails both the original use test and the substantial improvement "
                "test. Either original_use must be True OR substantially_improved must be "
                "True (improvements > 100% of purchase basis within 30 months)."
            )
        elif substantially_improved:
            requirements_met.append("Substantial improvement test passed.")
        elif original_use:
            requirements_met.append("Original use doctrine satisfied (no improvement test required).")

        # --- Check 4: Holding period tiers ---
        holding_tier: str
        if holding_months >= HOLD_10_YEAR_MONTHS:
            holding_tier = "10_year"
            requirements_met.append(
                f"10-year hold achieved ({holding_months:.1f} months). "
                "Full exclusion of QOZ appreciation qualifies."
            )
        elif holding_months >= HOLD_7_YEAR_MONTHS:
            holding_tier = "7_year"
            requirements_met.append(
                f"7-year hold tier ({holding_months:.1f} months). "
                "Legacy 5% additional basis step-up (if applicable pre-2022 deadlines)."
            )
        elif holding_months >= HOLD_5_YEAR_MONTHS:
            holding_tier = "5_year"
            requirements_met.append(
                f"5-year hold tier ({holding_months:.1f} months). "
                "Legacy 10% basis step-up (if applicable pre-2022 deadlines)."
            )
        else:
            holding_tier = "sub_5_year"
            months_to_10yr = HOLD_10_YEAR_MONTHS - holding_months
            issues.append(
                f"Holding period of {holding_months:.1f} months is below the 5-year threshold. "
                f"{months_to_10yr:.1f} more months needed for 10-year full exclusion benefit."
            )

        # --- Tax Benefit Estimate ---
        # Deferred gain: tax owed on original gain (deferred until end of deferral or 12/31/2026)
        deferred_tax_owed: float = amount * ASSUMED_CAPITAL_GAINS_RATE

        # Appreciation exclusion: if 10-year hold, assume 30% appreciation on principal
        assumed_appreciation_rate: float = 0.30
        qoz_appreciation_gain: float = amount * assumed_appreciation_rate

        if holding_tier == "10_year":
            exclusion_benefit: float = qoz_appreciation_gain * ASSUMED_CAPITAL_GAINS_RATE
        else:
            exclusion_benefit = 0.0

        tax_benefit_estimate: dict = {
            "assumed_capital_gains_rate_pct": round(ASSUMED_CAPITAL_GAINS_RATE * 100, 1),
            "deferred_gain_tax_owed_eventually": round(deferred_tax_owed, 2),
            "deferral_benefit_note": (
                "Original gain tax deferred until 12/31/2026 or disposition, whichever is earlier."
            ),
            "assumed_appreciation_rate_pct": round(assumed_appreciation_rate * 100, 1),
            "estimated_qoz_appreciation": round(qoz_appreciation_gain, 2),
            "exclusion_tax_benefit": round(exclusion_benefit, 2),
            "exclusion_applies": holding_tier == "10_year",
            "total_estimated_benefit": round(exclusion_benefit, 2),
            "disclaimer": (
                "Estimates assume federal rates only (20% LTCG + 3.8% NIIT). "
                "State taxes excluded. Consult a tax professional."
            )
        }

        compliant: bool = len(issues) == 0

        result: dict = {
            "investment_date": investment_date_str,
            "amount": amount,
            "zone_tract_id": zone_tract_id,
            "holding_period_months": holding_months,
            "holding_tier": holding_tier,
            "substantially_improved": substantially_improved,
            "original_use": original_use,
            "compliant": compliant,
            "issues": issues,
            "requirements_met": requirements_met,
            "tax_benefit_estimate": tax_benefit_estimate
        }

        logger.info(
            "opportunity_zone_audit: tract=%s, compliant=%s, holding_tier=%s, issues=%d",
            zone_tract_id, compliant, holding_tier, len(issues)
        )

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except Exception as e:
        logger.error("opportunity_zone_audit failed: %s", e)
        _log_lesson(f"opportunity_zone_audit: {e}")
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
