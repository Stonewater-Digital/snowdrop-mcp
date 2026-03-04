"""Excess-of-loss recovery calculator.

Computes per-occurrence reinsurance recoveries, aggregate metrics, and
reinstatement premium for an XL layer applied to a portfolio of ground-up losses.
"""
from __future__ import annotations

from typing import Any

from skills.utils import get_iso_timestamp, log_lesson

TOOL_META: dict[str, Any] = {
    "name": "excess_of_loss_calculator",
    "description": (
        "Calculates per-occurrence reinsurance recoveries, layer loss ratio, "
        "attachment frequency, average in-layer severity, and reinstatement premium "
        "for an excess-of-loss (XL) reinsurance layer applied to a list of ground-up losses."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "ground_up_losses": {
                "type": "array",
                "description": "List of per-occurrence ground-up loss amounts (before retention). Each must be >= 0.",
                "items": {"type": "number", "minimum": 0.0},
                "minItems": 1,
            },
            "attachment": {
                "type": "number",
                "description": "Per-occurrence retention / attachment point. Must be >= 0.",
                "minimum": 0.0,
            },
            "limit": {
                "type": "number",
                "description": "XL layer limit — maximum reinsurer payment per occurrence. Must be > 0.",
                "exclusiveMinimum": 0.0,
            },
            "original_premium": {
                "type": "number",
                "description": (
                    "Original subject premium used to compute layer loss ratio "
                    "(recoveries / original_premium). If omitted, loss ratio is computed "
                    "as recoveries / (limit × event_count)."
                ),
                "exclusiveMinimum": 0.0,
            },
            "reinstatement_premium_pct": {
                "type": "number",
                "description": (
                    "Reinstatement premium rate as % of the original layer premium for each dollar "
                    "of limit consumed. E.g., 100 = 100% pro-rata reinstatement. Must be >= 0."
                ),
                "default": 0.0,
                "minimum": 0.0,
            },
            "xol_rate_on_line_pct": {
                "type": "number",
                "description": (
                    "Original layer premium as % of the layer limit (rate on line). "
                    "Used to compute reinstatement premium. Required if reinstatement_premium_pct > 0."
                ),
                "default": 0.0,
                "minimum": 0.0,
                "maximum": 100.0,
            },
        },
        "required": ["ground_up_losses", "attachment", "limit"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "total_recovery": {"type": "number", "description": "Sum of all per-occurrence recoveries."},
            "layer_loss_ratio_pct": {
                "type": "number",
                "description": "total_recovery / original_premium × 100 (or vs. limit×count if no premium given).",
            },
            "frequency_of_attachment_pct": {
                "type": "number",
                "description": "Percentage of occurrences that pierced the attachment point.",
            },
            "average_severity_in_layer": {
                "type": "number",
                "description": "Average recovery amount per attaching occurrence.",
            },
            "max_single_recovery": {"type": "number", "description": "Largest single-occurrence recovery."},
            "reinstatement_premium": {
                "type": "number",
                "description": "Reinstatement premium owed = recoveries × (xol_rol / 100) × (reinstatement_pct / 100).",
            },
            "net_recovery": {"type": "number", "description": "total_recovery - reinstatement_premium."},
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def excess_of_loss_calculator(
    ground_up_losses: list[float],
    attachment: float,
    limit: float,
    original_premium: float | None = None,
    reinstatement_premium_pct: float = 0.0,
    xol_rate_on_line_pct: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Compute XL per-occurrence recoveries and aggregate layer statistics.

    Per-occurrence recovery formula:
      recovery_i = min(max(ground_up_loss_i - attachment, 0), limit)

    Reinstatement premium (standard Lloyd's/London market convention):
      reinstatement_premium = total_recovery / limit × original_layer_premium × reinstatement_rate/100
    where original_layer_premium = limit × xol_rate_on_line_pct / 100.

    Layer loss ratio denominator:
      If original_premium is provided: total_recovery / original_premium
      Otherwise: total_recovery / (limit × len(ground_up_losses))

    Args:
        ground_up_losses: List of per-occurrence gross losses. Each must be >= 0.
        attachment: Per-occurrence retention point. Must be >= 0.
        limit: Layer limit per occurrence. Must be > 0.
        original_premium: Subject premium for loss ratio; optional.
        reinstatement_premium_pct: Reinstatement rate as % of original layer premium; default 0.0.
        xol_rate_on_line_pct: Layer rate-on-line (% of limit); used for reinstatement calculation.

    Returns:
        dict with status "success" and XL layer analytics, or status "error".
    """
    try:
        if not ground_up_losses:
            raise ValueError("ground_up_losses must not be empty")
        if attachment < 0:
            raise ValueError(f"attachment must be >= 0, got {attachment}")
        if limit <= 0:
            raise ValueError(f"limit must be positive, got {limit}")
        if reinstatement_premium_pct < 0:
            raise ValueError(f"reinstatement_premium_pct must be >= 0, got {reinstatement_premium_pct}")
        if xol_rate_on_line_pct < 0:
            raise ValueError(f"xol_rate_on_line_pct must be >= 0, got {xol_rate_on_line_pct}")
        for i, loss in enumerate(ground_up_losses):
            if loss < 0:
                raise ValueError(f"ground_up_losses[{i}]={loss} must be >= 0")

        recoveries: list[float] = []
        for loss in ground_up_losses:
            in_layer = max(loss - attachment, 0.0)
            recovered = min(in_layer, limit)
            recoveries.append(recovered)

        attaching = [r for r in recoveries if r > 0]
        total_recovery = sum(recoveries)
        attach_count = len(attaching)
        frequency = attach_count / len(ground_up_losses)
        avg_severity = total_recovery / attach_count if attach_count > 0 else 0.0
        max_recovery = max(recoveries) if recoveries else 0.0

        # Layer loss ratio: prefer original_premium denominator; fall back to limit × events
        if original_premium is not None and original_premium > 0:
            layer_loss_ratio = total_recovery / original_premium
        else:
            denominator = limit * len(ground_up_losses)
            layer_loss_ratio = total_recovery / denominator if denominator > 0 else 0.0

        # Reinstatement premium (pro-rata reinstatement based on limit consumed)
        original_layer_premium = limit * xol_rate_on_line_pct / 100.0
        reinstatement_premium = (
            (total_recovery / limit) * original_layer_premium * reinstatement_premium_pct / 100.0
            if limit > 0
            else 0.0
        )
        net_recovery = total_recovery - reinstatement_premium

        return {
            "status": "success",
            "total_recovery": round(total_recovery, 2),
            "layer_loss_ratio_pct": round(layer_loss_ratio * 100, 2),
            "frequency_of_attachment_pct": round(frequency * 100, 2),
            "average_severity_in_layer": round(avg_severity, 2),
            "max_single_recovery": round(max_recovery, 2),
            "reinstatement_premium": round(reinstatement_premium, 2),
            "net_recovery": round(net_recovery, 2),
            "timestamp": get_iso_timestamp(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as exc:
        log_lesson(f"excess_of_loss_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": get_iso_timestamp()}
