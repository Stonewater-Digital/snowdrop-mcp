"""
Executive Smary: Estimates valuation ranges using revenue and EBITDA multiples by stage and sector.
Inputs: annual_revenue (float), ebitda (float), growth_rate (float), industry_sector (str), stage (str)
Outputs: revenue_multiple_range (tuple), ebitda_multiple_range (tuple), implied_valuation_range (tuple), comparable_context (dict)
MCP Tool Name: startup_valuation_multiples
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, Tuple

logger = logging.getLogger("snowdrop.skills")

STAGE_MULTIPLES = {
    "seed": 4.0,
    "series_a": 6.0,
    "series_b": 8.0,
    "growth": 10.0,
}

SECTOR_EBITDA = {
    "saas": 18.0,
    "fintech": 16.0,
    "marketplace": 12.0,
    "consumer": 10.0,
    "hardware": 8.0,
}


def _range(center: float, spread: float = 0.2) -> Tuple[float, float]:
    return center * (1 - spread), center * (1 + spread)


TOOL_META = {
    "name": "startup_valuation_multiples",
    "description": (
        "Applies growth-adjusted revenue multiples and sector EBITDA comparables to "
        "produce valuation ranges and comparable context notes."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "annual_revenue": {
                "type": "number",
                "description": "Latest annualized revenue run rate.",
            },
            "ebitda": {
                "type": "number",
                "description": "Trailing twelve months EBITDA (can be negative).",
            },
            "growth_rate": {
                "type": "number",
                "description": "Year-over-year revenue growth as decimal.",
            },
            "industry_sector": {
                "type": "string",
                "description": "Sector label (saas, fintech, marketplace, consumer, hardware).",
            },
            "stage": {
                "type": "string",
                "description": "seed, series_a, series_b, or growth.",
            },
        },
        "required": ["annual_revenue", "ebitda", "growth_rate", "industry_sector", "stage"],
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


def startup_valuation_multiples(**kwargs: Any) -> dict:
    """Estimate revenue and EBITDA multiple-based valuation ranges."""
    try:
        annual_revenue = float(kwargs["annual_revenue"])
        ebitda = float(kwargs["ebitda"])
        growth_rate = float(kwargs["growth_rate"])
        industry = str(kwargs["industry_sector"]).strip().lower()
        stage = str(kwargs["stage"]).strip().lower()

        if stage not in STAGE_MULTIPLES:
            raise ValueError("stage must be seed, series_a, series_b, or growth")

        base_multiple = STAGE_MULTIPLES[stage]
        growth_adjustment = 1 + (growth_rate - 0.3)
        revenue_multiple = max(base_multiple * growth_adjustment, 1.0)
        revenue_range = _range(revenue_multiple)

        sector_multiple = SECTOR_EBITDA.get(industry, 10.0)
        ebitda_range = _range(sector_multiple)

        revenue_valuation_range = (annual_revenue * revenue_range[0], annual_revenue * revenue_range[1])
        ebitda_valuation_range = (
            ebitda * ebitda_range[0],
            ebitda * ebitda_range[1],
        )

        implied_low = max(revenue_valuation_range[0], ebitda_valuation_range[0])
        implied_high = max(revenue_valuation_range[1], ebitda_valuation_range[1])

        comparable_context: Dict[str, Any] = {
            "stage_multiple_base": base_multiple,
            "sector_ebitda_multiple": sector_multiple,
            "growth_adjustment": growth_adjustment,
        }

        return {
            "status": "success",
            "data": {
                "revenue_multiple_range": revenue_range,
                "ebitda_multiple_range": ebitda_range,
                "implied_valuation_range": (implied_low, implied_high),
                "comparable_context": comparable_context,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"startup_valuation_multiples failed: {e}")
        _log_lesson(f"startup_valuation_multiples: {e}")
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
