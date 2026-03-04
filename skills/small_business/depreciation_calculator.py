"""
Executive Smary: Generates depreciation schedules across multiple accounting methods.
Inputs: asset_cost (float), salvage_value (float), useful_life_years (int), method (str)
Outputs: annual_schedule (list), total_depreciation (float), method_comparison (dict)
MCP Tool Name: depreciation_calculator
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

logger = logging.getLogger("snowdrop.skills")

METHODS = {"straight_line", "declining_balance", "macrs", "sum_of_years"}

TOOL_META = {
    "name": "depreciation_calculator",
    "description": (
        "Produces annual depreciation schedules for straight-line, declining balance, "
        "MACRS (simplified), and sum-of-years methods."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "asset_cost": {"type": "number", "description": "Original asset cost."},
            "salvage_value": {"type": "number", "description": "Residual value at end of life."},
            "useful_life_years": {"type": "number", "description": "Asset useful life in years."},
            "method": {
                "type": "string",
                "description": "Depreciation method: straight_line, declining_balance, macrs, or sum_of_years.",
            },
        },
        "required": ["asset_cost", "salvage_value", "useful_life_years", "method"],
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


def depreciation_calculator(**kwargs: Any) -> dict:
    """Return year-by-year depreciation schedule for the requested method."""
    try:
        cost = float(kwargs["asset_cost"])
        salvage = float(kwargs["salvage_value"])
        life = int(kwargs["useful_life_years"])
        method = str(kwargs["method"]).strip().lower()

        if method not in METHODS:
            raise ValueError("Unsupported method")

        comparison = {
            "straight_line": _straight_line(cost, salvage, life),
            "declining_balance": _declining_balance(cost, salvage, life),
            "macrs": _macrs(cost, salvage, life),
            "sum_of_years": _sum_of_years(cost, salvage, life),
        }
        schedule = comparison[method]
        total_dep = sum(item["depreciation"] for item in schedule)

        return {
            "status": "success",
            "data": {
                "annual_schedule": schedule,
                "total_depreciation": total_dep,
                "method_comparison": {k: sum(entry["depreciation"] for entry in v) for k, v in comparison.items()},
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"depreciation_calculator failed: {e}")
        _log_lesson(f"depreciation_calculator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _straight_line(cost: float, salvage: float, life: int) -> List[Dict[str, float]]:
    dep = (cost - salvage) / life
    schedule = []
    book = cost
    accumulated = 0.0
    for year in range(1, life + 1):
        book -= dep
        accumulated += dep
        schedule.append({"year": year, "depreciation": dep, "accumulated": accumulated, "book_value": max(book, salvage)})
    return schedule


def _declining_balance(cost: float, salvage: float, life: int, factor: float = 2.0) -> List[Dict[str, float]]:
    rate = factor / life
    schedule = []
    book = cost
    accumulated = 0.0
    for year in range(1, life + 1):
        depreciation = min((book * rate), book - salvage)
        book -= depreciation
        accumulated += depreciation
        schedule.append({"year": year, "depreciation": depreciation, "accumulated": accumulated, "book_value": book})
    return schedule


def _macrs(cost: float, salvage: float, life: int) -> List[Dict[str, float]]:
    schedule = []
    book = cost
    accumulated = 0.0
    rate = 1 / life
    for year in range(1, life + 1):
        depreciation = min(book * rate * 1.5, book - salvage)
        book -= depreciation
        accumulated += depreciation
        schedule.append({"year": year, "depreciation": depreciation, "accumulated": accumulated, "book_value": book})
    return schedule


def _sum_of_years(cost: float, salvage: float, life: int) -> List[Dict[str, float]]:
    schedule = []
    sum_years = life * (life + 1) / 2
    book = cost
    accumulated = 0.0
    depreciable = cost - salvage
    for year in range(life):
        factor = (life - year) / sum_years
        depreciation = depreciable * factor
        book -= depreciation
        accumulated += depreciation
        schedule.append({"year": year + 1, "depreciation": depreciation, "accumulated": accumulated, "book_value": book})
    return schedule


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
