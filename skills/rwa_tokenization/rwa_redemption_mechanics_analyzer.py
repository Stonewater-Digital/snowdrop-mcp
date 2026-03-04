"""Review redemption mechanics for tokenized products.
Scores investor friendliness across notice, frequency, and penalties."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "rwa_redemption_mechanics_analyzer",
    "description": "Evaluates redemption policies including frequency, notice, and penalties for tokenized RWAs.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "redemption_frequency_days": {"type": "number", "description": "How often redemptions are allowed"},
            "notice_period_days": {"type": "number", "description": "Required notice before redemption"},
            "penalty_pct": {"type": "number", "description": "Penalty percent for early exit", "default": 0},
            "liquidity_buffer_pct": {"type": "number", "description": "Portfolio liquidity buffer percent", "default": 0},
        },
        "required": ["redemption_frequency_days", "notice_period_days"],
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


def rwa_redemption_mechanics_analyzer(
    redemption_frequency_days: float,
    notice_period_days: float,
    penalty_pct: float = 0.0,
    liquidity_buffer_pct: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Score redemption mechanics.

    Args:
        redemption_frequency_days: Frequency of redemption windows.
        notice_period_days: Required notice for redemptions.
        penalty_pct: Penalty charged on early exits.
        liquidity_buffer_pct: Liquid assets supporting redemptions.

    Returns:
        Dict with investor access score and warnings.
    """
    try:
        frequency_score = max(30 - redemption_frequency_days, 0) / 30
        notice_score = max(30 - notice_period_days, 0) / 30
        penalty_score = max(10 - penalty_pct, 0) / 10
        buffer_score = liquidity_buffer_pct / 50
        composite = min(frequency_score * 0.3 + notice_score * 0.3 + penalty_score * 0.2 + buffer_score * 0.2, 1.0)
        data = {
            "investor_access_score": round(composite, 3),
            "lockup_tier": "open" if composite > 0.7 else "periodic" if composite > 0.4 else "locked",
            "redemption_frequency_days": redemption_frequency_days,
            "notice_period_days": notice_period_days,
            "penalty_pct": penalty_pct,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("rwa_redemption_mechanics_analyzer failure: %s", exc)
        log_lesson(f"rwa_redemption_mechanics_analyzer: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
