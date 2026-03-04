"""
Executive Smary: Suggests a target asset allocation using age and risk tolerance glide paths.
Inputs: age (int), risk_tolerance (str), retirement_age (int), portfolio_value (float)
Outputs: recommended_allocation (dict), rebalancing (dict), glide_path_to_retirement (list)
MCP Tool Name: asset_allocation_by_age
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

logger = logging.getLogger("snowdrop.skills")

RISK_ADJUSTMENTS = {"conservative": -0.1, "moderate": 0.0, "aggressive": 0.1}

TOOL_META = {
    "name": "asset_allocation_by_age",
    "description": (
        "Applies a modified age-based formula to recommend stock/bond/cash/alt "
        "allocations and produces a glide path toward retirement."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "age": {
                "type": "number",
                "description": "Current age of the investor.",
            },
            "risk_tolerance": {
                "type": "string",
                "description": "conservative, moderate, or aggressive.",
            },
            "retirement_age": {
                "type": "number",
                "description": "Target retirement age.",
            },
            "portfolio_value": {
                "type": "number",
                "description": "Total investable assets.",
            },
        },
        "required": ["age", "risk_tolerance", "retirement_age", "portfolio_value"],
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


def asset_allocation_by_age(**kwargs: Any) -> dict:
    """Generate an allocation recommendation based on age and risk tolerance."""
    try:
        age = int(kwargs["age"])
        risk_tolerance = str(kwargs["risk_tolerance"]).strip().lower()
        retirement_age = int(kwargs["retirement_age"])
        portfolio_value = float(kwargs["portfolio_value"])

        if risk_tolerance not in RISK_ADJUSTMENTS:
            raise ValueError("risk_tolerance must be conservative, moderate, or aggressive")
        if age <= 0 or retirement_age <= age:
            raise ValueError("Provide valid age and retirement_age greater than age")
        if portfolio_value < 0:
            raise ValueError("portfolio_value must be non-negative")

        base_stock = max(0.2, min(0.9, 1 - age / 110))
        stock_weight = base_stock + RISK_ADJUSTMENTS[risk_tolerance]
        stock_weight = max(0.2, min(0.95, stock_weight))
        bond_weight = min(0.7, 1 - stock_weight - 0.05)
        cash_weight = 0.05
        alt_weight = max(0.0, 1 - (stock_weight + bond_weight + cash_weight))

        allocation = {
            "stocks": round(stock_weight, 3),
            "bonds": round(bond_weight, 3),
            "cash": round(cash_weight, 3),
            "alternatives": round(alt_weight, 3),
        }

        target_values = {k: v * portfolio_value for k, v in allocation.items()}
        rebalancing = {
            "target_values": target_values,
            "guidance": "Shift toward bonds and cash as you approach retirement annually.",
        }

        years_to_retirement = retirement_age - age
        glide_path: List[Dict[str, Any]] = []
        for i in range(0, years_to_retirement + 1, max(years_to_retirement // 5, 1)):
            year_age = age + i
            step_stock = max(0.2, stock_weight - 0.02 * i)
            glide_path.append(
                {
                    "age": year_age,
                    "stocks": round(step_stock, 3),
                    "bonds": round(1 - step_stock - cash_weight - alt_weight, 3),
                    "cash": cash_weight,
                    "alternatives": alt_weight,
                }
            )

        return {
            "status": "success",
            "data": {
                "recommended_allocation": allocation,
                "rebalancing": rebalancing,
                "glide_path_to_retirement": glide_path,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"asset_allocation_by_age failed: {e}")
        _log_lesson(f"asset_allocation_by_age: {e}")
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
