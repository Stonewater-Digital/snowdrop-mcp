"""Garman-Kohlhagen FX option pricer."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "fx_option_pricer",
    "description": "Prices European FX options under Garman-Kohlhagen and returns Greeks.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "spot": {"type": "number", "description": "Spot FX rate (domestic per foreign). Must be > 0."},
            "strike": {"type": "number", "description": "Option strike rate. Must be > 0."},
            "domestic_rate_pct": {"type": "number", "description": "Domestic risk-free rate as a percentage."},
            "foreign_rate_pct": {"type": "number", "description": "Foreign risk-free (dividend) rate as a percentage."},
            "volatility_pct": {"type": "number", "description": "Annualised implied vol as a percentage. Must be > 0."},
            "time_to_expiry_years": {"type": "number", "description": "Time to expiry in years. Must be > 0."},
            "option_type": {"type": "string", "enum": ["call", "put"]},
            "notional": {"type": "number", "default": 1.0, "description": "Notional (default 1.0)."},
        },
        "required": [
            "spot",
            "strike",
            "domestic_rate_pct",
            "foreign_rate_pct",
            "volatility_pct",
            "time_to_expiry_years",
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
                    "option_price": {"type": "number"},
                    "delta": {"type": "number"},
                    "gamma": {"type": "number"},
                    "theta": {"type": "number"},
                    "vega": {"type": "number"},
                    "rho_domestic": {"type": "number"},
                    "rho_foreign": {"type": "number"},
                    "breakeven_spot": {"type": "number"},
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


def fx_option_pricer(
    spot: float,
    strike: float,
    domestic_rate_pct: float,
    foreign_rate_pct: float,
    volatility_pct: float,
    time_to_expiry_years: float,
    option_type: str,
    notional: float = 1.0,
    **_: Any,
) -> dict[str, Any]:
    """Return FX option price and Greeks via Garman-Kohlhagen.

    G-K model: treat foreign rate as a continuous dividend yield.
        d1 = [ln(S/K) + (r_d - r_f + 0.5*sigma^2)*T] / (sigma*sqrt(T))
        d2 = d1 - sigma*sqrt(T)
        Call = S*exp(-r_f*T)*N(d1) - K*exp(-r_d*T)*N(d2)
        Put  = K*exp(-r_d*T)*N(-d2) - S*exp(-r_f*T)*N(-d1)

    Args:
        spot: Spot FX rate (must be > 0).
        strike: Option strike (must be > 0).
        domestic_rate_pct: Domestic risk-free rate as a percentage.
        foreign_rate_pct: Foreign risk-free rate as a percentage.
        volatility_pct: Annualised vol as a percentage (must be > 0).
        time_to_expiry_years: Time to expiry in years (must be > 0).
        option_type: 'call' or 'put'.
        notional: Notional multiplier (default 1.0).

    Returns:
        dict with option_price, delta, gamma, theta, vega,
        rho_domestic, rho_foreign, breakeven_spot.
    """
    try:
        if spot <= 0 or strike <= 0:
            raise ValueError("spot and strike must be positive")
        if time_to_expiry_years <= 0:
            raise ValueError("time_to_expiry_years must be positive")
        if volatility_pct <= 0:
            raise ValueError("volatility_pct must be positive")
        if notional <= 0:
            raise ValueError("notional must be positive")

        option_type = option_type.lower()
        if option_type not in {"call", "put"}:
            raise ValueError("option_type must be 'call' or 'put'")

        sigma = volatility_pct / 100.0
        rd = domestic_rate_pct / 100.0
        rf = foreign_rate_pct / 100.0
        t = time_to_expiry_years
        sqrt_t = math.sqrt(t)
        df_d = math.exp(-rd * t)
        df_f = math.exp(-rf * t)

        d1 = (math.log(spot / strike) + (rd - rf + 0.5 * sigma ** 2) * t) / (sigma * sqrt_t)
        d2 = d1 - sigma * sqrt_t

        if option_type == "call":
            price = notional * (spot * df_f * _cdf(d1) - strike * df_d * _cdf(d2))
            delta = df_f * _cdf(d1)
            # Theta: per calendar day
            theta = (
                -spot * df_f * _pdf(d1) * sigma / (2 * sqrt_t)
                + rf * spot * df_f * _cdf(d1)
                - rd * strike * df_d * _cdf(d2)
            ) / 365.0
            rho_dom = strike * t * df_d * _cdf(d2) / 100.0   # per 1% move
            rho_for = -spot * t * df_f * _cdf(d1) / 100.0
        else:
            price = notional * (strike * df_d * _cdf(-d2) - spot * df_f * _cdf(-d1))
            delta = -df_f * _cdf(-d1)
            theta = (
                -spot * df_f * _pdf(d1) * sigma / (2 * sqrt_t)
                - rf * spot * df_f * _cdf(-d1)
                + rd * strike * df_d * _cdf(-d2)
            ) / 365.0
            rho_dom = -strike * t * df_d * _cdf(-d2) / 100.0  # per 1% move
            rho_for = spot * t * df_f * _cdf(-d1) / 100.0

        gamma = df_f * _pdf(d1) / (spot * sigma * sqrt_t)
        vega = spot * df_f * _pdf(d1) * sqrt_t / 100.0   # per 1% move in vol

        # Breakeven: spot at expiry that recovers the premium (per unit notional)
        unit_price = price / notional
        if option_type == "call":
            breakeven_spot = strike + unit_price
        else:
            breakeven_spot = strike - unit_price

        data = {
            "option_price": round(price, 4),
            "delta": round(delta, 6),
            "gamma": round(gamma, 6),
            "theta": round(theta, 6),
            "vega": round(vega, 6),
            "rho_domestic": round(rho_dom, 6),
            "rho_foreign": round(rho_for, 6),
            "breakeven_spot": round(breakeven_spot, 6),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson(f"fx_option_pricer: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
