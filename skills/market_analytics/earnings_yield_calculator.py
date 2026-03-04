"""
Execuve Summary: Compares earnings yield versus Treasury yields per the Fed Model.
Inputs: eps (float), stock_price (float), treasury_10yr_yield (float)
Outputs: earnings_yield (float), pe_ratio (float), equity_risk_premium (float), fed_model_signal (str)
MCP Tool Name: earnings_yield_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "earnings_yield_calculator",
    "description": "Computes earnings yield (inverse P/E) and compares against the 10Y Treasury yield.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "eps": {"type": "number", "description": "Earnings per share."},
            "stock_price": {"type": "number", "description": "Current share price."},
            "treasury_10yr_yield": {"type": "number", "description": "10-year Treasury yield (decimal)."}
        },
        "required": ["eps", "stock_price", "treasury_10yr_yield"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def earnings_yield_calculator(**kwargs: Any) -> dict:
    """Calculates earnings yield, equity risk premium, and Fed Model signal."""
    try:
        eps = kwargs.get("eps")
        price = kwargs.get("stock_price")
        treasury = kwargs.get("treasury_10yr_yield")
        for label, value in (("eps", eps), ("stock_price", price), ("treasury_10yr_yield", treasury)):
            if not isinstance(value, (int, float)):
                raise ValueError(f"{label} must be numeric")
        if price <= 0 or eps <= 0:
            raise ValueError("eps and stock_price must be positive")

        earnings_yield = eps / price
        pe_ratio = price / eps
        equity_risk_premium = earnings_yield - treasury
        if equity_risk_premium > 0.02:
            signal = "stocks_cheap"
        elif equity_risk_premium < -0.02:
            signal = "stocks_expensive"
        else:
            signal = "neutral"

        return {
            "status": "success",
            "data": {
                "earnings_yield": earnings_yield,
                "pe_ratio": pe_ratio,
                "equity_risk_premium": equity_risk_premium,
                "fed_model_signal": signal
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"earnings_yield_calculator failed: {e}")
        _log_lesson(f"earnings_yield_calculator: {e}")
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
