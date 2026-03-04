"""
Executive Smary: Compares dollar-cost averaging to lump-sum investing over historical prices.
Inputs: total_investment (float), monthly_amount (float), historical_prices (list), period_months (int)
Outputs: dca_shares (float), dca_avg_cost (float), lump_sum_shares (float), dca_final_value (float), lump_sum_final_value (float), winner (str)
MCP Tool Name: dollar_cost_averaging_simulator
"""
import logging
from datetime import datetime, timezone
from typing import Any, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "dollar_cost_averaging_simulator",
    "description": (
        "Runs a dollar-cost averaging simulation against lump sum investing using a price "
        "series to determine ending values and identify the winning approach."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "total_investment": {
                "type": "number",
                "description": "Total capital available if investing lump sum.",
            },
            "monthly_amount": {
                "type": "number",
                "description": "Monthly contribution used for DCA strategy.",
            },
            "historical_prices": {
                "type": "array",
                "description": "List of historical monthly prices ordered chronologically.",
                "items": {"type": "number"},
            },
            "period_months": {
                "type": "number",
                "description": "Number of months to simulate (<= len prices).",
            },
        },
        "required": ["total_investment", "monthly_amount", "historical_prices", "period_months"],
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


def dollar_cost_averaging_simulator(**kwargs: Any) -> dict:
    """Compare DCA and lump sum investing over a series of monthly prices."""
    try:
        total_investment = float(kwargs["total_investment"])
        monthly_amount = float(kwargs["monthly_amount"])
        prices_input = kwargs["historical_prices"]
        period_months = int(kwargs["period_months"])

        if total_investment <= 0 or monthly_amount <= 0:
            raise ValueError("investment amounts must be positive")
        if not isinstance(prices_input, list) or period_months <= 0:
            raise ValueError("Provide valid historical price data and period_months")
        if period_months > len(prices_input):
            raise ValueError("period_months exceeds price history length")

        prices: List[float] = [float(p) for p in prices_input[:period_months]]
        dca_shares = sum((monthly_amount / price) for price in prices if price > 0)
        dca_invested = monthly_amount * period_months
        dca_avg_cost = dca_invested / dca_shares if dca_shares > 0 else 0.0
        last_price = prices[-1]
        dca_final_value = dca_shares * last_price

        lump_sum_shares = total_investment / prices[0] if prices[0] > 0 else 0.0
        lump_sum_final_value = lump_sum_shares * last_price

        winner = "dca" if dca_final_value > lump_sum_final_value else "lump_sum"

        return {
            "status": "success",
            "data": {
                "dca_shares": dca_shares,
                "dca_avg_cost": dca_avg_cost,
                "lump_sum_shares": lump_sum_shares,
                "dca_final_value": dca_final_value,
                "lump_sum_final_value": lump_sum_final_value,
                "winner": winner,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"dollar_cost_averaging_simulator failed: {e}")
        _log_lesson(f"dollar_cost_averaging_simulator: {e}")
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
