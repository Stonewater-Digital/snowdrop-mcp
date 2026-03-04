"""Assess supply/demand balance for base metals."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable

TOOL_META: dict[str, Any] = {
    "name": "metals_supply_demand_analyzer",
    "description": (
        "Builds supply/demand surplus or deficit tallies for base metals, "
        "computes inventory coverage in months, and flags deficit conditions."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "metals": {
                "type": "array",
                "description": "List of metals with supply and demand data.",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Metal name (e.g. 'copper', 'aluminum').",
                        },
                        "mine_supply_mtons": {
                            "type": "number",
                            "description": "Annual mine supply in metric tonnes (must be >= 0).",
                        },
                        "scrap_supply_mtons": {
                            "type": "number",
                            "default": 0.0,
                            "description": "Annual scrap/secondary supply in metric tonnes.",
                        },
                        "demand_mtons": {
                            "type": "number",
                            "description": "Annual total demand in metric tonnes (must be >= 0).",
                        },
                        "inventory_weeks": {
                            "type": "number",
                            "default": 6,
                            "description": "Exchange + producer inventory in weeks of demand. Defaults to 6.",
                        },
                    },
                    "required": ["name", "mine_supply_mtons", "demand_mtons"],
                },
                "minItems": 1,
            }
        },
        "required": ["metals"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "balances": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "total_supply_mtons": {"type": "number"},
                        "demand_mtons": {"type": "number"},
                        "surplus_deficit_mtons": {"type": "number"},
                        "inventory_coverage_months": {"type": "number"},
                        "deficit_flag": {"type": "boolean"},
                        "tight_flag": {"type": "boolean"},
                    },
                },
            },
            "deficit_share": {"type": "number"},
            "timestamp": {"type": "string"},
        },
    },
}


def metals_supply_demand_analyzer(metals: Iterable[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return balance metrics for each metal.

    Args:
        metals: Iterable of metal dicts with mine_supply_mtons, optional scrap_supply_mtons,
            demand_mtons, and optional inventory_weeks.

    Returns:
        dict with status, per-metal balance metrics, and aggregate deficit_share.

    Formulas:
        total_supply = mine_supply + scrap_supply
        surplus_deficit = total_supply - demand  (positive = surplus, negative = deficit)
        inventory_coverage_months = inventory_weeks / (52/12) = inventory_weeks * 12 / 52

    Tight flag: inventory coverage < 4 weeks (~1 month), regardless of balance direction.
    """
    try:
        metal_list = list(metals)
        if not metal_list:
            raise ValueError("metals cannot be empty")

        balances = []
        for metal in metal_list:
            name = str(metal["name"])
            mine_supply = float(metal["mine_supply_mtons"])
            scrap_supply = float(metal.get("scrap_supply_mtons", 0.0))
            demand = float(metal["demand_mtons"])
            inv_weeks = float(metal.get("inventory_weeks", 6))

            if mine_supply < 0:
                raise ValueError(f"mine_supply_mtons must be >= 0 for '{name}'")
            if demand < 0:
                raise ValueError(f"demand_mtons must be >= 0 for '{name}'")

            total_supply = mine_supply + scrap_supply
            balance = total_supply - demand
            # Convert inventory weeks to months: weeks * (12/52)
            inv_months = inv_weeks * (12.0 / 52.0)

            balances.append(
                {
                    "name": name,
                    "total_supply_mtons": round(total_supply, 2),
                    "demand_mtons": round(demand, 2),
                    "surplus_deficit_mtons": round(balance, 2),
                    "inventory_coverage_months": round(inv_months, 2),
                    "deficit_flag": balance < 0,
                    "tight_flag": inv_weeks < 4.0,
                }
            )

        deficit_count = sum(1 for item in balances if item["deficit_flag"])
        deficit_share = deficit_count / len(balances)

        return {
            "status": "success",
            "balances": balances,
            "deficit_share": round(deficit_share, 3),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("metals_supply_demand_analyzer", str(exc))
        return {
            "status": "error",
            "error": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
