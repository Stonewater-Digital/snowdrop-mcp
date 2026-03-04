"""Solvency II SCR coverage ratio calculator.

Computes the Solvency Capital Requirement (SCR) and coverage ratio under the
Solvency II standard formula framework (Directive 2009/138/EC).
"""
from __future__ import annotations

from typing import Any

from skills.utils import get_iso_timestamp, log_lesson

# Solvency II NAIC-equivalent action level thresholds (SCR coverage ratio)
_SCR_THRESHOLDS = {
    "adequate": 1.50,       # > 150%: no regulatory action
    "attention": 1.30,      # 130–150%: supervisory attention (Ladder of Intervention Tier 1)
    "company_action": 1.00,  # 100–130%: company required to submit recovery plan (SCR breach)
    "regulatory_action": 0.0,  # < 100%: regulatory intervention / MCR breach risk
}

TOOL_META: dict[str, Any] = {
    "name": "solvency_ratio_calculator",
    "description": (
        "Computes the Solvency II SCR coverage ratio from component risk modules. "
        "Applies the standard formula diversification benefit before adding operational risk. "
        "Returns coverage ratio, action level classification, and capital buffers."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "available_own_funds": {
                "type": "number",
                "description": "Eligible own funds (Tier 1 + Tier 2 + Tier 3) available to cover SCR. Must be >= 0.",
                "minimum": 0.0,
            },
            "scr_market_risk": {
                "type": "number",
                "description": "Market risk module SCR (interest rate, equity, spread, currency, concentration). Must be >= 0.",
                "minimum": 0.0,
            },
            "scr_underwriting_risk": {
                "type": "number",
                "description": "Underwriting risk module SCR (life, non-life, or health). Must be >= 0.",
                "minimum": 0.0,
            },
            "scr_credit_risk": {
                "type": "number",
                "description": "Counterparty default risk module SCR. Must be >= 0.",
                "minimum": 0.0,
            },
            "scr_operational_risk": {
                "type": "number",
                "description": (
                    "Operational risk add-on. Per Solvency II standard formula, operational risk is "
                    "added AFTER diversification (not subject to diversification benefit). Must be >= 0."
                ),
                "minimum": 0.0,
            },
            "diversification_benefit_pct": {
                "type": "number",
                "description": (
                    "Diversification benefit as % of basic SCR (sum of market + underwriting + credit). "
                    "Reflects off-diagonal correlation in the BSCR aggregation matrix. "
                    "Typical range 10–30%. Must be 0–50%."
                ),
                "default": 0.0,
                "minimum": 0.0,
                "maximum": 50.0,
            },
        },
        "required": [
            "available_own_funds",
            "scr_market_risk",
            "scr_underwriting_risk",
            "scr_credit_risk",
            "scr_operational_risk",
        ],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "basic_scr": {
                "type": "number",
                "description": "Sum of market + underwriting + credit risk SCRs before diversification.",
            },
            "diversification_credit": {
                "type": "number",
                "description": "Monetary diversification benefit applied to basic SCR.",
            },
            "total_scr": {
                "type": "number",
                "description": "BSCR after diversification + operational risk = final SCR.",
            },
            "solvency_ratio_pct": {
                "type": "number",
                "description": "own_funds / total_SCR × 100. Regulator expects >= 100%.",
            },
            "capital_buffer_pct": {
                "type": "number",
                "description": "solvency_ratio_pct - 100 (positive = excess capital over SCR).",
            },
            "action_level": {
                "type": "string",
                "enum": ["adequate", "attention", "company_action", "regulatory_action"],
                "description": "Solvency II ladder-of-intervention classification.",
            },
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def solvency_ratio_calculator(
    available_own_funds: float,
    scr_market_risk: float,
    scr_underwriting_risk: float,
    scr_credit_risk: float,
    scr_operational_risk: float,
    diversification_benefit_pct: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Compute Solvency II SCR and coverage ratio.

    Standard formula aggregation:
      BSCR = scr_market + scr_underwriting + scr_credit   (simplified additive, pre-diversification)
      diversification_credit = BSCR × diversification_benefit_pct / 100
      total_SCR = (BSCR - diversification_credit) + scr_operational_risk
      coverage  = available_own_funds / total_SCR

    Note: The true standard formula uses a correlation matrix for BSCR; this
    implementation uses the simpler additive approximation less diversification credit.

    Args:
        available_own_funds: Eligible own funds. Must be >= 0.
        scr_market_risk: Market risk SCR. Must be >= 0.
        scr_underwriting_risk: Underwriting risk SCR. Must be >= 0.
        scr_credit_risk: Counterparty default risk SCR. Must be >= 0.
        scr_operational_risk: Operational risk add-on. Must be >= 0.
        diversification_benefit_pct: Diversification benefit as % of basic SCR; default 0.0.

    Returns:
        dict with status "success" and solvency metrics, or status "error".
    """
    try:
        for name, val in [
            ("available_own_funds", available_own_funds),
            ("scr_market_risk", scr_market_risk),
            ("scr_underwriting_risk", scr_underwriting_risk),
            ("scr_credit_risk", scr_credit_risk),
            ("scr_operational_risk", scr_operational_risk),
        ]:
            if val < 0:
                raise ValueError(f"{name} must be >= 0, got {val}")
        if not (0.0 <= diversification_benefit_pct <= 50.0):
            raise ValueError(f"diversification_benefit_pct must be 0–50, got {diversification_benefit_pct}")

        basic_scr = scr_market_risk + scr_underwriting_risk + scr_credit_risk
        diversification_credit = basic_scr * diversification_benefit_pct / 100.0
        adjusted_bscr = basic_scr - diversification_credit
        total_scr = adjusted_bscr + scr_operational_risk

        if total_scr <= 0:
            raise ValueError(f"total_scr must be positive, got {total_scr}")

        ratio = available_own_funds / total_scr
        ratio_pct = ratio * 100.0
        capital_buffer_pct = ratio_pct - 100.0

        if ratio_pct >= _SCR_THRESHOLDS["adequate"] * 100:
            action_level = "adequate"
        elif ratio_pct >= _SCR_THRESHOLDS["attention"] * 100:
            action_level = "attention"
        elif ratio_pct >= _SCR_THRESHOLDS["company_action"] * 100:
            action_level = "company_action"
        else:
            action_level = "regulatory_action"

        return {
            "status": "success",
            "basic_scr": round(basic_scr, 2),
            "diversification_credit": round(diversification_credit, 2),
            "total_scr": round(total_scr, 2),
            "solvency_ratio_pct": round(ratio_pct, 2),
            "capital_buffer_pct": round(capital_buffer_pct, 2),
            "action_level": action_level,
            "timestamp": get_iso_timestamp(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as exc:
        log_lesson(f"solvency_ratio_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": get_iso_timestamp()}
