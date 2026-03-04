"""
Execuve Summary: Aggregates multiple sentiment components into a composite fear/greed score.
Inputs: market_momentum (float), market_breadth (float), put_call_ratio (float), junk_bond_demand (float), market_volatility (float), safe_haven_demand (float), stock_price_strength (float)
Outputs: composite_score (float), label (str), component_scores (dict)
MCP Tool Name: fear_greed_composite
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "fear_greed_composite",
    "description": "Combines multiple sentiment metrics into a 0-100 fear/greed composite score.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "market_momentum": {"type": "number", "description": "Momentum score (0-100)."},
            "market_breadth": {"type": "number", "description": "Breadth score (0-100)."},
            "put_call_ratio": {"type": "number", "description": "Inverse scaled PCR score (0-100)."},
            "junk_bond_demand": {"type": "number", "description": "Risk appetite via HY demand."},
            "market_volatility": {"type": "number", "description": "Volatility score (lower vol => higher score)."},
            "safe_haven_demand": {"type": "number", "description": "Demand for safe havens (inverse risk)."},
            "stock_price_strength": {"type": "number", "description": "Percent of stocks above moving averages."}
        },
        "required": ["market_momentum", "market_breadth", "put_call_ratio", "junk_bond_demand", "market_volatility", "safe_haven_demand", "stock_price_strength"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def fear_greed_composite(**kwargs: Any) -> dict:
    """Averages normalized component scores and labels the sentiment regime."""
    try:
        components = {key: kwargs.get(key) for key in TOOL_META["inputSchema"]["properties"].keys()}
        for name, value in components.items():
            if not isinstance(value, (int, float)):
                raise ValueError(f"{name} must be numeric (0-100)")
            components[name] = max(0, min(100, float(value)))
        composite_score = sum(components.values()) / len(components)
        if composite_score < 20:
            label = "extreme_fear"
        elif composite_score < 40:
            label = "fear"
        elif composite_score < 60:
            label = "neutral"
        elif composite_score < 80:
            label = "greed"
        else:
            label = "extreme_greed"

        return {
            "status": "success",
            "data": {
                "composite_score": composite_score,
                "label": label,
                "component_scores": components
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"fear_greed_composite failed: {e}")
        _log_lesson(f"fear_greed_composite: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
