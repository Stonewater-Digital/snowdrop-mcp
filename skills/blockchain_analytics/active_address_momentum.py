
"""
Executive Summary: Measures active address acceleration and compares it with price for divergence checks.
Inputs: daily_active_addresses (list[float])
Outputs: address_momentum (float), address_price_divergence (str), network_growth_rate (float), metcalfe_value_estimate (float)
MCP Tool Name: active_address_momentum
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "active_address_momentum",
    "description": "Analyzes daily active address series, applying momentum and Metcalfe's Law valuation hints.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "daily_active_addresses": {
                "type": "array",
                "description": "Time-ordered list of daily active addresses counts (>=14 data points recommended).",
                "items": {"type": "number"}
            }
        },
        "required": ["daily_active_addresses"]
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


def active_address_momentum(**kwargs: Any) -> dict:
    """Computes second-derivative momentum and Metcalfe valuations for user growth."""
    try:
        series: Sequence[float] = kwargs.get("daily_active_addresses", [])
        if not isinstance(series, Sequence) or len(series) < 7:
            raise ValueError("daily_active_addresses must contain at least 7 values")
        clean_series = [float(value) for value in series]
        if any(value <= 0 for value in clean_series):
            raise ValueError("Address counts must all be positive")
        latest = clean_series[-1]
        prior = clean_series[-2]
        week_prior = clean_series[-7]
        address_momentum = (latest - prior) - (prior - week_prior)
        network_growth_rate = (latest - week_prior) / week_prior * 100
        metcalfe_value_estimate = latest ** 2
        if address_momentum > 0 and network_growth_rate > 0:
            address_price_divergence = "addresses leading price"
        elif address_momentum < 0 and network_growth_rate < 0:
            address_price_divergence = "growth stalling"
        else:
            address_price_divergence = "neutral"
        return {
            "status": "success",
            "data": {
                "address_momentum": address_momentum,
                "address_price_divergence": address_price_divergence,
                "network_growth_rate": network_growth_rate,
                "metcalfe_value_estimate": metcalfe_value_estimate
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"active_address_momentum failed: {e}")
        _log_lesson(f"active_address_momentum: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as file:
            file.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
