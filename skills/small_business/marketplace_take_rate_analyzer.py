"""
Executive Smary: Evaluates marketplace take rate economics and buyer/seller unit value.
Inputs: gmv (float), revenue (float), buyer_cac (float), seller_cac (float), orders (int), avg_order_value (float)
Outputs: take_rate (float), contribution_per_order (float), buyer_ltv (float), seller_ltv (float), liquidity_score (float)
MCP Tool Name: marketplace_take_rate_analyzer
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "marketplace_take_rate_analyzer",
    "description": (
        "Calculates marketplace take rate, per-order contribution, estimated buyer/seller "
        "LTV, and a liquidity score using GMV, revenue, and CAC inputs."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "gmv": {
                "type": "number",
                "description": "Gross merchandise value processed in the period.",
            },
            "revenue": {
                "type": "number",
                "description": "Marketplace revenue (fees) over the same period.",
            },
            "buyer_cac": {
                "type": "number",
                "description": "Average cost to acquire one buyer.",
            },
            "seller_cac": {
                "type": "number",
                "description": "Average cost to onboard one seller.",
            },
            "orders": {
                "type": "number",
                "description": "Number of completed transactions.",
            },
            "avg_order_value": {
                "type": "number",
                "description": "Average GMV per order.",
            },
        },
        "required": ["gmv", "revenue", "buyer_cac", "seller_cac", "orders", "avg_order_value"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"},
        },
        "required": ["status", "timestamp"],
    },
}


def marketplace_take_rate_analyzer(**kwargs: Any) -> dict:
    """Assess marketplace take rate and per-order contribution metrics."""
    try:
        gmv = float(kwargs["gmv"])
        revenue = float(kwargs["revenue"])
        buyer_cac = float(kwargs["buyer_cac"])
        seller_cac = float(kwargs["seller_cac"])
        orders = int(kwargs["orders"])
        avg_order_value = float(kwargs["avg_order_value"])

        if gmv <= 0 or revenue <= 0 or orders <= 0:
            raise ValueError("gmv, revenue, and orders must be positive")

        take_rate = revenue / gmv
        contribution_per_order = (revenue - (buyer_cac + seller_cac)) / orders
        buyer_ltv = avg_order_value * take_rate * 12
        seller_ltv = avg_order_value * take_rate * 24
        liquidity_score = orders / (buyer_cac + seller_cac) if (buyer_cac + seller_cac) > 0 else float("inf")

        return {
            "status": "success",
            "data": {
                "take_rate": take_rate,
                "contribution_per_order": contribution_per_order,
                "buyer_ltv": buyer_ltv,
                "seller_ltv": seller_ltv,
                "liquidity_score": liquidity_score,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"marketplace_take_rate_analyzer failed: {e}")
        _log_lesson(f"marketplace_take_rate_analyzer: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
