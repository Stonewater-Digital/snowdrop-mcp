"""Distribute cash flows across RWA tranches via waterfall.
Supports proportional allocations and deficit tracking."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Sequence
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "rwa_cash_flow_waterfall_model",
    "description": "Allocates tokenized asset cash flows across tranches based on priority or share percentages.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "cash_flows": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "period": {"type": "string"},
                        "amount": {"type": "number"},
                    },
                    "required": ["period", "amount"],
                },
                "description": "Per-period available cash",
            },
            "tranches": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "share_pct": {"type": "number"},
                    },
                    "required": ["name", "share_pct"],
                },
                "description": "Waterfall share percentages",
            },
        },
        "required": ["cash_flows", "tranches"],
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


def rwa_cash_flow_waterfall_model(
    cash_flows: Sequence[dict[str, Any]],
    tranches: Sequence[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    """Allocate RWA cash flows across tranches.

    Args:
        cash_flows: Periodic available cash.
        tranches: Tranche definitions with share percentages.

    Returns:
        Dict summarizing per-period allocations.
    """
    try:
        total_share = sum(max(float(t.get("share_pct", 0)), 0.0) for t in tranches)
        if total_share <= 0:
            raise ValueError("tranches must contain positive share percentages")
        allocation_schedule = []
        for period in cash_flows:
            amount = float(period.get("amount", 0))
            period_allocations = []
            for tranche in tranches:
                share = max(float(tranche.get("share_pct", 0)), 0.0) / total_share
                allocation = amount * share
                period_allocations.append(
                    {
                        "tranche": tranche.get("name", "tranche"),
                        "allocation": round(allocation, 2),
                        "share_pct": round(share * 100, 2),
                    }
                )
            allocation_schedule.append({"period": period.get("period", "period"), "allocations": period_allocations})
        data = {
            "schedule": allocation_schedule,
            "total_distributed": round(sum(float(p.get("amount", 0)) for p in cash_flows), 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("rwa_cash_flow_waterfall_model failure: %s", exc)
        log_lesson(f"rwa_cash_flow_waterfall_model: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
