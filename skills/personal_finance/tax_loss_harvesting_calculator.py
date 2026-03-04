"""
Executive Smary: Estimates tax savings from harvesting capital losses and warns on wash sales.
Inputs: realized_gains (float), unrealized_losses (list), tax_bracket (float), state_rate (float)
Outputs: harvestable_losses (float), tax_savings (float), net_gains_after_harvest (float), carryforward_amount (float), wash_sale_warning_dates (list)
MCP Tool Name: tax_loss_harvesting_calculator
"""
import logging
from datetime import datetime, timedelta, timezone
from typing import Any, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "tax_loss_harvesting_calculator",
    "description": (
        "Aggregates available capital losses to offset realized gains, estimates tax "
        "savings (federal + state), and flags 30-day wash sale blackout periods."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "realized_gains": {
                "type": "number",
                "description": "Net realized capital gains so far this year.",
            },
            "unrealized_losses": {
                "type": "array",
                "description": "List of holdings with loss amounts and holding_period days.",
                "items": {"type": "object"},
            },
            "tax_bracket": {
                "type": "number",
                "description": "Marginal federal capital gains rate as decimal.",
            },
            "state_rate": {
                "type": "number",
                "description": "State tax rate applicable to capital gains.",
            },
        },
        "required": ["realized_gains", "unrealized_losses", "tax_bracket", "state_rate"],
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


def tax_loss_harvesting_calculator(**kwargs: Any) -> dict:
    """Quantify tax loss harvesting benefits and wash sale windows."""
    try:
        realized_gains = float(kwargs["realized_gains"])
        losses_input = kwargs["unrealized_losses"]
        tax_bracket = float(kwargs["tax_bracket"])
        state_rate = float(kwargs["state_rate"])

        if not isinstance(losses_input, list):
            raise ValueError("unrealized_losses must be a list")

        loss_values: List[float] = []
        warning_dates = []
        now = datetime.now(timezone.utc)
        for idx, holding in enumerate(losses_input):
            amount = float(holding["amount"])
            holding_period = int(holding.get("holding_period", 0))
            if amount <= 0:
                continue
            loss_values.append(amount)
            warning_dates.append(
                {
                    "loss_index": idx,
                    "no_repurchase_before": (now + timedelta(days=31)).isoformat(),
                    "holding_period_days": holding_period,
                }
            )

        harvestable = sum(loss_values)
        net_gains = realized_gains - harvestable
        carryforward = abs(net_gains) if net_gains < 0 else 0.0
        effective_rate = tax_bracket + state_rate
        tax_savings = min(harvestable, realized_gains) * effective_rate
        if net_gains < 0:
            tax_savings += min(3000, carryforward) * effective_rate

        return {
            "status": "success",
            "data": {
                "harvestable_losses": harvestable,
                "tax_savings": tax_savings,
                "net_gains_after_harvest": net_gains,
                "carryforward_amount": carryforward,
                "wash_sale_warning_dates": warning_dates,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"tax_loss_harvesting_calculator failed: {e}")
        _log_lesson(f"tax_loss_harvesting_calculator: {e}")
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
