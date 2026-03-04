
"""
Executive Summary: Evaluates token unlock timelines and sell pressure hotspots.
Inputs: unlock_events (list[dict]), circulating_supply (float), price (float)
Outputs: unlock_timeline (list[dict]), monthly_unlock_pct (float), sell_pressure_months (list[str]), dilution_impact (float), largest_single_unlock (dict)
MCP Tool Name: token_unlock_scheduler
"""
import logging
import math
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "token_unlock_scheduler",
    "description": "Analyzes vesting events to quantify unlock pace, dilution, and sell pressure windows.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "unlock_events": {
                "type": "array",
                "description": "Scheduled unlocks [{date, amount, category}].",
                "items": {
                    "type": "object",
                    "properties": {
                        "date": {"type": "string", "description": "ISO date"},
                        "amount": {"type": "number", "description": "Tokens unlocking"},
                        "category": {"type": "string", "description": "Team/investor/treasury/ecosystem"}
                    },
                    "required": ["date", "amount", "category"]
                }
            },
            "circulating_supply": {"type": "number", "description": "Current circulating supply."},
            "price": {"type": "number", "description": "Current token price in USD."}
        },
        "required": ["unlock_events", "circulating_supply", "price"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"}
        },
        "required": ["status", "timestamp"]
    }
}


def token_unlock_scheduler(**kwargs: Any) -> dict:
    """Aggregates unlock events into monthly dilution analytics."""
    try:
        events: Sequence[dict] = kwargs.get("unlock_events", [])
        circulating_supply = float(kwargs.get("circulating_supply", 0))
        price = float(kwargs.get("price", 0))
        if not events:
            raise ValueError("unlock_events must be provided")
        if circulating_supply <= 0 or price <= 0:
            raise ValueError("circulating_supply and price must be positive")
        monthly = defaultdict(float)
        total_unlock = 0.0
        largest_unlock = {"date": None, "amount": 0.0, "value_usd": 0.0, "category": None}
        for event in events:
            amount = float(event.get("amount", 0))
            date = event.get("date")
            category = event.get("category", "other")
            if amount <= 0:
                continue
            month_key = date[:7]
            monthly[month_key] += amount
            total_unlock += amount
            usd_value = amount * price
            if amount > largest_unlock["amount"]:
                largest_unlock = {"date": date, "amount": amount, "value_usd": usd_value, "category": category}
        unlock_timeline = [{"month": month, "amount": amt, "value_usd": amt * price} for month, amt in sorted(monthly.items())]
        monthly_unlock_pct = (total_unlock / circulating_supply) * 100
        sell_pressure_months = [entry["month"] for entry in unlock_timeline if entry["amount"] / circulating_supply > 0.02]
        dilution_impact = (total_unlock / (circulating_supply + total_unlock)) * 100
        return {
            "status": "success",
            "data": {
                "unlock_timeline": unlock_timeline,
                "monthly_unlock_pct": monthly_unlock_pct,
                "sell_pressure_months": sell_pressure_months,
                "dilution_impact": dilution_impact,
                "largest_single_unlock": largest_unlock
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"token_unlock_scheduler failed: {e}")
        _log_lesson(f"token_unlock_scheduler: {e}")
        return {"status": "error", "error": str(e), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as file:
            file.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
