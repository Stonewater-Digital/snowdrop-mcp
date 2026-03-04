
"""
Executive Summary: Projects token inflation, burns, and time to max supply.
Inputs: current_supply (float), max_supply (float), emission_schedule (list[dict]), burn_rate (float)
Outputs: inflation_rate_current (float), inflation_rate_next_year (float), years_to_max_supply (float), supply_curve (list[dict]), real_inflation (float)
MCP Tool Name: token_supply_analyzer
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "token_supply_analyzer",
    "description": "Analyzes emission schedules and burn rates to forecast supply paths and inflation.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "current_supply": {"type": "number", "description": "Circulating supply today."},
            "max_supply": {"type": "number", "description": "Maximum supply cap."},
            "emission_schedule": {
                "type": "array",
                "description": "Future annual emissions [{year, new_tokens}].",
                "items": {
                    "type": "object",
                    "properties": {
                        "year": {"type": "number", "description": "Calendar year."},
                        "new_tokens": {"type": "number", "description": "Tokens minted that year."}
                    },
                    "required": ["year", "new_tokens"]
                }
            },
            "burn_rate": {"type": "number", "description": "Annual burn rate in tokens."}
        },
        "required": ["current_supply", "max_supply", "emission_schedule", "burn_rate"]
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


def token_supply_analyzer(**kwargs: Any) -> dict:
    """Models token supply growth net of burns using schedule inputs."""
    try:
        current_supply = float(kwargs.get("current_supply", 0))
        max_supply = float(kwargs.get("max_supply", 0))
        emission_schedule: Sequence[dict] = kwargs.get("emission_schedule", [])
        burn_rate = float(kwargs.get("burn_rate", 0))
        if current_supply <= 0 or max_supply <= 0 or burn_rate < 0:
            raise ValueError("current_supply/max_supply must be positive and burn_rate non-negative")
        if current_supply > max_supply:
            raise ValueError("current_supply cannot exceed max_supply")
        if not emission_schedule:
            raise ValueError("emission_schedule cannot be empty")
        sorted_schedule = sorted(emission_schedule, key=lambda item: item.get("year"))
        supply_curve = []
        headroom = max_supply - current_supply
        next_year_emission = sorted_schedule[0]["new_tokens"] if sorted_schedule else 0
        inflation_rate_current = (sorted_schedule[0]["new_tokens"] - burn_rate) / current_supply * 100
        inflation_rate_next_year = ((sorted_schedule[1]["new_tokens"] if len(sorted_schedule) > 1 else next_year_emission) - burn_rate) / current_supply * 100
        cumulative = current_supply
        years_to_max_supply = math.inf
        for entry in sorted_schedule:
            year = int(entry["year"])
            emission = float(entry["new_tokens"])
            net_emission = max(0.0, emission - burn_rate)
            cumulative = min(max_supply, cumulative + net_emission)
            supply_curve.append({"year": year, "projected_supply": cumulative})
            if cumulative >= max_supply and years_to_max_supply is math.inf:
                years_to_max_supply = year - datetime.now(timezone.utc).year
                break
        real_inflation = max(0.0, inflation_rate_current - (burn_rate / current_supply * 100))
        return {
            "status": "success",
            "data": {
                "inflation_rate_current": inflation_rate_current,
                "inflation_rate_next_year": inflation_rate_next_year,
                "years_to_max_supply": years_to_max_supply,
                "supply_curve": supply_curve,
                "real_inflation": real_inflation
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"token_supply_analyzer failed: {e}")
        _log_lesson(f"token_supply_analyzer: {e}")
        return {"status": "error", "error": str(e), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as file:
            file.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
