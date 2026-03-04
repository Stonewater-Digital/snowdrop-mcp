"""Wash sale rule checker.
Detects purchase/sale pairs that trigger IRS wash sale disallowance.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "wash_sale_rule_checker",
    "description": "Checks transaction logs for wash sales inside 30-day windows.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "transactions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "date_offset_days": {"type": "number"},
                        "action": {"type": "string", "enum": ["buy", "sell"]},
                        "symbol": {"type": "string"},
                        "shares": {"type": "number"},
                    },
                    "required": ["date_offset_days", "action", "symbol", "shares"],
                },
            }
        },
        "required": ["transactions"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def wash_sale_rule_checker(transactions: Sequence[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return flagged wash sale pairs."""
    try:
        sells = [tx for tx in transactions if tx["action"] == "sell"]
        buys = [tx for tx in transactions if tx["action"] == "buy"]
        flags = []
        for sell in sells:
            for buy in buys:
                if sell["symbol"] == buy["symbol"] and abs(sell["date_offset_days"] - buy["date_offset_days"]) <= 30:
                    quantity = min(sell["shares"], buy["shares"])
                    flags.append(
                        {
                            "symbol": sell["symbol"],
                            "sell_day": sell["date_offset_days"],
                            "buy_day": buy["date_offset_days"],
                            "shares": quantity,
                        }
                    )
        data = {
            "wash_sales": flags,
            "flagged_count": len(flags),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("wash_sale_rule_checker failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
