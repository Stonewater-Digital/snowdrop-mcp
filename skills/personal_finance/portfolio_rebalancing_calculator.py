"""
Executive Smary: Generates buy/sell trades to rebalance a portfolio to target weights.
Inputs: current_holdings (list), target_allocation (list), new_contribution (float)
Outputs: trades_needed (list), drift_analysis (list), tax_lot_considerations (list)
MCP Tool Name: portfolio_rebalancing_calculator
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "portfolio_rebalancing_calculator",
    "description": (
        "Compares current holdings with target allocations to produce trade "
        "instructions, drift metrics, and tax lot reminders for selling positions."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "current_holdings": {
                "type": "array",
                "description": "List of holdings with ticker and value fields.",
                "items": {"type": "object"},
            },
            "target_allocation": {
                "type": "array",
                "description": "Target weights expressed as percentage decimals per ticker.",
                "items": {"type": "object"},
            },
            "new_contribution": {
                "type": "number",
                "description": "Optional fresh cash to deploy before sales are triggered.",
            },
        },
        "required": ["current_holdings", "target_allocation"],
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


def portfolio_rebalancing_calculator(**kwargs: Any) -> dict:
    """Produce rebalance trades and drift diagnostics."""
    try:
        holdings_input = kwargs["current_holdings"]
        targets_input = kwargs["target_allocation"]
        new_contribution = float(kwargs.get("new_contribution", 0.0))

        if not isinstance(holdings_input, list) or not isinstance(targets_input, list):
            raise ValueError("current_holdings and target_allocation must be lists")

        holdings = {str(item["ticker"]).upper(): float(item["value"]) for item in holdings_input}
        total_value = sum(holdings.values()) + new_contribution
        if total_value <= 0:
            raise ValueError("Total portfolio value must be positive")

        targets = {str(item["ticker"]).upper(): float(item["pct"]) for item in targets_input}
        if abs(sum(targets.values()) - 1) > 0.01:
            raise ValueError("Target allocations should sum to 1.0")

        trades: List[Dict[str, Any]] = []
        drift_analysis: List[Dict[str, Any]] = []
        tax_considerations: List[Dict[str, Any]] = []

        for ticker, target_pct in targets.items():
            current_value = holdings.get(ticker, 0.0)
            target_value = total_value * target_pct
            drift = (current_value - target_value) / total_value
            action = None
            amount = 0.0
            if current_value < target_value:
                action = "buy"
                amount = target_value - current_value
            elif current_value > target_value:
                action = "sell"
                amount = current_value - target_value
                tax_considerations.append(
                    {
                        "ticker": ticker,
                        "note": "Review tax lots and holding periods before selling.",
                        "estimated_proceeds": amount,
                    }
                )
            if action:
                trades.append({"ticker": ticker, "action": action, "amount": amount})
            drift_analysis.append(
                {
                    "ticker": ticker,
                    "current_value": current_value,
                    "target_value": target_value,
                    "drift": drift,
                }
            )

        return {
            "status": "success",
            "data": {
                "trades_needed": trades,
                "drift_analysis": drift_analysis,
                "tax_lot_considerations": tax_considerations,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"portfolio_rebalancing_calculator failed: {e}")
        _log_lesson(f"portfolio_rebalancing_calculator: {e}")
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
