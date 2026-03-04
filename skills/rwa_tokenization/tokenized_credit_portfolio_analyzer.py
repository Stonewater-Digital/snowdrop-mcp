"""Analyze tokenized credit portfolios for yield and loss metrics.
Computes weighted yields, expected loss, and stress coverage."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Sequence
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "tokenized_credit_portfolio_analyzer",
    "description": "Aggregates RWA credit exposures to derive yield, expected loss, and coverage statistics.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "exposures": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "balance": {"type": "number"},
                        "coupon_pct": {"type": "number"},
                        "pd_pct": {"type": "number", "description": "Probability of default"},
                        "lgd_pct": {"type": "number", "description": "Loss given default"},
                    },
                    "required": ["balance", "coupon_pct", "pd_pct", "lgd_pct"],
                },
                "description": "Per-loan details",
            }
        },
        "required": ["exposures"],
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


def tokenized_credit_portfolio_analyzer(
    exposures: Sequence[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    """Compute portfolio yield and loss metrics.

    Args:
        exposures: Loan-level details.

    Returns:
        Payload with weighted average coupon, expected loss, and credit enhancement guidance.
    """
    try:
        total_balance = sum(float(exp.get("balance", 0)) for exp in exposures)
        if total_balance <= 0:
            raise ValueError("exposures must include positive balances")
        weighted_coupon = 0.0
        expected_loss = 0.0
        for exp in exposures:
            balance = float(exp.get("balance", 0))
            share = balance / total_balance
            weighted_coupon += share * float(exp.get("coupon_pct", 0))
            pd = float(exp.get("pd_pct", 0)) / 100
            lgd = float(exp.get("lgd_pct", 0)) / 100
            expected_loss += balance * pd * lgd
        expected_loss_pct = expected_loss / total_balance * 100
        excess_spread = weighted_coupon - expected_loss_pct
        data = {
            "weighted_coupon_pct": round(weighted_coupon, 2),
            "expected_loss_pct": round(expected_loss_pct, 2),
            "excess_spread_pct": round(excess_spread, 2),
            "enhancement_recommendation_pct": round(max(expected_loss_pct * 1.2, 0), 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("tokenized_credit_portfolio_analyzer failure: %s", exc)
        log_lesson(f"tokenized_credit_portfolio_analyzer: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
