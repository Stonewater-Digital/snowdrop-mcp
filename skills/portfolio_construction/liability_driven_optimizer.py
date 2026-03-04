"""
Executive Summary: Liability-driven investment optimizer aligning asset surplus, duration, and convexity with liability targets.
Inputs: asset_cashflows (list[dict]), liability_schedule (list[dict]), discount_rate (float)
Outputs: asset_weights (list[dict]), liability_duration (float), surplus (float), hedge_effectiveness (float)
MCP Tool Name: liability_driven_optimizer
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

import numpy as np

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "liability_driven_optimizer",
    "description": (
        "Matches liability duration/convexity and surplus targets by allocating across asset cash-flow profiles "
        "consistent with ERISA and Solvency II liability-driven investing practices."),
    "inputSchema": {
        "type": "object",
        "properties": {
            "asset_cashflows": {
                "type": "array",
                "description": "List of asset dictionaries each containing name and future cash flows.",
                "items": {
                    "type": "object",
                    "properties": {
                        "asset": {"type": "string", "description": "Asset identifier"},
                        "cashflows": {
                            "type": "array",
                            "description": "Cash flow schedule (time in years, amount).",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "time": {"type": "number", "description": "Years"},
                                    "amount": {"type": "number", "description": "Cash amount"},
                                },
                                "required": ["time", "amount"],
                            },
                        },
                    },
                    "required": ["asset", "cashflows"],
                },
            },
            "liability_schedule": {
                "type": "array",
                "description": "Schedule of liability cash flows with time and amount.",
                "items": {
                    "type": "object",
                    "properties": {
                        "time": {"type": "number", "description": "Years"},
                        "amount": {"type": "number", "description": "Cash amount"},
                    },
                    "required": ["time", "amount"],
                },
            },
            "discount_rate": {
                "type": "number",
                "description": "Flat discount rate used for PV calculations (decimal).",
            },
        },
        "required": ["asset_cashflows", "liability_schedule", "discount_rate"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "Execution status"},
            "data": {"type": "object", "description": "LDI solution"},
            "timestamp": {"type": "string", "description": "UTC timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def _pv_duration_convexity(schedule: List[Dict[str, float]], rate: float) -> tuple[float, float, float]:
    pv = 0.0
    duration_numer = 0.0
    convexity_numer = 0.0
    for item in schedule:
        t = float(item["time"])
        amt = float(item["amount"])
        discount = (1 + rate) ** t
        pv_contrib = amt / discount
        pv += pv_contrib
        duration_numer += t * pv_contrib
        convexity_numer += t * (t + 1) * pv_contrib / ((1 + rate) ** 2)
    duration = duration_numer / pv if pv else 0.0
    convexity = convexity_numer / pv if pv else 0.0
    return pv, duration, convexity


def liability_driven_optimizer(
    asset_cashflows: List[Dict[str, Any]],
    liability_schedule: List[Dict[str, float]],
    discount_rate: float,
    **_: Any,
) -> dict[str, Any]:
    try:
        if discount_rate < -0.01:
            raise ValueError("discount_rate cannot be strongly negative")
        liab_pv, liab_duration, liab_convexity = _pv_duration_convexity(liability_schedule, discount_rate)
        assets = []
        metrics = []
        for record in asset_cashflows:
            asset = record["asset"]
            pv, dur, conv = _pv_duration_convexity(record["cashflows"], discount_rate)
            if pv <= 0:
                raise ValueError(f"Asset {asset} has non-positive PV")
            assets.append(asset)
            metrics.append((pv, dur, conv))
        n = len(assets)
        pv_vec = np.array([m[0] for m in metrics])
        duration_vec = np.array([m[1] for m in metrics])
        convexity_vec = np.array([m[2] for m in metrics])
        target = np.array([liab_pv, liab_pv * liab_duration, liab_pv * liab_convexity])
        A = np.vstack([pv_vec, pv_vec * duration_vec, pv_vec * convexity_vec]).T
        weights, *_ = np.linalg.lstsq(A, target, rcond=None)
        weights = np.maximum(weights, 0.0)
        weights /= weights.sum()
        hedged_pv = float(pv_vec @ weights)
        hedged_duration = float((pv_vec * duration_vec) @ weights / hedged_pv)
        hedged_convexity = float((pv_vec * convexity_vec) @ weights / hedged_pv)
        surplus = hedged_pv - liab_pv
        hedge_effectiveness = 1 - abs(hedged_duration - liab_duration) / max(liab_duration, 1e-6)
        data = {
            "asset_weights": [
                {
                    "asset": asset,
                    "weight": round(float(weights[idx]), 6),
                    "duration": round(float(duration_vec[idx]), 4),
                    "convexity": round(float(convexity_vec[idx]), 4),
                }
                for idx, asset in enumerate(assets)
            ],
            "liability_duration": round(liab_duration, 4),
            "liability_convexity": round(liab_convexity, 4),
            "surplus": round(surplus, 4),
            "hedge_effectiveness": round(float(hedge_effectiveness), 4),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, np.linalg.LinAlgError) as e:
        logger.error(f"liability_driven_optimizer failed: {e}")
        _log_lesson(f"liability_driven_optimizer: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as sink:
            sink.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
