"""Measure wallet concentration risks for token distributions.
Computes Herfindahl and top-holder thresholds to flag governance capture."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Sequence
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "wallet_concentration_analyzer",
    "description": "Analyzes wallet balance data to quantify concentration risk and whale dominance.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "wallet_balances": {
                "type": "array",
                "items": {"type": "number"},
                "description": "Token balances per wallet",
            },
            "top_n_threshold": {
                "type": "integer",
                "description": "Number of wallets to aggregate in the top cohort",
                "default": 10,
            },
        },
        "required": ["wallet_balances"],
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


def wallet_concentration_analyzer(
    wallet_balances: Sequence[float],
    top_n_threshold: int = 10,
    **_: Any,
) -> dict[str, Any]:
    """Return top-holder share and HHI concentration.

    Args:
        wallet_balances: Balances for each wallet.
        top_n_threshold: Number of wallets to sum for whale share.

    Returns:
        Dict summarizing top-N share, median holdings, and HHI concentration.
    """
    try:
        balances = [max(float(balance), 0.0) for balance in wallet_balances]
        total_supply = sum(balances)
        if total_supply <= 0:
            raise ValueError("wallet_balances must contain positive totals")
        sorted_balances = sorted(balances, reverse=True)
        top_n = max(top_n_threshold, 1)
        top_share = sum(sorted_balances[:top_n]) / total_supply * 100
        shares = [balance / total_supply for balance in sorted_balances]
        hhi = sum(share ** 2 for share in shares)
        median_balance = sorted_balances[len(sorted_balances) // 2] if sorted_balances else 0.0
        data = {
            "top_n_share_pct": round(top_share, 2),
            "hhi": round(hhi, 4),
            "median_balance": round(median_balance, 4),
            "whale_risk_flag": top_share > 50 or hhi > 0.2,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("wallet_concentration_analyzer failure: %s", exc)
        log_lesson(f"wallet_concentration_analyzer: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
