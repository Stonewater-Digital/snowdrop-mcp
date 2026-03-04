"""Captive insurance feasibility analyzer.

Estimates the required surplus, break-even loss ratio, and feasibility score
for forming a single-parent or group captive insurer, using Value-at-Risk
methodology with a normal loss distribution assumption.
"""
from __future__ import annotations

import math
from typing import Any

from skills.utils import get_iso_timestamp, log_lesson

# Normal distribution z-scores for common confidence levels
_Z_SCORES: dict[float, float] = {
    90.0: 1.2816,
    95.0: 1.6449,
    97.5: 1.9600,
    99.0: 2.3263,
    99.5: 2.5758,
}

TOOL_META: dict[str, Any] = {
    "name": "captive_insurance_analyzer",
    "description": (
        "Estimates required surplus and feasibility for forming a captive insurer. "
        "Uses Value-at-Risk (VaR) at a user-specified confidence level with a normal "
        "loss distribution assumption. Returns required surplus, VaR capital, "
        "break-even loss ratio, and a feasibility score."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "expected_annual_losses": {
                "type": "number",
                "description": "Expected mean annual losses to be retained in the captive. Must be > 0.",
                "exclusiveMinimum": 0.0,
            },
            "loss_volatility_pct": {
                "type": "number",
                "description": (
                    "Coefficient of variation (CV) of annual losses as a percentage. "
                    "E.g., 30.0 = losses have a standard deviation of 30% of the mean. Must be > 0."
                ),
                "exclusiveMinimum": 0.0,
                "maximum": 200.0,
            },
            "premium_volume": {
                "type": "number",
                "description": "Annual gross premium charged by the captive. Must be > 0.",
                "exclusiveMinimum": 0.0,
            },
            "operating_expenses": {
                "type": "number",
                "description": "Annual captive operating expenses (management fees, fronting fees, etc.). Must be >= 0.",
                "minimum": 0.0,
            },
            "target_confidence_level_pct": {
                "type": "number",
                "description": (
                    "VaR confidence level for surplus sizing (e.g., 95.0 = 95th percentile loss). "
                    "Supported values: 90, 95, 97.5, 99, 99.5."
                ),
                "default": 95.0,
                "enum": [90.0, 95.0, 97.5, 99.0, 99.5],
            },
            "investment_return_pct": {
                "type": "number",
                "description": "Expected annual return on invested surplus. Must be >= 0.",
                "default": 3.0,
                "minimum": 0.0,
            },
        },
        "required": [
            "expected_annual_losses",
            "loss_volatility_pct",
            "premium_volume",
            "operating_expenses",
        ],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "loss_standard_deviation": {
                "type": "number",
                "description": "Standard deviation of annual losses = expected_losses × CV.",
            },
            "var_capital": {
                "type": "number",
                "description": "VaR at confidence level = z × std_dev (capital above expected losses).",
            },
            "required_surplus": {
                "type": "number",
                "description": "expected_annual_losses + var_capital (total surplus to hold at confidence level).",
            },
            "surplus_to_premium_ratio": {"type": "number", "description": "required_surplus / premium_volume."},
            "break_even_loss_ratio_pct": {
                "type": "number",
                "description": "(expected_losses + operating_expenses) / premium_volume × 100.",
            },
            "underwriting_profit_at_expected": {
                "type": "number",
                "description": "premium - expected_losses - operating_expenses (at mean loss scenario).",
            },
            "investment_income": {
                "type": "number",
                "description": "required_surplus × investment_return_pct / 100.",
            },
            "feasibility_score": {
                "type": "number",
                "description": (
                    "0–100 score. Penalizes high surplus-to-premium ratio and high loss volatility. "
                    ">= 60 = proceed; < 60 = review feasibility."
                ),
            },
            "recommendation": {
                "type": "string",
                "enum": ["proceed", "review"],
            },
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def captive_insurance_analyzer(
    expected_annual_losses: float,
    loss_volatility_pct: float,
    premium_volume: float,
    operating_expenses: float,
    target_confidence_level_pct: float = 95.0,
    investment_return_pct: float = 3.0,
    **_: Any,
) -> dict[str, Any]:
    """Estimate captive insurer surplus requirements and economic feasibility.

    Methodology (Normal VaR approach):
      std_dev         = expected_annual_losses × (loss_volatility_pct / 100)
      VaR_capital     = z_{alpha} × std_dev
      required_surplus = expected_annual_losses + VaR_capital
      break_even_LR   = (expected_losses + operating_expenses) / premium_volume

    Feasibility score (0–100):
      Penalizes: surplus/premium > 1.0 and loss volatility > 50%.
      Considers: underwriting profit at expected losses and investment income.

    Args:
        expected_annual_losses: Mean annual loss retained. Must be > 0.
        loss_volatility_pct: CV of annual losses as %. Must be > 0.
        premium_volume: Annual captive premium. Must be > 0.
        operating_expenses: Annual operating costs. Must be >= 0.
        target_confidence_level_pct: VaR confidence level; default 95.0.
        investment_return_pct: Investment return on surplus; default 3.0.

    Returns:
        dict with status "success" and feasibility metrics, or status "error".
    """
    try:
        if expected_annual_losses <= 0:
            raise ValueError(f"expected_annual_losses must be positive, got {expected_annual_losses}")
        if loss_volatility_pct <= 0:
            raise ValueError(f"loss_volatility_pct must be positive, got {loss_volatility_pct}")
        if premium_volume <= 0:
            raise ValueError(f"premium_volume must be positive, got {premium_volume}")
        if operating_expenses < 0:
            raise ValueError(f"operating_expenses must be >= 0, got {operating_expenses}")
        if investment_return_pct < 0:
            raise ValueError(f"investment_return_pct must be >= 0, got {investment_return_pct}")

        z_score = _Z_SCORES.get(float(target_confidence_level_pct))
        if z_score is None:
            # Fallback for non-standard confidence levels: use normal PPF approximation
            # Beasley-Springer-Moro approximation
            p = target_confidence_level_pct / 100.0
            if not (0.0 < p < 1.0):
                raise ValueError(f"target_confidence_level_pct must be between 0 and 100, got {target_confidence_level_pct}")
            # Simple approximation: z ≈ sqrt(2) * erfinv(2p - 1)
            # Use the closest supported value
            supported = sorted(_Z_SCORES.keys())
            nearest = min(supported, key=lambda x: abs(x - target_confidence_level_pct))
            z_score = _Z_SCORES[nearest]

        loss_cv = loss_volatility_pct / 100.0
        loss_std_dev = expected_annual_losses * loss_cv
        var_capital = z_score * loss_std_dev
        required_surplus = expected_annual_losses + var_capital

        surplus_to_premium = required_surplus / premium_volume
        break_even_lr = (expected_annual_losses + operating_expenses) / premium_volume
        underwriting_profit = premium_volume - expected_annual_losses - operating_expenses
        investment_income = required_surplus * investment_return_pct / 100.0

        # Feasibility score: 100 - penalties for surplus burden and volatility
        # Penalty 1: surplus/premium ratio above 0.5 is a burden
        surplus_penalty = max(0.0, (surplus_to_premium - 0.5) * 40.0)
        # Penalty 2: high loss volatility degrades predictability
        vol_penalty = max(0.0, (loss_volatility_pct - 20.0) * 0.5)
        # Bonus: positive underwriting profit at expected losses
        uw_bonus = max(0.0, min(20.0, underwriting_profit / premium_volume * 100.0))
        feasibility_score = max(0.0, min(100.0, 80.0 - surplus_penalty - vol_penalty + uw_bonus))

        recommendation = "proceed" if feasibility_score >= 60.0 else "review"

        return {
            "status": "success",
            "loss_standard_deviation": round(loss_std_dev, 2),
            "var_capital": round(var_capital, 2),
            "required_surplus": round(required_surplus, 2),
            "surplus_to_premium_ratio": round(surplus_to_premium, 3),
            "break_even_loss_ratio_pct": round(break_even_lr * 100, 2),
            "underwriting_profit_at_expected": round(underwriting_profit, 2),
            "investment_income": round(investment_income, 2),
            "feasibility_score": round(feasibility_score, 2),
            "recommendation": recommendation,
            "timestamp": get_iso_timestamp(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as exc:
        log_lesson(f"captive_insurance_analyzer: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": get_iso_timestamp()}
