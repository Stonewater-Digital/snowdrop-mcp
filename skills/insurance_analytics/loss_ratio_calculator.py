"""Loss ratio calculator.

Computes incurred loss ratio, ALAE-loaded ratio, and ultimate developed loss ratio
from earned premium and loss figures — core P&C actuarial metrics.
"""
from __future__ import annotations

from typing import Any

from skills.utils import get_iso_timestamp, log_lesson

TOOL_META: dict[str, Any] = {
    "name": "loss_ratio_calculator",
    "description": (
        "Calculates incurred loss ratio, ALAE-inclusive ratio, and development-adjusted "
        "ultimate loss ratio from earned premium and loss components."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "incurred_losses": {
                "type": "number",
                "description": "Incurred losses (paid + case reserves, excluding ALAE). Must be >= 0.",
                "minimum": 0.0,
            },
            "earned_premium": {
                "type": "number",
                "description": "Net earned premium for the period. Must be > 0.",
                "exclusiveMinimum": 0.0,
            },
            "alae": {
                "type": "number",
                "description": "Allocated loss adjustment expenses (defense costs, etc.). Must be >= 0.",
                "default": 0.0,
                "minimum": 0.0,
            },
            "development_factor": {
                "type": "number",
                "description": (
                    "Cumulative loss development factor (LDF) to ultimate. "
                    "1.0 = fully developed; >1.0 = immature losses still developing. Must be >= 1.0."
                ),
                "default": 1.0,
                "minimum": 1.0,
            },
        },
        "required": ["incurred_losses", "earned_premium"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "loss_ratio_pct": {"type": "number", "description": "Incurred losses / earned premium × 100."},
            "alae_loss_ratio_pct": {"type": "number", "description": "(Incurred losses + ALAE) / earned premium × 100."},
            "ultimate_loss_ratio_pct": {"type": "number", "description": "Developed ultimate losses / earned premium × 100."},
            "ultimate_losses": {"type": "number", "description": "Incurred losses × development_factor."},
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def loss_ratio_calculator(
    incurred_losses: float,
    earned_premium: float,
    alae: float = 0.0,
    development_factor: float = 1.0,
    **_: Any,
) -> dict[str, Any]:
    """Compute incurred, ALAE-loaded, and ultimate loss ratios.

    Args:
        incurred_losses: Paid + case reserves, net of salvage/subrogation. Must be >= 0.
        earned_premium: Net earned premium for the period. Must be > 0.
        alae: Allocated loss adjustment expenses; default 0.0.
        development_factor: Cumulative LDF to ultimate; default 1.0 (fully developed).

    Returns:
        dict with status "success" and loss ratio metrics, or status "error".
    """
    try:
        if earned_premium <= 0:
            raise ValueError(f"earned_premium must be positive, got {earned_premium}")
        if incurred_losses < 0:
            raise ValueError(f"incurred_losses must be >= 0, got {incurred_losses}")
        if alae < 0:
            raise ValueError(f"alae must be >= 0, got {alae}")
        if development_factor < 1.0:
            raise ValueError(f"development_factor must be >= 1.0, got {development_factor}")

        loss_ratio = incurred_losses / earned_premium
        alae_loss_ratio = (incurred_losses + alae) / earned_premium
        ultimate_losses = incurred_losses * development_factor
        ultimate_ratio = ultimate_losses / earned_premium

        return {
            "status": "success",
            "loss_ratio_pct": round(loss_ratio * 100, 2),
            "alae_loss_ratio_pct": round(alae_loss_ratio * 100, 2),
            "ultimate_loss_ratio_pct": round(ultimate_ratio * 100, 2),
            "ultimate_losses": round(ultimate_losses, 2),
            "timestamp": get_iso_timestamp(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as exc:
        log_lesson(f"loss_ratio_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": get_iso_timestamp()}
