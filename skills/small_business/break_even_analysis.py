"""
Executive Smary: Calculates the unit breakeven point and sensitivity to pricing/cost shifts.
Inputs: fixed_costs (float), variable_cost_per_unit (float), price_per_unit (float)
Outputs: break_even_units (float), break_even_revenue (float), contribution_margin (float), contribution_margin_ratio (float), what_if_table (list)
MCP Tool Name: break_even_analysis
"""
import logging
from datetime import datetime, timezone
from typing import Any, List, Dict

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "break_even_analysis",
    "description": (
        "Determines unit and revenue breakeven levels and runs pricing/cost what-if "
        "scenarios to stress test contribution margins."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "fixed_costs": {
                "type": "number",
                "description": "Total fixed costs per period.",
            },
            "variable_cost_per_unit": {
                "type": "number",
                "description": "Variable cost per unit sold.",
            },
            "price_per_unit": {
                "type": "number",
                "description": "Unit selling price.",
            },
        },
        "required": ["fixed_costs", "variable_cost_per_unit", "price_per_unit"],
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


def break_even_analysis(**kwargs: Any) -> dict:
    """Compute breakeven units/revenue and run what-if scenarios."""
    try:
        fixed_costs = float(kwargs["fixed_costs"])
        variable_cost = float(kwargs["variable_cost_per_unit"])
        price = float(kwargs["price_per_unit"])

        if price <= variable_cost:
            raise ValueError("price_per_unit must exceed variable_cost_per_unit")

        contribution_margin = price - variable_cost
        contribution_ratio = contribution_margin / price
        break_even_units = fixed_costs / contribution_margin
        break_even_revenue = break_even_units * price

        deltas = [-0.1, -0.05, 0, 0.05, 0.1]
        scenarios: List[Dict[str, Any]] = []
        for delta in deltas:
            scenario_price = price * (1 + delta)
            cm = scenario_price - variable_cost
            if cm <= 0:
                units = float("inf")
            else:
                units = fixed_costs / cm
            scenarios.append(
                {
                    "price_change_pct": delta,
                    "price": scenario_price,
                    "break_even_units": units,
                }
            )

        return {
            "status": "success",
            "data": {
                "break_even_units": break_even_units,
                "break_even_revenue": break_even_revenue,
                "contribution_margin": contribution_margin,
                "contribution_margin_ratio": contribution_ratio,
                "what_if_table": scenarios,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"break_even_analysis failed: {e}")
        _log_lesson(f"break_even_analysis: {e}")
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
