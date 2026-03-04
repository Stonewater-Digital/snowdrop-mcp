"""Scores live sandwich attack risk across Arbitrum dex orderflow."""
from __future__ import annotations

from typing import Any, Mapping

from skills.utils import _log_lesson, get_iso_timestamp


TOOL_META: dict[str, Any] = {
    "name": "arbitrum_sandwich_risk_radar",
    "description": "Scores live sandwich attack risk across Arbitrum dex orderflow.",
    "tier": "free",
    "inputSchema": {
    "type": "object",
    "properties": {
        "mempool_pressure_index": {
            "type": "number",
            "description": "0-2 proxy for mempool load."
        },
        "sandwich_alerts_last_hour": {
            "type": "number",
            "description": "Count of sandwich alerts triggered in the last hour."
        },
        "dex_slippage_bps": {
            "type": "number",
            "description": "Observed slippage (bps) from tracked DEX pools."
        }
    },
    "required": [
        "mempool_pressure_index",
        "sandwich_alerts_last_hour",
        "dex_slippage_bps"
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


def arbitrum_sandwich_risk_radar(metrics: Mapping[str, float | int]) -> dict[str, Any]:
    """Estimate MEV pressure for Arbitrum."""

    try:
        for field in ("mempool_pressure_index", "sandwich_alerts_last_hour", "dex_slippage_bps"):
            if field not in metrics:
                raise ValueError(f"{field} is required")

        pressure = float(metrics["mempool_pressure_index"])
        alerts = float(metrics["sandwich_alerts_last_hour"])
        slippage = float(metrics["dex_slippage_bps"])

        risk_score = (pressure * 0.5 + slippage / 50 + alerts / 20) * 1.100
        risk_score = min(3.0, risk_score)

        if risk_score >= 2.4:
            action = "Pause public mempool submissions and reroute through private relays."
        elif risk_score >= 1.6:
            action = "Enable sandwich protection and raise priority fees."
        else:
            action = "Conditions acceptable; continue normal flow."

        data = {
            "network": "Arbitrum",
            "risk_score": round(risk_score, 2),
            "alerts_per_min": round(alerts / 60, 3),
            "recommended_action": action,
        }
        return {"status": "ok", "data": data, "timestamp": get_iso_timestamp()}
    except Exception as exc:
        _log_lesson("arbitrum_sandwich_risk_radar", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": get_iso_timestamp(),
        }
