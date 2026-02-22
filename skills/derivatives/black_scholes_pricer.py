"""Price options and Greeks via the Black-Scholes model."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "black_scholes_pricer",
    "description": "Calculates Black-Scholes option prices with full Greek outputs.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "spot_price": {"type": "number"},
            "strike_price": {"type": "number"},
            "time_to_expiry_years": {"type": "number"},
            "risk_free_rate": {"type": "number"},
            "volatility": {"type": "number"},
            "option_type": {
                "type": "string",
                "enum": ["call", "put"],
                "description": "Option flavor for payoff selection.",
            },
        },
        "required": [
            "spot_price",
            "strike_price",
            "time_to_expiry_years",
            "risk_free_rate",
            "volatility",
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


def _norm_cdf(value: float) -> float:
    """Cumulative normal distribution via Abramowitz-Stegun approximation."""
    k = 1.0 / (1.0 + 0.2316419 * abs(value))
    coeffs = [0.319381530, -0.356563782, 1.781477937, -1.821255978, 1.330274429]
    poly = sum(c * k ** (idx + 1) for idx, c in enumerate(coeffs))
    approx = 1.0 - (1.0 / math.sqrt(2 * math.pi)) * math.exp(-0.5 * value * value) * poly
    return approx if value >= 0 else 1.0 - approx


def _norm_pdf(value: float) -> float:
    """Probability density for a standard normal variable."""
    return (1.0 / math.sqrt(2 * math.pi)) * math.exp(-0.5 * value * value)


def black_scholes_pricer(
    spot_price: float,
    strike_price: float,
    time_to_expiry_years: float,
    risk_free_rate: float,
    volatility: float,
    option_type: str,
    **_: Any,
) -> dict[str, Any]:
    """Compute Black-Scholes theoretical price and Greeks."""
    try:
        if spot_price <= 0 or strike_price <= 0:
            raise ValueError("spot_price and strike_price must be positive")
        if time_to_expiry_years <= 0:
            raise ValueError("time_to_expiry_years must be positive")
        if volatility <= 0:
            raise ValueError("volatility must be positive")
        option_type = option_type.lower()
        if option_type not in {"call", "put"}:
            raise ValueError("option_type must be 'call' or 'put'")

        sqrt_t = math.sqrt(time_to_expiry_years)
        d1 = (
            math.log(spot_price / strike_price)
            + (risk_free_rate + 0.5 * volatility * volatility) * time_to_expiry_years
        ) / (volatility * sqrt_t)
        d2 = d1 - volatility * sqrt_t

        nd1 = _norm_cdf(d1)
        nd2 = _norm_cdf(d2)
        pdf_d1 = _norm_pdf(d1)
        discount = math.exp(-risk_free_rate * time_to_expiry_years)

        if option_type == "call":
            price = spot_price * nd1 - strike_price * discount * nd2
            delta = nd1
            rho = strike_price * time_to_expiry_years * discount * nd2
            theta = (
                -spot_price * pdf_d1 * volatility / (2 * sqrt_t)
                - risk_free_rate * strike_price * discount * nd2
            )
        else:
            price = strike_price * discount * _norm_cdf(-d2) - spot_price * _norm_cdf(-d1)
            delta = nd1 - 1
            rho = -strike_price * time_to_expiry_years * discount * _norm_cdf(-d2)
            theta = (
                -spot_price * pdf_d1 * volatility / (2 * sqrt_t)
                + risk_free_rate * strike_price * discount * _norm_cdf(-d2)
            )

        gamma = pdf_d1 / (spot_price * volatility * sqrt_t)
        vega = spot_price * pdf_d1 * sqrt_t

        result = {
            "price": round(price, 6),
            "delta": round(delta, 6),
            "gamma": round(gamma, 6),
            "theta": round(theta, 6),
            "vega": round(vega, 6),
            "rho": round(rho, 6),
            "d1": round(d1, 6),
            "d2": round(d2, 6),
        }
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("black_scholes_pricer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    """Record anomaly entries for follow-up."""
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
