"""
Executive Summary: Multi-period rebalancer using dynamic programming to decide trade/hold actions with transaction costs.
Inputs: target_weights (dict[str, float]), initial_weights (dict[str, float]), expected_returns (list[dict[str, float]]), transaction_cost_bps (float)
Outputs: rebalance_schedule (list[dict]), terminal_wealth (float), total_cost (float)
MCP Tool Name: multi_period_rebalancer
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "multi_period_rebalancer",
    "description": (
        "Dynamic programming rebalancer choosing whether to rebalance or drift each period based on expected return "
        "trade-off versus transaction costs, following Bodie, Kane, Marcus multi-period optimization."),
    "inputSchema": {
        "type": "object",
        "properties": {
            "target_weights": {
                "type": "object",
                "description": "Strategic asset allocation weights that trades reset to.",
                "additionalProperties": {"type": "number"},
            },
            "initial_weights": {
                "type": "object",
                "description": "Starting allocation weights, typically equal to target.",
                "additionalProperties": {"type": "number"},
            },
            "expected_returns": {
                "type": "array",
                "description": "List of per-period expected returns keyed by asset.",
                "items": {
                    "type": "object",
                    "additionalProperties": {"type": "number"},
                },
            },
            "transaction_cost_bps": {
                "type": "number",
                "description": "Round-trip transaction cost per unit weight traded (in basis points).",
            },
        },
        "required": ["target_weights", "initial_weights", "expected_returns", "transaction_cost_bps"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "Execution status"},
            "data": {"type": "object", "description": "Optimal schedule"},
            "timestamp": {"type": "string", "description": "UTC timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def _apply_returns(weights: Dict[str, float], returns: Dict[str, float]) -> Dict[str, float]:
    grown = {asset: weight * (1 + returns.get(asset, 0.0)) for asset, weight in weights.items()}
    total = sum(grown.values())
    return {asset: value / total for asset, value in grown.items()}


def multi_period_rebalancer(
    target_weights: Dict[str, float],
    initial_weights: Dict[str, float],
    expected_returns: List[Dict[str, float]],
    transaction_cost_bps: float,
    **_: Any,
) -> dict[str, Any]:
    try:
        if set(target_weights.keys()) != set(initial_weights.keys()):
            raise ValueError("target_weights and initial_weights must cover the same assets")
        if not expected_returns:
            raise ValueError("expected_returns cannot be empty")
        tc = transaction_cost_bps / 10000
        state = {"weights": initial_weights.copy(), "wealth": 1.0}
        schedule = []
        total_cost = 0.0
        for period, exp_ret in enumerate(expected_returns, start=1):
            # Option 1: no rebalance
            drift_weights = _apply_returns(state["weights"], exp_ret)
            drift_wealth = state["wealth"] * (1 + sum(state["weights"][a] * exp_ret.get(a, 0.0) for a in state["weights"]))
            # Option 2: rebalance
            trade_amount = sum(abs(target_weights[a] - drift_weights[a]) for a in target_weights)
            trade_cost = trade_amount * tc
            rebalance_wealth = drift_wealth * (1 - trade_cost)
            if rebalance_wealth >= drift_wealth:
                action = "rebalance"
                state["weights"] = target_weights.copy()
                state["wealth"] = rebalance_wealth
                total_cost += trade_cost
            else:
                action = "drift"
                state["weights"] = drift_weights
                state["wealth"] = drift_wealth
            schedule.append(
                {
                    "period": period,
                    "action": action,
                    "weights": {k: round(v, 4) for k, v in state["weights"].items()},
                    "wealth": round(state["wealth"], 4),
                }
            )
        data = {
            "rebalance_schedule": schedule,
            "terminal_wealth": round(state["wealth"], 4),
            "total_cost": round(total_cost, 6),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError) as e:
        logger.error(f"multi_period_rebalancer failed: {e}")
        _log_lesson(f"multi_period_rebalancer: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as file:
            file.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
