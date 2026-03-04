"""Catastrophe bond analyzer.

Evaluates expected loss, risk-adjusted spread, multiple-at-risk, and
investor return metrics for parametric or indemnity cat bonds.
"""
from __future__ import annotations

from typing import Any

from skills.utils import get_iso_timestamp, log_lesson

TOOL_META: dict[str, Any] = {
    "name": "catastrophe_bond_analyzer",
    "description": (
        "Evaluates expected loss, risk-adjusted spread, multiple-at-risk (MAR), "
        "and approximate Sharpe ratio for catastrophe bonds. "
        "Uses trapezoidal integration over the loss distribution to estimate expected loss."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "attachment_probability": {
                "type": "number",
                "description": (
                    "Annual probability that losses exceed the attachment point (0–1). "
                    "E.g., 0.02 = 2% annual attachment probability (1-in-50-year event)."
                ),
                "minimum": 0.0,
                "maximum": 1.0,
            },
            "exhaustion_probability": {
                "type": "number",
                "description": (
                    "Annual probability that losses exceed the exhaustion point (0–1). "
                    "Must be <= attachment_probability."
                ),
                "minimum": 0.0,
                "maximum": 1.0,
            },
            "coupon_spread_bps": {
                "type": "number",
                "description": "Annual coupon spread above LIBOR/SOFR in basis points (e.g., 500 = 5%).",
                "exclusiveMinimum": 0.0,
            },
            "notional": {
                "type": "number",
                "description": "Notional principal of the cat bond. Must be > 0.",
                "exclusiveMinimum": 0.0,
            },
            "risk_free_rate_pct": {
                "type": "number",
                "description": "Risk-free rate (SOFR/T-bill) as a percentage (e.g., 5.0 = 5%). Must be >= 0.",
                "minimum": 0.0,
            },
            "maturity_years": {
                "type": "number",
                "description": "Tenor of the cat bond in years. Must be > 0.",
                "exclusiveMinimum": 0.0,
            },
        },
        "required": [
            "attachment_probability",
            "exhaustion_probability",
            "coupon_spread_bps",
            "notional",
            "risk_free_rate_pct",
            "maturity_years",
        ],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "expected_loss_pct": {
                "type": "number",
                "description": (
                    "Annual expected loss as % of notional. "
                    "Trapezoidal approximation: 0.5 × (attachment_prob + exhaustion_prob) × 100."
                ),
            },
            "expected_loss_dollars": {"type": "number", "description": "Expected annual loss in dollars."},
            "loss_given_full_exhaustion_pct": {
                "type": "number",
                "description": "Maximum possible annual loss as % of notional (attachment_prob - exhaustion_prob) × 100.",
            },
            "multiple_at_risk": {
                "type": "number",
                "description": "Coupon spread (%) / expected_loss_pct — how many times EL the investor earns.",
            },
            "risk_adjusted_spread_bps": {
                "type": "number",
                "description": "coupon_spread_bps minus expected_loss_pct × 100 bps.",
            },
            "expected_return_pct": {
                "type": "number",
                "description": "risk_free_rate + coupon_spread(%) - expected_loss_pct.",
            },
            "sharpe_approximation": {
                "type": "number",
                "description": "Expected excess return above risk-free divided by expected loss as proxy for std dev.",
            },
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def catastrophe_bond_analyzer(
    attachment_probability: float,
    exhaustion_probability: float,
    coupon_spread_bps: float,
    notional: float,
    risk_free_rate_pct: float,
    maturity_years: float,
    **_: Any,
) -> dict[str, Any]:
    """Evaluate cat bond expected loss and investor risk/return metrics.

    Expected Loss (EL) estimation:
      Under a uniform severity distribution between attachment and exhaustion:
        EL% = 0.5 × (attachment_prob + exhaustion_prob) × (attachment_prob - exhaustion_prob)
              / attachment_prob  ... simplified to trapezoidal area under exceedance curve:
        EL% = 0.5 × (attachment_prob + exhaustion_prob) × 100
      This is standard ILS market convention for binary-trigger approximation.

    Multiple at Risk (MAR) = coupon_spread_pct / EL_pct
      Industry benchmark: MAR > 2.0x indicates reasonable risk-adjusted compensation.

    Args:
        attachment_probability: Annual prob of attaching (0–1). Must be > exhaustion_probability.
        exhaustion_probability: Annual prob of full exhaustion (0–1). Must be <= attachment_probability.
        coupon_spread_bps: Annual spread above risk-free in bps. Must be > 0.
        notional: Principal amount. Must be > 0.
        risk_free_rate_pct: Risk-free rate %. Must be >= 0.
        maturity_years: Bond tenor in years. Must be > 0.

    Returns:
        dict with status "success" and risk/return metrics, or status "error".
    """
    try:
        if not (0.0 <= exhaustion_probability <= attachment_probability <= 1.0):
            raise ValueError(
                f"Probabilities must satisfy 0 <= exhaustion_prob ({exhaustion_probability}) "
                f"<= attachment_prob ({attachment_probability}) <= 1"
            )
        if coupon_spread_bps <= 0:
            raise ValueError(f"coupon_spread_bps must be positive, got {coupon_spread_bps}")
        if notional <= 0:
            raise ValueError(f"notional must be positive, got {notional}")
        if risk_free_rate_pct < 0:
            raise ValueError(f"risk_free_rate_pct must be >= 0, got {risk_free_rate_pct}")
        if maturity_years <= 0:
            raise ValueError(f"maturity_years must be positive, got {maturity_years}")

        # Trapezoidal EL: area under exceedance curve from exhaustion to attachment
        # EL_pct = 0.5 × (p_attach + p_exhaust) × (p_attach - p_exhaust) × 100  (in-layer mean)
        # Simplified market convention for single-layer binary triggers:
        #   EL_pct ≈ 0.5 × (p_attach + p_exhaust) × 100
        # This assumes full notional lost when event exceeds exhaustion point.
        expected_loss_pct = 0.5 * (attachment_probability + exhaustion_probability) * 100.0
        expected_loss_dollars = expected_loss_pct / 100.0 * notional

        # Maximum in-layer loss probability bandwidth
        loss_given_exhaustion_pct = (attachment_probability - exhaustion_probability) * 100.0

        coupon_spread_pct = coupon_spread_bps / 100.0  # convert bps to %
        multiple_at_risk = coupon_spread_pct / expected_loss_pct if expected_loss_pct > 0 else float("inf")

        # Risk-adjusted spread: raw spread minus EL expressed in bps
        risk_adjusted_spread_bps = coupon_spread_bps - expected_loss_pct * 100.0

        # Expected total return: risk-free + spread - EL
        expected_return_pct = risk_free_rate_pct + coupon_spread_pct - expected_loss_pct

        # Sharpe approximation: excess return above risk-free / EL (as vol proxy)
        excess_return = expected_return_pct - risk_free_rate_pct
        sharpe = excess_return / expected_loss_pct if expected_loss_pct > 0 else float("inf")

        return {
            "status": "success",
            "expected_loss_pct": round(expected_loss_pct, 4),
            "expected_loss_dollars": round(expected_loss_dollars, 2),
            "loss_given_full_exhaustion_pct": round(loss_given_exhaustion_pct, 4),
            "multiple_at_risk": round(multiple_at_risk, 4),
            "risk_adjusted_spread_bps": round(risk_adjusted_spread_bps, 2),
            "expected_return_pct": round(expected_return_pct, 4),
            "sharpe_approximation": round(sharpe, 4),
            "timestamp": get_iso_timestamp(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as exc:
        log_lesson(f"catastrophe_bond_analyzer: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": get_iso_timestamp()}
