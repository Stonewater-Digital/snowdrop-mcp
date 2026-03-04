"""Insurance-linked securities (ILS) analyzer.

Analyzes expected loss, spreads, and relative value for ILS instruments
(cat bonds, sidecars, industry loss warranties) using standard ILS market
metrics — multiple-at-risk (MAR), risk-adjusted spread, and relative value score.
"""
from __future__ import annotations

from typing import Any

from skills.utils import get_iso_timestamp, log_lesson

TOOL_META: dict[str, Any] = {
    "name": "insurance_linked_securities_tool",
    "description": (
        "Analyzes expected loss, attachment/exhaustion probabilities, multiple-at-risk (MAR), "
        "risk-adjusted spread, and relative value score for ILS instruments "
        "(cat bonds, industry loss warranties, sidecars)."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "modeled_annual_expected_loss_pct": {
                "type": "number",
                "description": (
                    "Modeled annual expected loss as % of notional. "
                    "Output from a catastrophe model (e.g., RMS, AIR). Must be > 0."
                ),
                "exclusiveMinimum": 0.0,
                "maximum": 100.0,
            },
            "attachment_return_period_years": {
                "type": "number",
                "description": (
                    "Return period at attachment in years (e.g., 50 = 1-in-50-year event). "
                    "Must be >= exhaustion_return_period_years."
                ),
                "exclusiveMinimum": 1.0,
            },
            "exhaustion_return_period_years": {
                "type": "number",
                "description": (
                    "Return period at exhaustion in years (e.g., 200 = 1-in-200-year event). "
                    "Must be >= attachment_return_period_years."
                ),
                "exclusiveMinimum": 1.0,
            },
            "quoted_spread_bps": {
                "type": "number",
                "description": "Quoted annual spread above risk-free in basis points. Must be > 0.",
                "exclusiveMinimum": 0.0,
            },
            "risk_free_rate_pct": {
                "type": "number",
                "description": "Risk-free (SOFR/T-bill) rate as percentage. Must be >= 0.",
                "minimum": 0.0,
            },
            "notional": {
                "type": "number",
                "description": "Notional principal of the ILS instrument. Must be > 0.",
                "exclusiveMinimum": 0.0,
            },
        },
        "required": [
            "modeled_annual_expected_loss_pct",
            "attachment_return_period_years",
            "exhaustion_return_period_years",
            "quoted_spread_bps",
            "risk_free_rate_pct",
            "notional",
        ],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "expected_loss_pct": {"type": "number", "description": "Modeled annual EL as % of notional."},
            "expected_loss_dollars": {"type": "number", "description": "EL × notional."},
            "attachment_probability_pct": {"type": "number", "description": "1 / attachment_RP × 100."},
            "exhaustion_probability_pct": {"type": "number", "description": "1 / exhaustion_RP × 100."},
            "multiple_at_risk": {
                "type": "number",
                "description": "coupon_spread_pct / EL_pct — spread earned per unit of expected loss.",
            },
            "risk_adjusted_spread_bps": {
                "type": "number",
                "description": "quoted_spread_bps - (EL_pct × 100) in bps.",
            },
            "expected_total_return_pct": {
                "type": "number",
                "description": "risk_free_rate + coupon_spread_pct - EL_pct.",
            },
            "relative_value_score": {
                "type": "number",
                "description": (
                    "0–100 score: MAR-based. Industry heuristic: MAR >= 2.0x scores >= 50; "
                    "MAR >= 4.0x scores 100."
                ),
            },
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def insurance_linked_securities_tool(
    modeled_annual_expected_loss_pct: float,
    attachment_return_period_years: float,
    exhaustion_return_period_years: float,
    quoted_spread_bps: float,
    risk_free_rate_pct: float,
    notional: float,
    **_: Any,
) -> dict[str, Any]:
    """Evaluate ILS instrument expected loss, pricing, and relative value.

    Key metrics:
      attachment_prob = 1 / attachment_return_period
      exhaustion_prob = 1 / exhaustion_return_period
      MAR (Multiple-at-Risk) = coupon_spread_pct / EL_pct
        Industry benchmark: MAR >= 2.0x is typical; > 4.0x is compelling value.
      risk_adjusted_spread = quoted_spread - EL (in bps)
      expected_total_return = risk_free + spread_pct - EL_pct

    Args:
        modeled_annual_expected_loss_pct: Modeled EL as % of notional. Must be > 0.
        attachment_return_period_years: Attachment RP in years (higher = rarer event).
        exhaustion_return_period_years: Exhaustion RP in years; must be >= attachment RP.
        quoted_spread_bps: Annual investor spread in bps. Must be > 0.
        risk_free_rate_pct: Risk-free rate %. Must be >= 0.
        notional: ILS notional principal. Must be > 0.

    Returns:
        dict with status "success" and ILS metrics, or status "error".
    """
    try:
        if modeled_annual_expected_loss_pct <= 0:
            raise ValueError(f"modeled_annual_expected_loss_pct must be positive, got {modeled_annual_expected_loss_pct}")
        if attachment_return_period_years <= 1:
            raise ValueError(f"attachment_return_period_years must be > 1, got {attachment_return_period_years}")
        if exhaustion_return_period_years < attachment_return_period_years:
            raise ValueError(
                f"exhaustion_return_period_years ({exhaustion_return_period_years}) must be >= "
                f"attachment_return_period_years ({attachment_return_period_years})"
            )
        if quoted_spread_bps <= 0:
            raise ValueError(f"quoted_spread_bps must be positive, got {quoted_spread_bps}")
        if risk_free_rate_pct < 0:
            raise ValueError(f"risk_free_rate_pct must be >= 0, got {risk_free_rate_pct}")
        if notional <= 0:
            raise ValueError(f"notional must be positive, got {notional}")

        attachment_prob = 1.0 / attachment_return_period_years
        exhaustion_prob = 1.0 / exhaustion_return_period_years

        el_pct = modeled_annual_expected_loss_pct
        el_dollars = el_pct / 100.0 * notional

        # Coupon spread in % terms for ratio calculations
        coupon_spread_pct = quoted_spread_bps / 100.0

        # Multiple-at-Risk: how many times EL the investor earns in spread
        multiple_at_risk = coupon_spread_pct / el_pct

        # Risk-adjusted spread in bps: raw spread minus expected loss in bps
        risk_adjusted_spread_bps = quoted_spread_bps - (el_pct * 100.0)

        # Expected total return
        expected_total_return = risk_free_rate_pct + coupon_spread_pct - el_pct

        # Relative value score: linear 0–100 based on MAR
        # MAR < 1.0 = below cost; MAR = 2.0 = min acceptable (score ~50); MAR = 4.0 = max score (100)
        relative_value_score = max(0.0, min(100.0, (multiple_at_risk - 1.0) / 3.0 * 100.0))

        return {
            "status": "success",
            "expected_loss_pct": round(el_pct, 4),
            "expected_loss_dollars": round(el_dollars, 2),
            "attachment_probability_pct": round(attachment_prob * 100, 4),
            "exhaustion_probability_pct": round(exhaustion_prob * 100, 4),
            "multiple_at_risk": round(multiple_at_risk, 4),
            "risk_adjusted_spread_bps": round(risk_adjusted_spread_bps, 2),
            "expected_total_return_pct": round(expected_total_return, 4),
            "relative_value_score": round(relative_value_score, 2),
            "timestamp": get_iso_timestamp(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as exc:
        log_lesson(f"insurance_linked_securities_tool: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": get_iso_timestamp()}
