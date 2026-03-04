"""Reinsurance treaty analyzer.

Evaluates the economic impact of quota share and per-occurrence excess-of-loss
(XL) reinsurance treaties, computing ceded/net premium, losses, ceding commission,
and net combined ratio.
"""
from __future__ import annotations

from typing import Any

from skills.utils import get_iso_timestamp, log_lesson

TOOL_META: dict[str, Any] = {
    "name": "reinsurance_treaty_analyzer",
    "description": (
        "Evaluates quota share and per-occurrence excess-of-loss treaty economics. "
        "Returns ceded and net premium/losses, ceding commission, and net combined ratio."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "treaty_type": {
                "type": "string",
                "enum": ["quota_share", "excess_of_loss"],
                "description": "Type of reinsurance treaty structure.",
            },
            "gross_premium": {
                "type": "number",
                "description": "Gross written premium before cession. Must be > 0.",
                "exclusiveMinimum": 0.0,
            },
            "gross_loss": {
                "type": "number",
                "description": "Gross incurred loss for the period. Must be >= 0.",
                "minimum": 0.0,
            },
            "gross_expenses": {
                "type": "number",
                "description": "Gross underwriting expenses for the period. Must be >= 0.",
                "default": 0.0,
                "minimum": 0.0,
            },
            "cession_pct": {
                "type": "number",
                "description": "Cession percentage for quota share (0–100). Required for quota_share.",
                "minimum": 0.0,
                "maximum": 100.0,
            },
            "retention": {
                "type": "number",
                "description": "Per-occurrence retention (attachment point) for XL. Required for excess_of_loss.",
                "minimum": 0.0,
            },
            "limit": {
                "type": "number",
                "description": "XL layer limit (maximum reinsurer payment per occurrence). Required for excess_of_loss.",
                "exclusiveMinimum": 0.0,
            },
            "ceding_commission_pct": {
                "type": "number",
                "description": "Ceding commission as % of ceded premium (quota share only). 0–100.",
                "default": 0.0,
                "minimum": 0.0,
                "maximum": 100.0,
            },
            "xol_rate_on_line_pct": {
                "type": "number",
                "description": (
                    "XL rate-on-line as % of ceded limit (price paid for the XL layer). "
                    "Required for excess_of_loss to compute ceded premium."
                ),
                "default": 0.0,
                "minimum": 0.0,
                "maximum": 100.0,
            },
        },
        "required": ["treaty_type", "gross_premium", "gross_loss"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "ceded_premium": {"type": "number"},
            "ceded_loss": {"type": "number"},
            "net_premium": {"type": "number"},
            "net_loss": {"type": "number"},
            "ceding_commission": {"type": "number"},
            "net_combined_ratio_pct": {"type": "number", "description": "(net_loss + net_expenses) / net_premium × 100."},
            "reinsurance_recovery_rate_pct": {
                "type": "number",
                "description": "ceded_loss / gross_loss × 100 (how much of gross loss the reinsurer covers).",
            },
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def reinsurance_treaty_analyzer(
    treaty_type: str,
    gross_premium: float,
    gross_loss: float,
    gross_expenses: float = 0.0,
    cession_pct: float | None = None,
    retention: float | None = None,
    limit: float | None = None,
    ceding_commission_pct: float | None = None,
    xol_rate_on_line_pct: float | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Evaluate quota share or per-occurrence XL treaty economics.

    Quota Share:
      ceded_premium   = gross_premium × cession_pct / 100
      ceded_loss      = gross_loss × cession_pct / 100
      ceding_commission = ceded_premium × ceding_commission_pct / 100

    Excess of Loss (per occurrence):
      ceded_loss      = min(max(gross_loss - retention, 0), limit)
      ceded_premium   = limit × xol_rate_on_line_pct / 100 (ROL pricing)

    Net combined ratio uses net_expenses = gross_expenses - ceding_commission
    (ceding commission offsets the cedant's expense load).

    Args:
        treaty_type: "quota_share" or "excess_of_loss".
        gross_premium: Gross written premium. Must be > 0.
        gross_loss: Gross incurred loss. Must be >= 0.
        gross_expenses: Gross underwriting expenses; default 0.0.
        cession_pct: Quota share cession %; required for quota_share.
        retention: XL attachment point; required for excess_of_loss.
        limit: XL layer limit; required for excess_of_loss.
        ceding_commission_pct: Commission on ceded premium (quota share only); default 0.0.
        xol_rate_on_line_pct: XL rate-on-line as % of limit; default 0.0.

    Returns:
        dict with status "success" and treaty economics, or status "error".
    """
    try:
        treaty_type = treaty_type.lower().strip()
        if gross_premium <= 0:
            raise ValueError(f"gross_premium must be positive, got {gross_premium}")
        if gross_loss < 0:
            raise ValueError(f"gross_loss must be >= 0, got {gross_loss}")
        if gross_expenses < 0:
            raise ValueError(f"gross_expenses must be >= 0, got {gross_expenses}")

        if treaty_type == "quota_share":
            if cession_pct is None:
                raise ValueError("cession_pct is required for quota_share treaty")
            if not (0.0 <= cession_pct <= 100.0):
                raise ValueError(f"cession_pct must be 0–100, got {cession_pct}")
            cc_pct = float(ceding_commission_pct or 0.0)
            ceded_premium = gross_premium * cession_pct / 100.0
            ceded_loss = gross_loss * cession_pct / 100.0
            ceding_commission = ceded_premium * cc_pct / 100.0

        elif treaty_type == "excess_of_loss":
            if retention is None:
                raise ValueError("retention is required for excess_of_loss treaty")
            if limit is None:
                raise ValueError("limit is required for excess_of_loss treaty")
            if retention < 0:
                raise ValueError(f"retention must be >= 0, got {retention}")
            if limit <= 0:
                raise ValueError(f"limit must be positive, got {limit}")
            rol = float(xol_rate_on_line_pct or 0.0)
            layer_loss = max(gross_loss - retention, 0.0)
            ceded_loss = min(layer_loss, limit)
            ceded_premium = limit * rol / 100.0
            ceding_commission = 0.0  # XL treaties do not carry ceding commissions

        else:
            raise ValueError(f"unsupported treaty_type '{treaty_type}'; expected 'quota_share' or 'excess_of_loss'")

        net_premium = gross_premium - ceded_premium
        net_loss = gross_loss - ceded_loss
        net_expenses = gross_expenses - ceding_commission

        net_combined_ratio = (net_loss + net_expenses) / net_premium if net_premium > 0 else float("inf")
        recovery_rate = ceded_loss / gross_loss if gross_loss > 0 else 0.0

        return {
            "status": "success",
            "ceded_premium": round(ceded_premium, 2),
            "ceded_loss": round(ceded_loss, 2),
            "net_premium": round(net_premium, 2),
            "net_loss": round(net_loss, 2),
            "ceding_commission": round(ceding_commission, 2),
            "net_combined_ratio_pct": round(net_combined_ratio * 100, 2),
            "reinsurance_recovery_rate_pct": round(recovery_rate * 100, 2),
            "timestamp": get_iso_timestamp(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as exc:
        log_lesson(f"reinsurance_treaty_analyzer: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": get_iso_timestamp()}
