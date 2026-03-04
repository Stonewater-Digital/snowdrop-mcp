"""
Executive Summary: Prices contingent CDS that triggers only after an equity barrier knock-in event.
Inputs: equity_spot (float), barrier_level (float), equity_volatility (float), drift (float), horizon_years (float), default_probability (float), recovery_rate (float), notional (float), discount_rate (float)
Outputs: status (str), timestamp (str), data (dict)
MCP Tool Name: contingent_cds_pricer
"""
import logging
import math
import random
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "contingent_cds_pricer",
    "description": (
        "Values contingent CDS via barrier-adjusted probabilities: barrier probability via down-and-in hitting "
        "formula (Broadie-Glasserman) multiplied by conditional default PV."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "equity_spot": {"type": "number", "description": "Current equity price serving as trigger reference."},
            "barrier_level": {"type": "number", "description": "Equity barrier level for knock-in (spot must breach)."},
            "equity_volatility": {"type": "number", "description": "Equity volatility (decimal)."},
            "drift": {"type": "number", "description": "Equity risk-neutral drift (r-q)."},
            "horizon_years": {"type": "number", "description": "Contract tenor in years."},
            "default_probability": {"type": "number", "description": "Unconditional default probability over the horizon."},
            "recovery_rate": {"type": "number", "description": "Recovery assumption on the CDS leg."},
            "notional": {"type": "number", "description": "Contract notional."},
            "discount_rate": {"type": "number", "description": "Continuous risk-free rate for PV."}
        },
        "required": [
            "equity_spot",
            "barrier_level",
            "equity_volatility",
            "drift",
            "horizon_years",
            "default_probability",
            "recovery_rate",
            "notional",
            "discount_rate"
        ]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"}
        },
        "required": ["status", "timestamp"]
    }
}


def contingent_cds_pricer(**kwargs: Any) -> dict[str, Any]:
    try:
        spot = float(kwargs["equity_spot"])
        barrier = float(kwargs["barrier_level"])
        sigma = float(kwargs["equity_volatility"])
        drift = float(kwargs["drift"])
        tenor = float(kwargs["horizon_years"])
        default_probability = float(kwargs["default_probability"])
        recovery = float(kwargs["recovery_rate"])
        notional = float(kwargs["notional"])
        discount_rate = float(kwargs["discount_rate"])
        if spot <= 0 or barrier <= 0 or sigma <= 0:
            raise ValueError("spot, barrier, and volatility must be positive")
        barrier_prob = _estimate_barrier_hit_probability(spot, barrier, drift, sigma, tenor)
        default_probability = min(max(default_probability, 0.0), 1.0)
        if not 0.0 <= recovery < 1.0:
            raise ValueError("recovery_rate must lie in [0,1)")

        joint_probability = barrier_prob * default_probability
        discount_factor = math.exp(-discount_rate * tenor)
        expected_payout = joint_probability * (1 - recovery) * notional
        present_value = expected_payout * discount_factor

        data = {
            "barrier_hit_probability": barrier_prob,
            "default_probability": default_probability,
            "joint_probability": joint_probability,
            "expected_payout": expected_payout,
            "present_value": present_value,
            "discount_factor": discount_factor
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError, KeyError) as e:
        logger.error("contingent_cds_pricer failed: %s", e)
        _log_lesson(f"contingent_cds_pricer: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _estimate_barrier_hit_probability(
    spot: float, barrier: float, drift: float, sigma: float, tenor: float, num_paths: int = 8000
) -> float:
    steps = max(50, int(252 * tenor))
    dt = tenor / steps
    rand = random.Random(123)
    hits = 0
    for _ in range(num_paths):
        s_prev = spot
        hit = False
        for _ in range(steps):
            z = rand.gauss(0.0, 1.0)
            s_new = s_prev * math.exp((drift - 0.5 * sigma * sigma) * dt + sigma * math.sqrt(dt) * z)
            if (s_prev > barrier and s_new <= barrier) or (s_prev < barrier and s_new >= barrier):
                hit = True
                break
            # Brownian-bridge adjustment for continuous monitoring (Andersen-Brotherton-Ratcliffe)
            if (s_prev > barrier and s_new > barrier and barrier < s_prev):
                log_prev = math.log(s_prev / barrier)
                log_new = math.log(s_new / barrier)
                bridge_prob = math.exp(-2 * log_prev * log_new / (sigma * sigma * dt))
                if rand.random() < min(max(bridge_prob, 0.0), 1.0):
                    hit = True
                    break
            s_prev = s_new
        if hit:
            hits += 1
    return hits / num_paths


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as file:
            file.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
