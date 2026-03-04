"""Run stress scenarios for RWA portfolios.
Applies haircut and default assumptions to estimate downside loss."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "rwa_portfolio_stress_tester",
    "description": "Applies price haircuts and default shocks to estimate stressed RWA portfolio values.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "portfolio_value": {"type": "number", "description": "Current market value"},
            "haircut_pct": {"type": "number", "description": "Market value haircut percent"},
            "default_rate_pct": {"type": "number", "description": "Default rate applied to assets"},
            "lgd_pct": {"type": "number", "description": "Loss given default percent", "default": 60},
        },
        "required": ["portfolio_value", "haircut_pct", "default_rate_pct"],
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


def rwa_portfolio_stress_tester(
    portfolio_value: float,
    haircut_pct: float,
    default_rate_pct: float,
    lgd_pct: float = 60.0,
    **_: Any,
) -> dict[str, Any]:
    """Apply stress scenario.

    Args:
        portfolio_value: Base valuation of the assets.
        haircut_pct: Market price haircut.
        default_rate_pct: Percentage of assets defaulting.
        lgd_pct: Loss given default.

    Returns:
        Dict summarizing stress loss and remaining equity.
    """
    try:
        haircut_loss = portfolio_value * haircut_pct / 100
        credit_loss = portfolio_value * default_rate_pct / 100 * lgd_pct / 100
        stressed_value = portfolio_value - haircut_loss - credit_loss
        data = {
            "haircut_loss": round(haircut_loss, 2),
            "credit_loss": round(credit_loss, 2),
            "stressed_value": round(stressed_value, 2),
            "loss_pct": round((portfolio_value - stressed_value) / portfolio_value * 100 if portfolio_value else 0.0, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("rwa_portfolio_stress_tester failure: %s", exc)
        log_lesson(f"rwa_portfolio_stress_tester: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
