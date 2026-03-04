
"""
Executive Summary: Quantifies whether net token supply is inflationary or deflationary.
Inputs: total_supply (float), circulating_supply (float), burn_events (list[dict]), annual_emission (float)
Outputs: net_inflation_rate (float), annualized_burn_rate (float), deflationary (bool), supply_trajectory (list[dict]), years_to_halve (float)
MCP Tool Name: token_burn_deflation
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "token_burn_deflation",
    "description": "Analyzes burn events vs emissions to classify token supply behavior.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "total_supply": {"type": "number", "description": "Total supply minted"},
            "circulating_supply": {"type": "number", "description": "Current circulating supply"},
            "burn_events": {
                "type": "array",
                "description": "List of burn events {date, amount}",
                "items": {
                    "type": "object",
                    "properties": {
                        "date": {"type": "string", "description": "ISO date"},
                        "amount": {"type": "number", "description": "Tokens burned"}
                    },
                    "required": ["date", "amount"]
                }
            },
            "annual_emission": {"type": "number", "description": "Tokens minted per year"}
        },
        "required": ["total_supply", "circulating_supply", "burn_events", "annual_emission"]
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


def token_burn_deflation(**kwargs: Any) -> dict:
    """Compares burns with emission to determine net inflation path."""
    try:
        total_supply = float(kwargs.get("total_supply", 0))
        circulating_supply = float(kwargs.get("circulating_supply", 0))
        burn_events: Sequence[dict] = kwargs.get("burn_events", [])
        annual_emission = float(kwargs.get("annual_emission", 0))
        if total_supply <= 0 or circulating_supply <= 0 or annual_emission < 0:
            raise ValueError("Supply and emission inputs must be positive")
        total_burned_annual = sum(float(event.get("amount", 0)) for event in burn_events)
        annualized_burn_rate = total_burned_annual / circulating_supply * 100
        net_inflation_rate = ((annual_emission - total_burned_annual) / circulating_supply) * 100
        deflationary = net_inflation_rate < 0
        supply_trajectory = []
        supply = circulating_supply
        for year in range(5):
            supply = max(0.0, supply + annual_emission - total_burned_annual)
            supply_trajectory.append({"year_ahead": year + 1, "projected_supply": supply})
        years_to_halve = math.inf
        if deflationary and all(entry["projected_supply"] < circulating_supply for entry in supply_trajectory):
            drop_per_year = circulating_supply - supply_trajectory[0]["projected_supply"]
            if drop_per_year > 0:
                years_to_halve = (circulating_supply / 2) / drop_per_year
        return {
            "status": "success",
            "data": {
                "net_inflation_rate": net_inflation_rate,
                "annualized_burn_rate": annualized_burn_rate,
                "deflationary": deflationary,
                "supply_trajectory": supply_trajectory,
                "years_to_halve": years_to_halve
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"token_burn_deflation failed: {e}")
        _log_lesson(f"token_burn_deflation: {e}")
        return {"status": "error", "error": str(e), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as file:
            file.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
