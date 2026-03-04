"""Calculate duration metrics for tokenized bond positions.
Uses cash-flow schedules to compute Macaulay and modified duration."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Sequence
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "tokenized_bond_duration_calculator",
    "description": "Computes Macaulay and modified duration from cash-flow schedules of tokenized bonds.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "cash_flows": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "period_years": {"type": "number"},
                        "amount": {"type": "number"},
                    },
                    "required": ["period_years", "amount"],
                },
                "description": "Cash flow schedule for the bond",
            },
            "yield_pct": {"type": "number", "description": "Yield to maturity percent"},
        },
        "required": ["cash_flows", "yield_pct"],
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


def tokenized_bond_duration_calculator(
    cash_flows: Sequence[dict[str, float]],
    yield_pct: float,
    **_: Any,
) -> dict[str, Any]:
    """Compute Macaulay and modified duration.

    Args:
        cash_flows: Cash flows of the tokenized bond.
        yield_pct: Yield-to-maturity.

    Returns:
        Dict with price, Macaulay duration, and modified duration.
    """
    try:
        y = yield_pct / 100
        pv_total = 0.0
        weighted_sum = 0.0
        for flow in cash_flows:
            t = float(flow.get("period_years", 0))
            amount = float(flow.get("amount", 0))
            df = (1 + y) ** t
            pv = amount / df if df else 0.0
            pv_total += pv
            weighted_sum += t * pv
        if pv_total <= 0:
            raise ValueError("cash_flows must produce positive price")
        macaulay_duration = weighted_sum / pv_total
        modified_duration = macaulay_duration / (1 + y)
        data = {
            "price": round(pv_total, 4),
            "macaulay_duration": round(macaulay_duration, 4),
            "modified_duration": round(modified_duration, 4),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("tokenized_bond_duration_calculator failure: %s", exc)
        log_lesson(f"tokenized_bond_duration_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
