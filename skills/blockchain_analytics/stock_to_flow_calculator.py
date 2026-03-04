
"""
Executive Summary: Evaluates PlanB's stock-to-flow scarcity model for a given asset price.
Inputs: circulating_supply (float), annual_production_rate (float), current_price (float)
Outputs: sf_ratio (float), model_price (float), deviation_from_model_pct (float), scarcity_percentile (str)
MCP Tool Name: stock_to_flow_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "stock_to_flow_calculator",
    "description": "Applies the PlanB stock-to-flow regression to estimate model price and scarcity context.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "circulating_supply": {
                "type": "number",
                "description": "Total circulating supply of the asset in native units."
            },
            "annual_production_rate": {
                "type": "number",
                "description": "Annualized new issuance of tokens or coins in native units."
            },
            "current_price": {
                "type": "number",
                "description": "Spot price of the asset in USD for deviation analysis."
            }
        },
        "required": ["circulating_supply", "annual_production_rate", "current_price"]
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


def stock_to_flow_calculator(**kwargs: Any) -> dict:
    """Implements the classic BTC stock-to-flow regression (PlanB, 2019)."""
    try:
        for field in ("circulating_supply", "annual_production_rate", "current_price"):
            if field not in kwargs:
                raise ValueError(f"Missing required field {field}")
        circulating_supply = float(kwargs["circulating_supply"])
        annual_production_rate = float(kwargs["annual_production_rate"])
        current_price = float(kwargs["current_price"])
        if circulating_supply <= 0 or annual_production_rate <= 0 or current_price <= 0:
            raise ValueError("All inputs must be positive numbers")
        sf_ratio = circulating_supply / annual_production_rate
        model_price = math.exp(-1.84 + 3.36 * math.log(sf_ratio))
        deviation_from_model_pct = (current_price - model_price) / model_price * 100
        if sf_ratio < 10:
            scarcity_percentile = "young asset (<50% of BTC scarcity history)"
        elif sf_ratio < 30:
            scarcity_percentile = "mid-cycle scarcity"
        else:
            scarcity_percentile = "post-halving scarcity comparable to gold"
        return {
            "status": "success",
            "data": {
                "sf_ratio": sf_ratio,
                "model_price": model_price,
                "deviation_from_model_pct": deviation_from_model_pct,
                "scarcity_percentile": scarcity_percentile,
                "disclaimer": "Stock-to-flow remains contested and should be complemented with demand-side data."
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"stock_to_flow_calculator failed: {e}")
        _log_lesson(f"stock_to_flow_calculator: {e}")
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
