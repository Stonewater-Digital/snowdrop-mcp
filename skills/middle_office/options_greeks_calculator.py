"""Black-Scholes option Greek calculator."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "options_greeks_calculator",
    "description": "Returns price and Greeks for European options via Black-Scholes.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "spot": {"type": "number"},
            "strike": {"type": "number"},
            "rate": {"type": "number"},
            "volatility": {"type": "number"},
            "time_to_expiry": {"type": "number"},
            "option_type": {"type": "string", "enum": ["call", "put"]},
        },
        "required": ["spot", "strike", "rate", "volatility", "time_to_expiry", "option_type"],
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


def _norm_cdf(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def _norm_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)


def options_greeks_calculator(
    spot: float,
    strike: float,
    rate: float,
    volatility: float,
    time_to_expiry: float,
    option_type: str,
    **_: Any,
) -> dict[str, Any]:
    """Return option price and Greeks."""
    try:
        option_type = option_type.lower()
        if spot <= 0 or strike <= 0 or time_to_expiry <= 0:
            raise ValueError("spot, strike, and time_to_expiry must be positive")
        sigma = volatility / 100 if volatility > 1 else volatility
        r = rate / 100 if rate > 1 else rate
        sqrt_t = math.sqrt(time_to_expiry)
        d1 = (math.log(spot / strike) + (r + 0.5 * sigma**2) * time_to_expiry) / (sigma * sqrt_t)
        d2 = d1 - sigma * sqrt_t
        if option_type == "call":
            price = spot * _norm_cdf(d1) - strike * math.exp(-r * time_to_expiry) * _norm_cdf(d2)
            delta = _norm_cdf(d1)
        elif option_type == "put":
            price = strike * math.exp(-r * time_to_expiry) * _norm_cdf(-d2) - spot * _norm_cdf(-d1)
            delta = _norm_cdf(d1) - 1
        else:
            raise ValueError("option_type must be call or put")
        gamma = _norm_pdf(d1) / (spot * sigma * sqrt_t)
        theta = (
            -spot * _norm_pdf(d1) * sigma / (2 * sqrt_t)
            - r * strike * math.exp(-r * time_to_expiry) * (_norm_cdf(d2) if option_type == "call" else _norm_cdf(-d2))
        )
        vega = spot * _norm_pdf(d1) * sqrt_t / 100
        rho = (
            strike
            * time_to_expiry
            * math.exp(-r * time_to_expiry)
            * (_norm_cdf(d2) if option_type == "call" else -_norm_cdf(-d2))
            / 100
        )
        data = {
            "option_price": round(price, 6),
            "delta": round(delta, 6),
            "gamma": round(gamma, 6),
            "theta": round(theta, 6),
            "vega": round(vega, 6),
            "rho": round(rho, 6),
        }
        return {"status": "ok", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        try:
            with open("logs/lessons.md", "a") as _f:
                _f.write(f"- [{datetime.now(timezone.utc).isoformat()}] options_greeks_calculator: {exc}\n")
        except OSError:
            pass
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
