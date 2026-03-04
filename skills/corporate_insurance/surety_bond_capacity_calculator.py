"""Surety bond capacity calculator.
Uses working capital, net worth, and backlog to size bonding line.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "surety_bond_capacity_calculator",
    "description": "Estimates surety bonding capacity from financial statements.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "working_capital": {"type": "number"},
            "net_worth": {"type": "number"},
            "backlog": {"type": "number"},
            "bonding_multiplier": {"type": "number", "default": 10.0},
        },
        "required": ["working_capital", "net_worth", "backlog"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def surety_bond_capacity_calculator(
    working_capital: float,
    net_worth: float,
    backlog: float,
    bonding_multiplier: float = 10.0,
    **_: Any,
) -> dict[str, Any]:
    """Return single and aggregate bond capacity estimates."""
    try:
        single_project = min(working_capital * bonding_multiplier, net_worth * 0.5)
        aggregate = single_project * 3
        backlog_ratio = backlog / aggregate if aggregate else 0.0
        status = "overextended" if backlog_ratio > 1 else "balanced"
        data = {
            "single_project_capacity": round(single_project, 2),
            "aggregate_capacity": round(aggregate, 2),
            "backlog_to_capacity_ratio": round(backlog_ratio, 2),
            "status": status,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("surety_bond_capacity_calculator failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
