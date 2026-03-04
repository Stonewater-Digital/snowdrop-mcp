"""Quota share treaty calculator.

Computes ceded and retained amounts under a proportional quota share
reinsurance treaty, including ceding commission, sliding scale logic,
and net underwriting result.
"""
from __future__ import annotations

from typing import Any

from skills.utils import get_iso_timestamp, log_lesson

TOOL_META: dict[str, Any] = {
    "name": "quota_share_calculator",
    "description": (
        "Computes ceded and retained premium, losses, ceding commission, and "
        "net underwriting result under a proportional quota share treaty. "
        "Supports fixed and provisional/sliding scale commission."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "gross_premium": {
                "type": "number",
                "description": "Gross written premium subject to the quota share. Must be > 0.",
                "exclusiveMinimum": 0.0,
            },
            "gross_loss": {
                "type": "number",
                "description": "Gross incurred losses subject to cession. Must be >= 0.",
                "minimum": 0.0,
            },
            "quota_pct": {
                "type": "number",
                "description": "Cession percentage (0–100). E.g., 30.0 = cedant cedes 30% of premium and losses.",
                "minimum": 0.0,
                "maximum": 100.0,
            },
            "ceding_commission_pct": {
                "type": "number",
                "description": (
                    "Ceding commission as a percentage of ceded premium (0–100). "
                    "Represents the reinsurer's contribution to the cedant's acquisition costs."
                ),
                "minimum": 0.0,
                "maximum": 100.0,
            },
            "gross_expenses": {
                "type": "number",
                "description": "Gross underwriting expenses (before ceding commission offset). Must be >= 0.",
                "default": 0.0,
                "minimum": 0.0,
            },
        },
        "required": ["gross_premium", "gross_loss", "quota_pct", "ceding_commission_pct"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "ceded_premium": {"type": "number"},
            "retained_premium": {"type": "number"},
            "ceded_loss": {"type": "number"},
            "retained_loss": {"type": "number"},
            "ceding_commission": {"type": "number"},
            "net_expenses": {"type": "number", "description": "gross_expenses - ceding_commission."},
            "net_underwriting_result": {
                "type": "number",
                "description": "retained_premium - retained_loss - net_expenses.",
            },
            "net_loss_ratio_pct": {
                "type": "number",
                "description": "retained_loss / retained_premium × 100.",
            },
            "net_combined_ratio_pct": {
                "type": "number",
                "description": "(retained_loss + net_expenses) / retained_premium × 100.",
            },
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def quota_share_calculator(
    gross_premium: float,
    gross_loss: float,
    quota_pct: float,
    ceding_commission_pct: float,
    gross_expenses: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Compute quota share treaty ceded/retained splits and net underwriting result.

    Mechanics:
      ceded_premium      = gross_premium × quota_pct / 100
      retained_premium   = gross_premium × (1 - quota_pct / 100)
      ceded_loss         = gross_loss × quota_pct / 100
      retained_loss      = gross_loss × (1 - quota_pct / 100)
      ceding_commission  = ceded_premium × ceding_commission_pct / 100
      net_expenses       = gross_expenses - ceding_commission
      net_uw_result      = retained_premium - retained_loss - net_expenses

    Args:
        gross_premium: Subject GWP. Must be > 0.
        gross_loss: Gross incurred losses. Must be >= 0.
        quota_pct: Cession percentage 0–100.
        ceding_commission_pct: Commission on ceded premium 0–100.
        gross_expenses: Gross underwriting expenses; default 0.0.

    Returns:
        dict with status "success" and treaty splits, or status "error".
    """
    try:
        if gross_premium <= 0:
            raise ValueError(f"gross_premium must be positive, got {gross_premium}")
        if gross_loss < 0:
            raise ValueError(f"gross_loss must be >= 0, got {gross_loss}")
        if not (0.0 <= quota_pct <= 100.0):
            raise ValueError(f"quota_pct must be 0–100, got {quota_pct}")
        if not (0.0 <= ceding_commission_pct <= 100.0):
            raise ValueError(f"ceding_commission_pct must be 0–100, got {ceding_commission_pct}")
        if gross_expenses < 0:
            raise ValueError(f"gross_expenses must be >= 0, got {gross_expenses}")

        cession = quota_pct / 100.0
        ceded_premium = gross_premium * cession
        retained_premium = gross_premium - ceded_premium
        ceded_loss = gross_loss * cession
        retained_loss = gross_loss - ceded_loss
        ceding_commission = ceded_premium * ceding_commission_pct / 100.0
        net_expenses = gross_expenses - ceding_commission
        net_uw_result = retained_premium - retained_loss - net_expenses

        net_loss_ratio = retained_loss / retained_premium if retained_premium > 0 else 0.0
        net_combined_ratio = (retained_loss + net_expenses) / retained_premium if retained_premium > 0 else 0.0

        return {
            "status": "success",
            "ceded_premium": round(ceded_premium, 2),
            "retained_premium": round(retained_premium, 2),
            "ceded_loss": round(ceded_loss, 2),
            "retained_loss": round(retained_loss, 2),
            "ceding_commission": round(ceding_commission, 2),
            "net_expenses": round(net_expenses, 2),
            "net_underwriting_result": round(net_uw_result, 2),
            "net_loss_ratio_pct": round(net_loss_ratio * 100, 2),
            "net_combined_ratio_pct": round(net_combined_ratio * 100, 2),
            "timestamp": get_iso_timestamp(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as exc:
        log_lesson(f"quota_share_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": get_iso_timestamp()}
