"""
Executive Smary: Values ending inventory and COGS under FIFO, LIFO, or weighted average.
Inputs: purchases (list), sales (list), method (str)
Outputs: ending_inventory_value (float), cogs (float), units_on_hand (float), method_comparison (dict), gross_profit_impact (float)
MCP Tool Name: inventory_valuation
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "inventory_valuation",
    "description": (
        "Runs FIFO, LIFO, and weighted-average calculations to derive COGS and ending "
        "inventory, highlighting gross profit differences between methods."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "purchases": {
                "type": "array",
                "description": "List of purchases {date, quantity, unit_cost}.",
                "items": {"type": "object"},
            },
            "sales": {
                "type": "array",
                "description": "List of sales {date, quantity}.",
                "items": {"type": "object"},
            },
            "method": {
                "type": "string",
                "description": "fifo, lifo, or weighted_avg.",
            },
        },
        "required": ["purchases", "sales", "method"],
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


def inventory_valuation(**kwargs: Any) -> dict:
    """Value inventory and COGS under requested costing methods."""
    try:
        purchases = kwargs["purchases"]
        sales = kwargs["sales"]
        method = str(kwargs["method"]).strip().lower()

        if method not in {"fifo", "lifo", "weighted_avg"}:
            raise ValueError("method must be fifo, lifo, or weighted_avg")

        comparator = {
            "fifo": _cost_flow(purchases, sales, lifo=False),
            "lifo": _cost_flow(purchases, sales, lifo=True),
            "weighted_avg": _weighted_average(purchases, sales),
        }

        primary = comparator[method]
        highest_gp = max(value["gross_profit"] for value in comparator.values())
        lowest_gp = min(value["gross_profit"] for value in comparator.values())

        return {
            "status": "success",
            "data": {
                "ending_inventory_value": primary["ending_value"],
                "cogs": primary["cogs"],
                "units_on_hand": primary["units_on_hand"],
                "method_comparison": comparator,
                "gross_profit_impact": highest_gp - lowest_gp,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError, KeyError) as e:
        logger.error(f"inventory_valuation failed: {e}")
        _log_lesson(f"inventory_valuation: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _cost_flow(purchases: List[Dict[str, Any]], sales: List[Dict[str, Any]], lifo: bool) -> Dict[str, float]:
    layers: List[Tuple[float, float]] = []
    for entry in sorted(purchases, key=lambda x: x["date"]):
        layers.append((float(entry["quantity"]), float(entry["unit_cost"])))
    cogs = 0.0
    revenue = 0.0
    for sale in sorted(sales, key=lambda x: x["date"]):
        qty_to_sell = float(sale["quantity"])
        revenue += qty_to_sell * float(sale.get("unit_price", layers[-1][1] * 1.2 if layers else 0))
        while qty_to_sell > 0 and layers:
            idx = -1 if lifo else 0
            qty, cost = layers[idx]
            take = min(qty, qty_to_sell)
            cogs += take * cost
            qty_to_sell -= take
            qty -= take
            if qty == 0:
                layers.pop(idx)
            else:
                layers[idx] = (qty, cost)
        if qty_to_sell > 0:
            raise ValueError("Sales exceed available inventory")
    ending_value = sum(qty * cost for qty, cost in layers)
    units_on_hand = sum(qty for qty, _ in layers)
    return {
        "ending_value": ending_value,
        "units_on_hand": units_on_hand,
        "cogs": cogs,
        "gross_profit": revenue - cogs,
    }


def _weighted_average(purchases: List[Dict[str, Any]], sales: List[Dict[str, Any]]) -> Dict[str, float]:
    total_qty = sum(float(p["quantity"]) for p in purchases)
    total_cost = sum(float(p["quantity"]) * float(p["unit_cost"]) for p in purchases)
    avg_cost = total_cost / total_qty if total_qty else 0.0
    total_sales_qty = sum(float(s["quantity"]) for s in sales)
    cogs = total_sales_qty * avg_cost
    revenue = sum(float(s["quantity"]) * float(s.get("unit_price", avg_cost * 1.2)) for s in sales)
    units_on_hand = total_qty - total_sales_qty
    ending_value = units_on_hand * avg_cost
    return {
        "ending_value": ending_value,
        "units_on_hand": units_on_hand,
        "cogs": cogs,
        "gross_profit": revenue - cogs,
    }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
