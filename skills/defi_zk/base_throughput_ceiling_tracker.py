"""Estimates Base throughput headroom vs current usage to plan order flow bursts."""
from __future__ import annotations

from typing import Any, Mapping

from skills.utils import _log_lesson, get_iso_timestamp


TOOL_META: dict[str, Any] = {
    "name": "base_throughput_ceiling_tracker",
    "description": "Estimates Base throughput headroom vs current usage to plan order flow bursts.",
    "tier": "free",
    "inputSchema": {
    "type": "object",
    "properties": {
        "sequencer_backlog": {
            "type": "number",
            "description": "Current number of pending transactions waiting on the sequencer."
        },
        "avg_gas_price_gwei": {
            "type": "number",
            "description": "Average L2 gas price in gwei over the last minute."
        },
        "l1_data_gas_price_gwei": {
            "type": "number",
            "description": "Current L1 calldata gas price in gwei for the submission chain."
        }
    },
    "required": [
        "sequencer_backlog",
        "avg_gas_price_gwei",
        "l1_data_gas_price_gwei"
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


def base_throughput_ceiling_tracker(metrics: Mapping[str, float | int]) -> dict[str, Any]:
    """Evaluate sequencer conditions for Base."""

    try:
        for field in ("sequencer_backlog", "avg_gas_price_gwei", "l1_data_gas_price_gwei"):
            if field not in metrics:
                raise ValueError(f"{field} is required")

        backlog = float(metrics["sequencer_backlog"])
        avg_gas = float(metrics["avg_gas_price_gwei"])
        data_gas = float(metrics["l1_data_gas_price_gwei"])

        backlog_ratio = backlog / max(600.000, 1)
        gas_ratio = avg_gas / max(0.050 * 10, 0.001)
        data_ratio = data_gas / max(7.000, 0.001)

        pressure_index = (
            backlog_ratio * 0.580
            + gas_ratio * 0.240
            + data_ratio * 0.2
        )
        predicted_fee = 0.050000 * (1 + pressure_index * 0.360)
        band = [max(predicted_fee * 0.85, 0.0001), predicted_fee * 1.15]

        if pressure_index >= 1.5:
            guidance = "Throttle order flow or subsidize priority fees."
        elif pressure_index >= 1.0:
            guidance = "Expect elevated fees; alert power users."
        else:
            guidance = "Fees normal; OK to batch routine jobs."

        data = {
            "network": "Base",
            "pressure_index": round(pressure_index, 3),
            "predicted_fee_gwei": round(predicted_fee, 5),
            "fee_band_gwei": [round(band[0], 5), round(band[1], 5)],
            "guidance": guidance,
        }
        return {"status": "ok", "data": data, "timestamp": get_iso_timestamp()}
    except Exception as exc:
        _log_lesson("base_throughput_ceiling_tracker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": get_iso_timestamp(),
        }
