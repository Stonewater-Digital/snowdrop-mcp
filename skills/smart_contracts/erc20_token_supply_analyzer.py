"""Summarize ERC-20 token supply buckets and free float ratios.
Highlights treasury and locked positions that constrain circulation."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "erc20_token_supply_analyzer",
    "description": "Breaks total supply into circulating, treasury, and locked components to monitor float.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "total_supply": {"type": "number", "description": "Fully diluted token supply"},
            "treasury_tokens": {"type": "number", "description": "Tokens held by treasury wallets"},
            "burned_tokens": {"type": "number", "description": "Tokens sent to burn addresses"},
            "locked_tokens": {"type": "number", "description": "Tokens locked in vesting or contracts"},
        },
        "required": ["total_supply", "treasury_tokens", "burned_tokens", "locked_tokens"],
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


def erc20_token_supply_analyzer(
    total_supply: float,
    treasury_tokens: float,
    burned_tokens: float,
    locked_tokens: float,
    **_: Any,
) -> dict[str, Any]:
    """Decompose supply stack into circulating and constrained buckets.

    Args:
        total_supply: Fully diluted supply reported on-chain.
        treasury_tokens: Governance-controlled reserve tokens.
        burned_tokens: Permanently removed tokens.
        locked_tokens: Tokens in vesting, escrow, or staking lockups.

    Returns:
        Response dict containing free-float ratios and risk signals.
    """
    try:
        circulating = max(total_supply - treasury_tokens - burned_tokens - locked_tokens, 0)
        burn_ratio = burned_tokens / total_supply * 100 if total_supply else 0.0
        float_ratio = circulating / total_supply * 100 if total_supply else 0.0
        data = {
            "circulating_supply": round(circulating, 2),
            "treasury_ratio_pct": round(treasury_tokens / total_supply * 100 if total_supply else 0.0, 2),
            "burn_ratio_pct": round(burn_ratio, 2),
            "locked_ratio_pct": round(locked_tokens / total_supply * 100 if total_supply else 0.0, 2),
            "free_float_ratio_pct": round(float_ratio, 2),
            "supply_health_flag": float_ratio >= 35,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("erc20_token_supply_analyzer failure: %s", exc)
        log_lesson(f"erc20_token_supply_analyzer: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
