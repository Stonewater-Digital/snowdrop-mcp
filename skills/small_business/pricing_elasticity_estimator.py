"""
Executive Smary: Estimates price elasticity from experiments and finds revenue/profit maximizing prices.
Inputs: current_price (float), current_volume (float), test_prices (list), test_volumes (list), unit_cost (float)
Outputs: price_elasticity (float), optimal_price (float), revenue_curve (list), max_revenue_price (float), profit_maximizing_price (float|None)
MCP Tool Name: pricing_elasticity_estimator
"""
import logging
from datetime import datetime, timezone
from math import log
from typing import Any, List, Optional

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "pricing_elasticity_estimator",
    "description": (
        "Uses observed price/volume pairs to estimate demand elasticity and recommends "
        "revenue/profit maximizing price points."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "current_price": {
                "type": "number",
                "description": "Existing list price.",
            },
            "current_volume": {
                "type": "number",
                "description": "Units sold at the current price.",
            },
            "test_prices": {
                "type": "array",
                "description": "List of tested prices.",
                "items": {"type": "number"},
            },
            "test_volumes": {
                "type": "array",
                "description": "List of observed volumes corresponding to test_prices.",
                "items": {"type": "number"},
            },
            "unit_cost": {
                "type": "number",
                "description": "Optional variable cost per unit for profit calculations.",
            },
        },
        "required": ["current_price", "current_volume", "test_prices", "test_volumes"],
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


def pricing_elasticity_estimator(**kwargs: Any) -> dict:
    """Estimate price elasticity and highlight revenue/profit optimal price points."""
    try:
        current_price = float(kwargs["current_price"])
        current_volume = float(kwargs["current_volume"])
        test_prices = [float(p) for p in kwargs["test_prices"]]
        test_volumes = [float(v) for v in kwargs["test_volumes"]]
        unit_cost: Optional[float] = kwargs.get("unit_cost")
        unit_cost_val = float(unit_cost) if unit_cost is not None else None

        if len(test_prices) != len(test_volumes) or len(test_prices) < 2:
            raise ValueError("test_prices and test_volumes must match and include >=2 entries")

        prices = [current_price] + test_prices
        volumes = [current_volume] + test_volumes

        # Elasticity via log-log regression
        log_prices = [log(p) for p in prices if p > 0]
        log_volumes = [log(volumes[i]) for i in range(len(prices)) if prices[i] > 0 and volumes[i] > 0]
        if len(log_prices) != len(log_volumes):
            raise ValueError("All prices and volumes must be positive")

        mean_lp = sum(log_prices) / len(log_prices)
        mean_lv = sum(log_volumes) / len(log_volumes)
        num = sum((lp - mean_lp) * (lv - mean_lv) for lp, lv in zip(log_prices, log_volumes))
        den = sum((lp - mean_lp) ** 2 for lp in log_prices)
        elasticity = num / den if den else 0.0

        revenue_curve: List[dict[str, float]] = []
        max_revenue = -1.0
        max_revenue_price = prices[0]
        max_profit = -1.0
        profit_price = None

        for price, volume in zip(prices, volumes):
            revenue = price * volume
            revenue_curve.append({"price": price, "volume": volume, "revenue": revenue})
            if revenue > max_revenue:
                max_revenue = revenue
                max_revenue_price = price
            if unit_cost_val is not None:
                profit = (price - unit_cost_val) * volume
                if profit > max_profit:
                    max_profit = profit
                    profit_price = price

        optimal_price = max_revenue_price

        return {
            "status": "success",
            "data": {
                "price_elasticity": elasticity,
                "optimal_price": optimal_price,
                "revenue_curve": revenue_curve,
                "max_revenue_price": max_revenue_price,
                "profit_maximizing_price": profit_price,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"pricing_elasticity_estimator failed: {e}")
        _log_lesson(f"pricing_elasticity_estimator: {e}")
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
