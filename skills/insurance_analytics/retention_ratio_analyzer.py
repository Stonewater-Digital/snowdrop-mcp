"""Retention ratio analyzer.

Analyzes net retention and reinsurance cession ratios, measuring the economic
efficiency of a reinsurance program relative to the cedant's net position.
"""
from __future__ import annotations

from typing import Any

from skills.utils import get_iso_timestamp, log_lesson

TOOL_META: dict[str, Any] = {
    "name": "retention_ratio_analyzer",
    "description": (
        "Analyzes retention and cession ratios with net loss ratio and reinsurance "
        "leverage metrics. Measures how much premium and loss exposure is retained "
        "vs. ceded and evaluates reinsurance program efficiency."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "gross_written_premium": {
                "type": "number",
                "description": "Total gross written premium before any cessions. Must be > 0.",
                "exclusiveMinimum": 0.0,
            },
            "ceded_premium": {
                "type": "number",
                "description": "Premium ceded to reinsurers. Must be >= 0 and <= gross_written_premium.",
                "minimum": 0.0,
            },
            "gross_losses": {
                "type": "number",
                "description": "Total gross incurred losses for the period. Must be >= 0.",
                "minimum": 0.0,
            },
            "ceded_losses": {
                "type": "number",
                "description": "Losses recoverable from reinsurers. Must be >= 0 and <= gross_losses.",
                "minimum": 0.0,
            },
            "ceding_commission": {
                "type": "number",
                "description": "Ceding commissions received from reinsurers (reduces net expenses). Must be >= 0.",
                "default": 0.0,
                "minimum": 0.0,
            },
        },
        "required": [
            "gross_written_premium",
            "ceded_premium",
            "gross_losses",
            "ceded_losses",
        ],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "retention_ratio_pct": {
                "type": "number",
                "description": "Net written premium / gross written premium × 100.",
            },
            "cession_ratio_pct": {
                "type": "number",
                "description": "Ceded premium / gross written premium × 100.",
            },
            "gross_loss_ratio_pct": {
                "type": "number",
                "description": "Gross losses / gross written premium × 100.",
            },
            "net_loss_ratio_pct": {
                "type": "number",
                "description": "Net losses / net written premium × 100.",
            },
            "reinsurance_recovery_ratio_pct": {
                "type": "number",
                "description": "Ceded losses / gross losses × 100 (how much loss the reinsurer absorbs).",
            },
            "reinsurance_efficiency": {
                "type": "number",
                "description": (
                    "Ceded loss ratio / cession ratio (>1.0 means reinsurer pays more than it charges proportionally)."
                ),
            },
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def retention_ratio_analyzer(
    gross_written_premium: float,
    ceded_premium: float,
    gross_losses: float,
    ceded_losses: float,
    ceding_commission: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Analyze retention, cession, and reinsurance efficiency ratios.

    Key metrics:
      retention_ratio    = net_written_premium / gross_written_premium
      cession_ratio      = ceded_premium / gross_written_premium
      net_loss_ratio     = net_losses / net_written_premium
      reinsurance_recovery = ceded_losses / gross_losses
      reinsurance_efficiency = (ceded_losses / gross_losses) / (ceded_premium / gwp)
        > 1.0 means the reinsurer recovers a higher share of loss than of premium (favorable to cedant)

    Args:
        gross_written_premium: Total GWP. Must be > 0.
        ceded_premium: Ceded premium. Must be 0 <= ceded_premium <= gross_written_premium.
        gross_losses: Gross incurred losses. Must be >= 0.
        ceded_losses: Reinsurance recoveries. Must be 0 <= ceded_losses <= gross_losses.
        ceding_commission: Commission received; reduces net cost of reinsurance; default 0.0.

    Returns:
        dict with status "success" and retention metrics, or status "error".
    """
    try:
        if gross_written_premium <= 0:
            raise ValueError(f"gross_written_premium must be positive, got {gross_written_premium}")
        if ceded_premium < 0:
            raise ValueError(f"ceded_premium must be >= 0, got {ceded_premium}")
        if ceded_premium > gross_written_premium:
            raise ValueError(
                f"ceded_premium ({ceded_premium}) cannot exceed gross_written_premium ({gross_written_premium})"
            )
        if gross_losses < 0:
            raise ValueError(f"gross_losses must be >= 0, got {gross_losses}")
        if ceded_losses < 0:
            raise ValueError(f"ceded_losses must be >= 0, got {ceded_losses}")
        if ceded_losses > gross_losses:
            raise ValueError(
                f"ceded_losses ({ceded_losses}) cannot exceed gross_losses ({gross_losses})"
            )
        if ceding_commission < 0:
            raise ValueError(f"ceding_commission must be >= 0, got {ceding_commission}")

        net_written_premium = gross_written_premium - ceded_premium
        net_losses = gross_losses - ceded_losses

        retention_ratio = net_written_premium / gross_written_premium
        cession_ratio = ceded_premium / gross_written_premium
        gross_loss_ratio = gross_losses / gross_written_premium
        net_loss_ratio = net_losses / net_written_premium if net_written_premium > 0 else 0.0
        recovery_ratio = ceded_losses / gross_losses if gross_losses > 0 else 0.0

        # Reinsurance efficiency: if > 1.0, reinsurer absorbs proportionally more loss than premium
        reinsurance_efficiency = (
            recovery_ratio / cession_ratio if cession_ratio > 0 else 0.0
        )

        return {
            "status": "success",
            "retention_ratio_pct": round(retention_ratio * 100, 2),
            "cession_ratio_pct": round(cession_ratio * 100, 2),
            "gross_loss_ratio_pct": round(gross_loss_ratio * 100, 2),
            "net_loss_ratio_pct": round(net_loss_ratio * 100, 2),
            "reinsurance_recovery_ratio_pct": round(recovery_ratio * 100, 2),
            "reinsurance_efficiency": round(reinsurance_efficiency, 4),
            "timestamp": get_iso_timestamp(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as exc:
        log_lesson(f"retention_ratio_analyzer: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": get_iso_timestamp()}
