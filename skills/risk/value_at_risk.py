"""Historical simulation Value at Risk utility."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "value_at_risk",
    "description": "Computes multi-level VaR and CVaR via historical simulation.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "positions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "asset": {"type": "string"},
                        "value": {"type": "number"},
                        "daily_returns": {
                            "type": "array",
                            "items": {"type": "number"},
                        },
                    },
                },
            },
            "confidence_levels": {
                "type": "array",
                "items": {"type": "number"},
                "default": [0.95, 0.99],
            },
            "holding_period_days": {"type": "integer", "default": 1},
        },
        "required": ["positions", "holding_period_days"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "portfolio_value": {"type": "number"},
                    "var": {"type": "object"},
                    "expected_shortfall": {"type": "object"},
                    "holding_period_days": {"type": "integer"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def value_at_risk(
    positions: list[dict[str, Any]],
    holding_period_days: int,
    confidence_levels: list[float] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Calculate VaR and CVaR for the provided portfolio."""

    try:
        if holding_period_days <= 0:
            raise ValueError("holding_period_days must be positive")
        if not positions:
            raise ValueError("positions must be supplied")
        confidence_levels = confidence_levels or [0.95, 0.99]
        if not all(0 < level < 1 for level in confidence_levels):
            raise ValueError("confidence_levels must be between 0 and 1")

        aggregate_value = sum(float(pos.get("value", 0)) for pos in positions)
        if aggregate_value <= 0:
            raise ValueError("Total portfolio value must be positive")

        min_length = min(len(pos.get("daily_returns", [])) for pos in positions)
        if min_length == 0:
            raise ValueError("Each position must include at least one daily return")

        daily_portfolio_returns: list[float] = []
        for day in range(min_length):
            weighted_sum = 0.0
            for pos in positions:
                value = float(pos.get("value", 0))
                daily_ret = float(pos["daily_returns"][day])
                weighted_sum += value * daily_ret
            daily_portfolio_returns.append(weighted_sum / aggregate_value)

        sorted_returns = sorted(daily_portfolio_returns)
        scale = math.sqrt(holding_period_days)
        var_results: dict[str, float] = {}
        es_results: dict[str, float] = {}
        for level in confidence_levels:
            percentile_index = max(0, int((1 - level) * len(sorted_returns)) - 1)
            var_point = sorted_returns[percentile_index]
            var_value = max(0.0, -var_point * aggregate_value * scale)

            cutoff = sorted_returns[: percentile_index + 1]
            if cutoff:
                es = -sum(cutoff) / len(cutoff) * aggregate_value * scale
            else:
                es = var_value

            level_key = f"{int(level * 100)}pct"
            var_results[level_key] = round(var_value, 2)
            es_results[level_key] = round(es, 2)

        data = {
            "portfolio_value": round(aggregate_value, 2),
            "var": var_results,
            "expected_shortfall": es_results,
            "holding_period_days": holding_period_days,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("value_at_risk", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    """Append a Ralph Wiggum lesson entry."""

    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
