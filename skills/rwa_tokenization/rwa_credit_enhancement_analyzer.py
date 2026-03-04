"""Evaluate credit enhancement sufficiency for RWA pools.
Sums subordination, reserves, and insurance relative to expected losses."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "rwa_credit_enhancement_analyzer",
    "description": "Measures expected loss coverage from subordination, reserves, and insurance protections.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "pool_balance": {"type": "number", "description": "Outstanding asset pool balance"},
            "expected_loss_pct": {"type": "number", "description": "Expected loss percent"},
            "subordination_pct": {"type": "number", "description": "Junior tranche subordination percent"},
            "reserve_pct": {"type": "number", "description": "Cash reserve percent", "default": 0},
            "insurance_pct": {"type": "number", "description": "Insurance coverage percent", "default": 0},
        },
        "required": ["pool_balance", "expected_loss_pct", "subordination_pct"],
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


def rwa_credit_enhancement_analyzer(
    pool_balance: float,
    expected_loss_pct: float,
    subordination_pct: float,
    reserve_pct: float = 0.0,
    insurance_pct: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Compute enhancement coverage multiples.

    Args:
        pool_balance: Balance of underlying assets.
        expected_loss_pct: Expected loss percent of pool.
        subordination_pct: Subordination available ahead of seniors.
        reserve_pct: Cash reserves as percent of pool.
        insurance_pct: External insurance coverage percent.

    Returns:
        Dict with coverage multiples and deficit warnings.
    """
    try:
        enhancement_pct = subordination_pct + reserve_pct + insurance_pct
        expected_loss_amount = pool_balance * expected_loss_pct / 100
        enhancement_amount = pool_balance * enhancement_pct / 100
        coverage_multiple = enhancement_amount / expected_loss_amount if expected_loss_amount else float("inf")
        data = {
            "enhancement_pct": round(enhancement_pct, 2),
            "expected_loss_amount": round(expected_loss_amount, 2),
            "enhancement_amount": round(enhancement_amount, 2),
            "coverage_multiple": round(coverage_multiple, 2) if coverage_multiple != float("inf") else float("inf"),
            "adequacy_flag": coverage_multiple >= 1.25,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("rwa_credit_enhancement_analyzer failure: %s", exc)
        log_lesson(f"rwa_credit_enhancement_analyzer: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
