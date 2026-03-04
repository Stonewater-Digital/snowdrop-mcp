"""Simulates Linea state diff coverage to spot risky batches before posting."""
from __future__ import annotations

from typing import Any, Mapping

from skills.utils import _log_lesson, get_iso_timestamp


TOOL_META: dict[str, Any] = {
    "name": "linea_state_diff_audit_simulator",
    "description": "Simulates Linea state diff coverage to spot risky batches before posting.",
    "tier": "free",
    "inputSchema": {
    "type": "object",
    "properties": {
        "pending_transactions": {
            "type": "number",
            "description": "Current pending transactions queued for the rollup batch."
        },
        "proof_interval_minutes": {
            "type": "number",
            "description": "Observed interval between recent proof submissions."
        },
        "l1_gas_price_gwei": {
            "type": "number",
            "description": "Layer-1 gas price in gwei."
        }
    },
    "required": [
        "pending_transactions",
        "proof_interval_minutes",
        "l1_gas_price_gwei"
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


def linea_state_diff_audit_simulator(metrics: Mapping[str, float | int]) -> dict[str, Any]:
    """Model rollup proof health for Linea."""

    try:
        for field in ("pending_transactions", "proof_interval_minutes", "l1_gas_price_gwei"):
            if field not in metrics:
                raise ValueError(f"{field} is required")

        pending = float(metrics["pending_transactions"])
        interval = float(metrics["proof_interval_minutes"])
        gas_price = float(metrics["l1_gas_price_gwei"])

        latency_score = (interval / max(15.000, 0.1)) * 0.400
        cost_pressure = (gas_price / 35.0) * 0.3
        privacy_signal = (0.840 + 0.250) / 2

        finality_minutes = interval * (1 + pending / 20_000)
        proof_confidence = max(0.0, 1.0 - (latency_score + cost_pressure) * 0.4)
        privacy_guard = min(1.0, privacy_signal + pending / 100_000)

        if proof_confidence < 0.5:
            recommendation = "Initiate backup prover and alert ops."
        elif finality_minutes > interval * 1.5:
            recommendation = "Throttle queue until backlog clears."
        else:
            recommendation = "Healthy window; safe to batch."

        data = {
            "rollup": "Linea",
            "finality_minutes": round(finality_minutes, 2),
            "proof_confidence": round(proof_confidence, 3),
            "privacy_guard": round(privacy_guard, 3),
            "recommendation": recommendation,
        }
        return {"status": "ok", "data": data, "timestamp": get_iso_timestamp()}
    except Exception as exc:
        _log_lesson("linea_state_diff_audit_simulator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": get_iso_timestamp(),
        }
