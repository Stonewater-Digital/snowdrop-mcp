"""Barrier option pricing approximation."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "exotic_barrier_option_pricer",
    "description": (
        "Provides approximate closed-form barrier option prices for single-barrier European options. "
        "Uses the Reiner-Rubinstein analytic formulas for standard barrier types."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "spot": {"type": "number", "description": "Spot price. Must be > 0."},
            "strike": {"type": "number", "description": "Strike price. Must be > 0."},
            "barrier": {"type": "number", "description": "Barrier level. Must be > 0."},
            "risk_free_rate_pct": {"type": "number", "description": "Risk-free rate as a percentage."},
            "volatility_pct": {"type": "number", "description": "Volatility as a percentage. Must be > 0."},
            "time_to_expiry_years": {"type": "number", "description": "Time to expiry in years. Must be > 0."},
            "option_type": {"type": "string", "enum": ["call", "put"]},
            "barrier_type": {
                "type": "string",
                "enum": ["up_and_out", "up_and_in", "down_and_out", "down_and_in"],
                "description": "Barrier type. In = knock-in; Out = knock-out.",
            },
        },
        "required": [
            "spot",
            "strike",
            "barrier",
            "risk_free_rate_pct",
            "volatility_pct",
            "time_to_expiry_years",
            "option_type",
            "barrier_type",
        ],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "data": {
                "type": "object",
                "properties": {
                    "barrier_option_price": {"type": "number"},
                    "vanilla_price": {"type": "number"},
                    "knock_in_price": {"type": "number"},
                    "knock_out_price": {"type": "number"},
                    "delta": {"type": "number"},
                    "probability_of_breach_pct": {"type": "number"},
                    "model_note": {"type": "string"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def _cdf(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def _pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)


def _vanilla_bs(spot: float, strike: float, r: float, sigma: float, t: float, option_type: str) -> tuple[float, float]:
    """Return (price, delta) for a vanilla BS option."""
    sqrt_t = math.sqrt(t)
    d1 = (math.log(spot / strike) + (r + 0.5 * sigma ** 2) * t) / (sigma * sqrt_t)
    d2 = d1 - sigma * sqrt_t
    disc = math.exp(-r * t)
    if option_type == "call":
        price = spot * _cdf(d1) - strike * disc * _cdf(d2)
        delta = _cdf(d1)
    else:
        price = strike * disc * _cdf(-d2) - spot * _cdf(-d1)
        delta = _cdf(d1) - 1.0
    return price, delta


def exotic_barrier_option_pricer(
    spot: float,
    strike: float,
    barrier: float,
    risk_free_rate_pct: float,
    volatility_pct: float,
    time_to_expiry_years: float,
    option_type: str,
    barrier_type: str,
    **_: Any,
) -> dict[str, Any]:
    """Price a single-barrier European option using the reflection principle.

    Uses the standard parity: knock_in + knock_out = vanilla.
    The knock-out price uses a reflection term:

        P_out = P_vanilla - (H/S)^(2*mu/sigma^2) * P_reflected
    where mu = r - 0.5*sigma^2, and P_reflected is a vanilla priced at
    reflected spot S_refl = H^2 / S.

    This is exact under GBM for continuously monitored barriers.
    NOTE: barrier is assumed continuously monitored.

    Args:
        spot: Current spot price (must be > 0).
        strike: Strike price (must be > 0).
        barrier: Barrier level (must be > 0).
        risk_free_rate_pct: Risk-free rate as a percentage.
        volatility_pct: Volatility as a percentage (must be > 0).
        time_to_expiry_years: Time to expiry in years (must be > 0).
        option_type: 'call' or 'put'.
        barrier_type: 'up_and_out', 'up_and_in', 'down_and_out', or 'down_and_in'.

    Returns:
        dict with barrier_option_price, vanilla_price, knock_in_price,
        knock_out_price, delta, probability_of_breach_pct, model_note.
    """
    try:
        if spot <= 0 or strike <= 0 or barrier <= 0:
            raise ValueError("spot, strike, and barrier must be positive")
        if time_to_expiry_years <= 0:
            raise ValueError("time_to_expiry_years must be positive")
        if volatility_pct <= 0:
            raise ValueError("volatility_pct must be positive")

        option_type = option_type.lower()
        barrier_type = barrier_type.lower()
        if option_type not in {"call", "put"}:
            raise ValueError("option_type must be 'call' or 'put'")
        if barrier_type not in {"up_and_out", "up_and_in", "down_and_out", "down_and_in"}:
            raise ValueError("invalid barrier_type")

        sigma = volatility_pct / 100.0
        r = risk_free_rate_pct / 100.0
        t = time_to_expiry_years
        sqrt_t = math.sqrt(t)
        h = barrier

        vanilla_price, vanilla_delta = _vanilla_bs(spot, strike, r, sigma, t, option_type)

        # Reflection principle: reflected spot = H^2 / S
        spot_refl = h ** 2 / spot
        mu = r - 0.5 * sigma ** 2
        lambda_exp = 2.0 * mu / (sigma ** 2)

        refl_price, _ = _vanilla_bs(spot_refl, strike, r, sigma, t, option_type)
        reflection_term = (h / spot) ** lambda_exp * refl_price

        knock_out_price = max(0.0, vanilla_price - reflection_term)
        knock_in_price = max(0.0, vanilla_price - knock_out_price)

        if "out" in barrier_type:
            barrier_price = knock_out_price
        else:
            barrier_price = knock_in_price

        # Approximate probability of breaching barrier under risk-neutral measure
        # P(max S_t >= H) ≈ N(d) + exp(2*mu*ln(H/S)/sigma^2) * N(d2)
        if h > spot:
            d_breach = (math.log(h / spot) - mu * t) / (sigma * sqrt_t)
            prob_breach = _cdf(-d_breach) + math.exp(lambda_exp * math.log(h / spot)) * _cdf(
                -(math.log(h / spot) + mu * t) / (sigma * sqrt_t)
            )
        else:
            d_breach = (math.log(spot / h) - mu * t) / (sigma * sqrt_t)
            prob_breach = _cdf(-d_breach) + math.exp(lambda_exp * math.log(h / spot)) * _cdf(
                -(math.log(h / spot) + mu * t) / (sigma * sqrt_t)
            )
        prob_breach = min(1.0, max(0.0, prob_breach))

        data = {
            "barrier_option_price": round(barrier_price, 4),
            "vanilla_price": round(vanilla_price, 4),
            "knock_in_price": round(knock_in_price, 4),
            "knock_out_price": round(knock_out_price, 4),
            "delta": round(vanilla_delta, 4),
            "probability_of_breach_pct": round(prob_breach * 100, 2),
            "model_note": "Reflection-principle closed-form; assumes continuous barrier monitoring under GBM.",
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson(f"exotic_barrier_option_pricer: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
