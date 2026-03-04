"""Estimate impermanent loss for two-asset AMM LPs.
Supports scenario analysis across relative price moves."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import logging
import math

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "impermanent_loss_calculator",
    "description": "Computes impermanent loss percentage for constant product pools given price ratio shifts.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "initial_price_ratio": {"type": "number", "description": "Token A price / Token B price at deposit"},
            "ending_price_ratio": {"type": "number", "description": "Token A price / Token B price at evaluation"},
        },
        "required": ["initial_price_ratio", "ending_price_ratio"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"},
            "error": {"type": "string"},
        },
    },
}


def impermanent_loss_calculator(
    initial_price_ratio: float,
    ending_price_ratio: float,
    **_: Any,
) -> dict[str, Any]:
    """Calculate impermanent loss relative to HODL.

    Args:
        initial_price_ratio: Relative price at LP deposit.
        ending_price_ratio: Relative price at measurement time.

    Returns:
        Dict with impermanent loss percentage and relative value change.
    """
    try:
        if initial_price_ratio <= 0 or ending_price_ratio <= 0:
            raise ValueError("Price ratios must be positive")
        ratio_move = ending_price_ratio / initial_price_ratio
        sqrt_ratio = math.sqrt(ratio_move)
        lp_value_ratio = (2 * sqrt_ratio) / (1 + ratio_move)
        impermanent_loss_pct = (lp_value_ratio - 1) * 100
        data = {
            "price_ratio_change": round(ratio_move, 4),
            "lp_value_ratio": round(lp_value_ratio, 4),
            "impermanent_loss_pct": round(impermanent_loss_pct, 3),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("impermanent_loss_calculator failure: %s", exc)
        log_lesson(f"impermanent_loss_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
