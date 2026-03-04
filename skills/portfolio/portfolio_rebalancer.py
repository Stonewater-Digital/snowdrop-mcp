"""Generate pending portfolio rebalance orders."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "portfolio_rebalancer",
    "description": "Compares target weights vs current positions and builds pending trade list.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "current_positions": {"type": "array", "items": {"type": "object"}},
            "target_weights": {"type": "object"},
            "total_portfolio_value": {"type": "number"},
            "min_trade_threshold": {"type": "number", "default": 50.0},
        },
        "required": ["current_positions", "target_weights", "total_portfolio_value"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
    },
}


def portfolio_rebalancer(
    current_positions: list[dict[str, Any]],
    target_weights: dict[str, float],
    total_portfolio_value: float,
    min_trade_threshold: float = 50.0,
    **_: Any,
) -> dict[str, Any]:
    """Return buy/sell instructions flagged for Thunder approval."""
    try:
        if total_portfolio_value <= 0:
            raise ValueError("total_portfolio_value must be positive")
        current_map = {pos["asset"]: pos for pos in current_positions}
        trades: list[dict[str, Any]] = []
        for asset, target_weight in target_weights.items():
            target_value = total_portfolio_value * target_weight
            current_value = float(current_map.get(asset, {}).get("value", 0.0))
            delta = target_value - current_value
            if abs(delta) < min_trade_threshold:
                continue
            trades.append(
                {
                    "asset": asset,
                    "action": "buy" if delta > 0 else "sell",
                    "amount_usd": round(abs(delta), 2),
                    "target_weight": target_weight,
                }
            )
        data = {
            "trades": trades,
            "execution": "pending_thunder_approval",
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("portfolio_rebalancer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
