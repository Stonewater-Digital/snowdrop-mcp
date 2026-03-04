"""Builds Curve liquidity rebalance plans for yield rotations."""
from __future__ import annotations

from typing import Any, Mapping

from skills.utils import _log_lesson, get_iso_timestamp


TOOL_META: dict[str, Any] = {
    "name": "curve_liquidity_rebalance_playbook",
    "description": "Builds Curve liquidity rebalance plans for yield rotations.",
    "tier": "free",
    "inputSchema": {
    "type": "object",
    "properties": {
        "principal_usd": {
            "type": "number",
            "description": "Capital deployed into the strategy."
        },
        "base_yield_apr": {
            "type": "number",
            "description": "Observed APR from live dashboards."
        },
        "volatility_score": {
            "type": "number",
            "description": "0-1 measure of pool volatility."
        },
        "lockup_days": {
            "type": "number",
            "description": "Expected lockup horizon in days."
        }
    },
    "required": [
        "principal_usd",
        "base_yield_apr",
        "volatility_score",
        "lockup_days"
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


def curve_liquidity_rebalance_playbook(metrics: Mapping[str, float | int]) -> dict[str, Any]:
    """Simulate Curve yield scenarios."""

    try:
        for field in ("principal_usd", "base_yield_apr", "volatility_score", "lockup_days"):
            if field not in metrics:
                raise ValueError(f"{field} is required")

        principal = float(metrics["principal_usd"])
        apr = float(metrics["base_yield_apr"])
        volatility = float(metrics["volatility_score"])
        lockup = float(metrics["lockup_days"])

        apr_adjusted = apr * (1 - volatility * 0.380)
        projected_yield = principal * (apr_adjusted / 100) * (lockup / 365)
        hedge_requirement = principal * volatility * 0.420
        il_floor = max(0.0, volatility - 0.220) * 100

        if il_floor > 3:
            recommendation = "Pair with delta hedge."
        elif hedge_requirement / principal > 0.3:
            recommendation = "Reduce leverage to keep health factor > 1.5."
        else:
            recommendation = "Deploy full stack."

        data = {
            "protocol": "Curve",
            "durational_yield_usd": round(projected_yield, 2),
            "apr_after_risk": round(apr_adjusted, 2),
            "hedge_buffer_usd": round(hedge_requirement, 2),
            "impermanent_loss_risk_pct": round(il_floor, 2),
            "recommendation": recommendation,
        }
        return {"status": "ok", "data": data, "timestamp": get_iso_timestamp()}
    except Exception as exc:
        _log_lesson("curve_liquidity_rebalance_playbook", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": get_iso_timestamp(),
        }
