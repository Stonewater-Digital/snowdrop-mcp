"""Optimizes stablecoin bridge routing from Optimism to Arbitrum with fee and latency heuristics."""
from __future__ import annotations

from typing import Any, Mapping

from skills.utils import _log_lesson, get_iso_timestamp


TOOL_META: dict[str, Any] = {
    "name": "optimism_to_arbitrum_stablecoin_bridge_optimizer",
    "description": "Optimizes stablecoin bridge routing from Optimism to Arbitrum with fee and latency heuristics.",
    "tier": "free",
    "inputSchema": {
    "type": "object",
    "properties": {
        "amount_usd": {
            "type": "number",
            "description": "Notional Size in USD."
        },
        "urgency": {
            "type": "string",
            "enum": [
                "low",
                "standard",
                "high"
            ],
            "description": "Speed requirement for the transfer."
        },
        "volatility_index": {
            "type": "number",
            "description": "Bridge volatility proxy between 0-2."
        }
    },
    "required": [
        "amount_usd",
        "urgency",
        "volatility_index"
    ]
},
    "outputSchema": {
    "type": "object",
    "properties": {
        "status": {
            "type": "string"
        },
        "data": {
            "type": "object"
        },
        "timestamp": {
            "type": "string"
        }
    }
},
}


def optimism_to_arbitrum_stablecoin_bridge_optimizer(metrics: Mapping[str, float | int | str]) -> dict[str, Any]:
    """Route stablecoin transfers from Optimism to Arbitrum."""

    try:
        for field in ("amount_usd", "urgency", "volatility_index"):
            if field not in metrics:
                raise ValueError(f"{field} is required")

        amount = float(metrics["amount_usd"])
        urgency = str(metrics["urgency"]).lower()
        volatility = float(metrics["volatility_index"])

        basis_points = 4.000
        fee_usd = 1.200 + amount * (basis_points / 10_000)
        latency = 87.500
        if urgency == "high":
            latency *= 0.85
            fee_usd *= 1.08
        elif urgency == "low":
            latency *= 1.15
            fee_usd *= 0.97

        liquidity_score = 1.000 - 0.2 * volatility
        if liquidity_score < 0.4:
            recommended = "Across"
            failover = "Connext"
        else:
            recommended = "Connext"
            failover = "Across"

        data = {
            "source": "Optimism",
            "target": "Arbitrum",
            "asset": "stablecoin",
            "estimated_fee_usd": round(fee_usd, 2),
            "projected_latency_seconds": round(latency * max(1 + volatility * 0.15, 0.5), 1),
            "recommended_router": recommended,
            "failover_router": failover,
            "liquidity_confidence": round(max(min(liquidity_score + 0.5, 1.0), 0), 3),
        }
        return {"status": "ok", "data": data, "timestamp": get_iso_timestamp()}
    except Exception as exc:
        _log_lesson("optimism_to_arbitrum_stablecoin_bridge_optimizer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": get_iso_timestamp(),
        }
