"""Compute NAV for tokenized funds using asset and liability inputs.
Outputs per-token NAV and leverage metrics."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Sequence
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "tokenized_fund_nav_calculator",
    "description": "Aggregates asset values minus liabilities to derive NAV per RWA token.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "asset_values": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of asset fair values",
            },
            "liabilities": {"type": "number", "description": "Total liabilities"},
            "token_supply": {"type": "number", "description": "Token units outstanding"},
        },
        "required": ["asset_values", "liabilities", "token_supply"],
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


def tokenized_fund_nav_calculator(
    asset_values: Sequence[float],
    liabilities: float,
    token_supply: float,
    **_: Any,
) -> dict[str, Any]:
    """Calculate NAV per token.

    Args:
        asset_values: Fair values of fund assets.
        liabilities: Total liabilities outstanding.
        token_supply: Token count outstanding.

    Returns:
        Dict containing NAV, per-token value, and leverage.
    """
    try:
        total_assets = sum(asset_values)
        nav = total_assets - liabilities
        if token_supply <= 0:
            raise ValueError("token_supply must be positive")
        nav_per_token = nav / token_supply
        leverage = liabilities / total_assets * 100 if total_assets else 0.0
        data = {
            "total_assets": round(total_assets, 2),
            "nav": round(nav, 2),
            "nav_per_token": round(nav_per_token, 4),
            "leverage_pct": round(leverage, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("tokenized_fund_nav_calculator failure: %s", exc)
        log_lesson(f"tokenized_fund_nav_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
