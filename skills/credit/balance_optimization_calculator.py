"""Optimize balance distribution across credit cards to minimize interest and utilization.

MCP Tool Name: balance_optimization_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "balance_optimization_calculator",
    "description": "Suggest balance redistribution across credit cards to minimize interest while keeping per-card utilization below 30%.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "cards": {
                "type": "array",
                "description": "List of credit cards.",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Card name."},
                        "limit": {"type": "number", "description": "Credit limit."},
                        "balance": {"type": "number", "description": "Current balance."},
                        "rate": {"type": "number", "description": "Annual rate as decimal."},
                    },
                    "required": ["name", "limit", "balance", "rate"],
                },
            },
        },
        "required": ["cards"],
    },
}


def balance_optimization_calculator(cards: list[dict[str, Any]]) -> dict[str, Any]:
    """Optimize balance distribution across credit cards."""
    try:
        if not cards:
            return {
                "status": "error",
                "data": {"error": "cards list must not be empty."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        total_balance = sum(c["balance"] for c in cards)
        total_limit = sum(c["limit"] for c in cards)

        # Current state
        current_interest = sum(c["balance"] * c["rate"] for c in cards)
        current_cards = []
        for c in cards:
            util = (c["balance"] / c["limit"] * 100) if c["limit"] > 0 else 0
            current_cards.append({
                "name": c["name"],
                "balance": c["balance"],
                "limit": c["limit"],
                "rate_pct": round(c["rate"] * 100, 2),
                "utilization_pct": round(util, 2),
            })

        # Optimized: move balances to lowest-rate cards first, respecting 30% limit
        sorted_cards = sorted(cards, key=lambda x: x["rate"])
        remaining = total_balance
        optimized = []
        for c in sorted_cards:
            max_balance = c["limit"] * 0.30
            assigned = min(remaining, max_balance)
            remaining -= assigned
            optimized.append({
                "name": c["name"],
                "suggested_balance": round(assigned, 2),
                "limit": c["limit"],
                "rate_pct": round(c["rate"] * 100, 2),
                "utilization_pct": round((assigned / c["limit"] * 100) if c["limit"] > 0 else 0, 2),
            })

        # If remaining > 0, distribute overflow to lowest-rate cards (exceeding 30%)
        if remaining > 0:
            for item in optimized:
                card_limit = item["limit"]
                current_assigned = item["suggested_balance"]
                can_add = card_limit - current_assigned
                add = min(remaining, can_add)
                item["suggested_balance"] = round(current_assigned + add, 2)
                item["utilization_pct"] = round(
                    (item["suggested_balance"] / card_limit * 100) if card_limit > 0 else 0, 2
                )
                remaining -= add
                if remaining <= 0:
                    break

        optimized_interest = sum(
            o["suggested_balance"] * (o["rate_pct"] / 100) for o in optimized
        )
        interest_savings = current_interest - optimized_interest

        return {
            "status": "ok",
            "data": {
                "total_balance": round(total_balance, 2),
                "total_limit": round(total_limit, 2),
                "current_annual_interest": round(current_interest, 2),
                "current_cards": current_cards,
                "optimized_cards": optimized,
                "optimized_annual_interest": round(optimized_interest, 2),
                "annual_interest_savings": round(interest_savings, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
