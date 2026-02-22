"""Solve for implied volatility using Black-Scholes and bisection."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "implied_volatility_solver",
    "description": "Computes implied volatility from option price using bisection search.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "option_price": {"type": "number"},
            "spot": {"type": "number"},
            "strike": {"type": "number"},
            "time_to_expiry": {"type": "number"},
            "risk_free_rate": {"type": "number"},
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
            "status": {"type": "string"},
            "data": {"type": "object"},
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
    """Return implied volatility and pricing error."""
    try:
        low, high = 0.001, 5.0
        price = option_price
        iterations = 0
        while high - low > 1e-4 and iterations < 100:
            mid = (low + high) / 2
            model_price = _black_scholes(spot, strike, time_to_expiry, risk_free_rate, mid, option_type)
            if model_price > price:
                high = mid
            else:
                low = mid
            iterations += 1
        implied_vol = (low + high) / 2
        pricing_error = _black_scholes(spot, strike, time_to_expiry, risk_free_rate, implied_vol, option_type) - price
        data = {
            "implied_vol": round(implied_vol, 4),
            "iterations": iterations,
            "pricing_error": round(pricing_error, 4),
            "vol_smile_note": "High vol" if implied_vol > 1 else "Normal",
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("implied_volatility_solver", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _black_scholes(spot: float, strike: float, t: float, r: float, sigma: float, option_type: str) -> float:
    if sigma == 0 or t == 0:
        intrinsic = max(0.0, spot - strike) if option_type == "call" else max(0.0, strike - spot)
        return intrinsic
    d1 = (math.log(spot / strike) + (r + 0.5 * sigma**2) * t) / (sigma * math.sqrt(t))
    d2 = d1 - sigma * math.sqrt(t)
    call = spot * _norm_cdf(d1) - strike * math.exp(-r * t) * _norm_cdf(d2)
    if option_type == "call":
        return call
    return call - spot + strike * math.exp(-r * t)


def _norm_cdf(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
