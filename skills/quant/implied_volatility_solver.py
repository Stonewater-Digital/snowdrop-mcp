"""Solve for implied volatility using Black-Scholes and bisection."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "implied_volatility_solver",
    "description": "Computes implied volatility from an observed option price using bisection on the Black-Scholes model.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "option_price": {"type": "number", "description": "Observed market option price. Must be > 0."},
            "spot": {"type": "number", "description": "Underlying spot price. Must be > 0."},
            "strike": {"type": "number", "description": "Option strike price. Must be > 0."},
            "time_to_expiry": {"type": "number", "description": "Time to expiry in years. Must be > 0."},
            "risk_free_rate": {"type": "number", "description": "Risk-free rate as a decimal (e.g. 0.05 for 5%)."},
            "option_type": {"type": "string", "enum": ["call", "put"]},
        },
        "required": [
            "option_price",
            "spot",
            "strike",
            "time_to_expiry",
            "risk_free_rate",
            "option_type",
        ],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "data": {
                "type": "object",
                "properties": {
                    "implied_vol_pct": {"type": "number"},
                    "implied_vol_decimal": {"type": "number"},
                    "iterations": {"type": "integer"},
                    "pricing_error": {"type": "number"},
                    "vol_regime": {"type": "string"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def implied_volatility_solver(
    option_price: float,
    spot: float,
    strike: float,
    time_to_expiry: float,
    risk_free_rate: float,
    option_type: str,
    **_: Any,
) -> dict[str, Any]:
    """Return implied volatility from an observed option price via bisection.

    Bisects the Black-Scholes vol space [0.001, 5.0] (0.1% to 500%).
    Convergence tolerance: 1e-5 on vol, max 200 iterations.

    Args:
        option_price: Observed option price (must be > 0).
        spot: Underlying spot price (must be > 0).
        strike: Strike price (must be > 0).
        time_to_expiry: Time to expiry in years (must be > 0).
        risk_free_rate: Risk-free rate as a decimal (not percentage).
        option_type: 'call' or 'put'.

    Returns:
        dict with implied_vol_pct, implied_vol_decimal, iterations,
        pricing_error, vol_regime.
    """
    try:
        if option_price <= 0:
            raise ValueError("option_price must be positive")
        if spot <= 0 or strike <= 0:
            raise ValueError("spot and strike must be positive")
        if time_to_expiry <= 0:
            raise ValueError("time_to_expiry must be positive")

        option_type = option_type.lower()
        if option_type not in {"call", "put"}:
            raise ValueError("option_type must be 'call' or 'put'")

        # Check that option_price is above intrinsic to avoid no-solution case
        disc = math.exp(-risk_free_rate * time_to_expiry)
        if option_type == "call":
            intrinsic = max(0.0, spot - strike * disc)
        else:
            intrinsic = max(0.0, strike * disc - spot)
        if option_price < intrinsic - 1e-6:
            raise ValueError(
                f"option_price ({option_price:.4f}) is below intrinsic ({intrinsic:.4f}); "
                "implied vol has no solution"
            )

        low, high = 1e-4, 5.0
        iterations = 0
        tol = 1e-5

        while high - low > tol and iterations < 200:
            mid = (low + high) / 2.0
            model_price = _black_scholes(spot, strike, time_to_expiry, risk_free_rate, mid, option_type)
            if model_price > option_price:
                high = mid
            else:
                low = mid
            iterations += 1

        implied_vol = (low + high) / 2.0
        pricing_error = _black_scholes(spot, strike, time_to_expiry, risk_free_rate, implied_vol, option_type) - option_price

        if implied_vol > 1.0:
            vol_regime = "very_high"
        elif implied_vol > 0.5:
            vol_regime = "high"
        elif implied_vol > 0.2:
            vol_regime = "normal"
        else:
            vol_regime = "low"

        data = {
            "implied_vol_pct": round(implied_vol * 100, 4),
            "implied_vol_decimal": round(implied_vol, 6),
            "iterations": iterations,
            "pricing_error": round(pricing_error, 6),
            "vol_regime": vol_regime,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson(f"implied_volatility_solver: {exc}")
        return {
            "status": "error",
            "error": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _black_scholes(spot: float, strike: float, t: float, r: float, sigma: float, option_type: str) -> float:
    """Compute Black-Scholes price; returns intrinsic if sigma/t is near zero."""
    if sigma < 1e-10 or t < 1e-10:
        return max(0.0, spot - strike) if option_type == "call" else max(0.0, strike - spot)
    d1 = (math.log(spot / strike) + (r + 0.5 * sigma ** 2) * t) / (sigma * math.sqrt(t))
    d2 = d1 - sigma * math.sqrt(t)
    disc = math.exp(-r * t)
    if option_type == "call":
        return spot * _norm_cdf(d1) - strike * disc * _norm_cdf(d2)
    # Put via put-call parity
    call = spot * _norm_cdf(d1) - strike * disc * _norm_cdf(d2)
    return call - spot + strike * disc


def _norm_cdf(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def _log_lesson(message: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
