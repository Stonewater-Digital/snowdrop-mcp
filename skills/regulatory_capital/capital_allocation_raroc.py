"""
Executive Summary: RAROC-based capital allocation engine computing EVA per business unit.
Inputs: business_units (list[dict]), cost_of_capital_pct (float)
Outputs: raroc_by_unit (list[dict]), optimal_allocation (list[str]), portfolio_raroc_pct (float)
MCP Tool Name: capital_allocation_raroc
"""
import logging
from datetime import datetime, timezone
from typing import Any, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "capital_allocation_raroc",
    "description": "Calculates RAROC and economic value added per business line for regulatory capital planning.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "business_units": {
                "type": "array",
                "description": "Units with revenue, expected loss, and economic capital.",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Business unit name"},
                        "revenue": {"type": "number", "description": "Net revenue"},
                        "expected_loss": {"type": "number", "description": "Expected loss charge"},
                        "economic_capital": {"type": "number", "description": "Economic capital allocated"},
                    },
                    "required": ["name", "revenue", "expected_loss", "economic_capital"],
                },
            },
            "cost_of_capital_pct": {"type": "number", "description": "Target cost of capital (hurdle rate)."},
        },
        "required": ["business_units", "cost_of_capital_pct"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "RAROC results"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def capital_allocation_raroc(
    business_units: List[dict[str, Any]],
    cost_of_capital_pct: float,
    **_: Any,
) -> dict[str, Any]:
    try:
        if not business_units:
            raise ValueError("business_units required")
        raroc_results = []
        total_economic = sum(unit["economic_capital"] for unit in business_units)
        portfolio_raroc = 0.0
        for unit in business_units:
            capital = unit["economic_capital"]
            income = unit["revenue"] - unit["expected_loss"]
            raroc = income / capital if capital else 0.0
            eva = income - capital * (cost_of_capital_pct / 100.0)
            raroc_results.append(
                {
                    "name": unit["name"],
                    "raroc_pct": round(raroc * 100, 2),
                    "economic_value_added": round(eva, 2),
                    "capital": round(capital, 2),
                }
            )
            portfolio_raroc += raroc * capital
        portfolio_raroc = portfolio_raroc / total_economic if total_economic else 0.0
        optimal = [res["name"] for res in raroc_results if res["raroc_pct"] >= cost_of_capital_pct]
        data = {
            "raroc_by_unit": raroc_results,
            "portfolio_raroc_pct": round(portfolio_raroc * 100, 2),
            "optimal_allocation": optimal,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"capital_allocation_raroc failed: {e}")
        _log_lesson(f"capital_allocation_raroc: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as handle:
            handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
