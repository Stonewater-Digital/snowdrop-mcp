"""Convert emission schedules into annualized inflation rates.
Simple helper for tokenomics reviews and treasury planning."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "token_inflation_rate_calculator",
    "description": "Transforms token emission inputs into annualized inflation metrics.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "current_supply": {"type": "number", "description": "Circulating supply"},
            "new_tokens_per_period": {"type": "number", "description": "Tokens emitted each period"},
            "periods_per_year": {"type": "number", "description": "Number of emission periods in a year"},
        },
        "required": ["current_supply", "new_tokens_per_period", "periods_per_year"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"},
            "error": {"type": "string"},
        },
    },
}


def token_inflation_rate_calculator(
    current_supply: float,
    new_tokens_per_period: float,
    periods_per_year: float,
    **_: Any,
) -> dict[str, Any]:
    """Compute annualized inflation from emission rate.

    Args:
        current_supply: Circulating float.
        new_tokens_per_period: Emissions per period.
        periods_per_year: Number of periods per year.

    Returns:
        Dict with inflation rate and supply projections.
    """
    try:
        if current_supply <= 0 or periods_per_year <= 0:
            raise ValueError("current_supply and periods_per_year must be positive")
        annual_emissions = new_tokens_per_period * periods_per_year
        inflation_pct = annual_emissions / current_supply * 100
        projected_supply = current_supply + annual_emissions
        data = {
            "annual_emissions": round(annual_emissions, 2),
            "inflation_pct": round(inflation_pct, 2),
            "projected_supply_next_year": round(projected_supply, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("token_inflation_rate_calculator failure: %s", exc)
        log_lesson(f"token_inflation_rate_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
