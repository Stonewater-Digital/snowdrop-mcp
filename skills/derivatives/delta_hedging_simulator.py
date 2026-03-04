"""Delta hedging simulator."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "delta_hedging_simulator",
    "description": "Simulates discrete delta hedging P&L decomposition over a price path.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "spot_prices": {
                "type": "array",
                "items": {"type": "number"},
                "description": "Time-ordered underlying price path (at least 2 values).",
            },
            "strike": {"type": "number", "description": "Option strike price. Must be > 0."},
            "risk_free_rate_pct": {"type": "number", "description": "Risk-free rate as a percentage."},
            "volatility_pct": {"type": "number", "description": "Option vol as a percentage (must be > 0)."},
            "time_to_expiry_start_years": {"type": "number", "description": "Time to expiry at the start of the path (must be > 0)."},
            "option_type": {"type": "string", "enum": ["call", "put"]},
            "notional": {"type": "number", "default": 1.0, "description": "Option notional multiplier."},
        },
        "required": [
            "spot_prices",
            "strike",
            "risk_free_rate_pct",
            "volatility_pct",
            "time_to_expiry_start_years",
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
                    "hedge_pnl_series": {"type": "array", "items": {"type": "number"}},
                    "option_pnl": {"type": "number"},
                    "gamma_pnl": {"type": "number"},
                    "theta_pnl": {"type": "number"},
                    "residual_pnl": {"type": "number"},
                    "hedge_effectiveness_pct": {"type": "number"},
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


def _bs_price_delta_gamma(
    spot: float, strike: float, r: float, sigma: float, tau: float, option_type: str
) -> tuple[float, float, float]:
    """Return (price, delta, gamma) using Black-Scholes.

    At tau=0, returns intrinsic value and binary delta.
    """
    if tau <= 0 or sigma <= 0:
        intrinsic = max(spot - strike, 0.0) if option_type == "call" else max(strike - spot, 0.0)
        # Delta at expiry: 1 if in-the-money call, -1 if in-the-money put, 0 otherwise
        if option_type == "call":
            delta = 1.0 if spot > strike else 0.0
        else:
            delta = -1.0 if spot < strike else 0.0
        return intrinsic, delta, 0.0

    sqrt_t = math.sqrt(tau)
    d1 = (math.log(spot / strike) + (r + 0.5 * sigma ** 2) * tau) / (sigma * sqrt_t)
    d2 = d1 - sigma * sqrt_t

    disc = math.exp(-r * tau)
    if option_type == "call":
        price = spot * _cdf(d1) - strike * disc * _cdf(d2)
        delta = _cdf(d1)
    else:
        price = strike * disc * _cdf(-d2) - spot * _cdf(-d1)
        delta = _cdf(d1) - 1.0

    gamma = _pdf(d1) / (spot * sigma * sqrt_t)
    return price, delta, gamma


def delta_hedging_simulator(
    spot_prices: list[float],
    strike: float,
    risk_free_rate_pct: float,
    volatility_pct: float,
    time_to_expiry_start_years: float,
    option_type: str,
    notional: float = 1.0,
    **_: Any,
) -> dict[str, Any]:
    """Simulate discrete delta hedging and decompose P&L into gamma and theta.

    Each step:
      - hedge_pnl: gain/loss from delta-hedging the option change
      - gamma_pnl: accumulated 0.5 * gamma * dS^2 (convexity gain)
      - theta_pnl: accumulated theta decay

    Args:
        spot_prices: Price path (>= 2 observations).
        strike: Strike price (must be > 0).
        risk_free_rate_pct: Risk-free rate as a percentage.
        volatility_pct: Volatility as a percentage (must be > 0).
        time_to_expiry_start_years: Time to expiry at first observation (must be > 0).
        option_type: 'call' or 'put'.
        notional: Notional multiplier.

    Returns:
        dict with hedge_pnl_series, option_pnl, gamma_pnl, theta_pnl,
        residual_pnl, hedge_effectiveness_pct.
    """
    try:
        if not spot_prices or len(spot_prices) < 2:
            raise ValueError("spot_prices must contain at least two observations")
        if strike <= 0:
            raise ValueError("strike must be positive")
        if volatility_pct <= 0:
            raise ValueError("volatility_pct must be positive")
        if time_to_expiry_start_years <= 0:
            raise ValueError("time_to_expiry_start_years must be positive")

        option_type = option_type.lower()
        if option_type not in {"call", "put"}:
            raise ValueError("option_type must be 'call' or 'put'")

        r = risk_free_rate_pct / 100.0
        sigma = volatility_pct / 100.0
        horizon = time_to_expiry_start_years
        n_steps = len(spot_prices) - 1
        dt = horizon / n_steps

        initial_price, _, _ = _bs_price_delta_gamma(spot_prices[0], strike, r, sigma, horizon, option_type)
        prev_price, prev_delta, prev_gamma = initial_price, *_bs_price_delta_gamma(spot_prices[0], strike, r, sigma, horizon, option_type)[1:]

        hedge_pnl_series: list[float] = []
        gamma_pnl = 0.0
        theta_pnl = 0.0

        for idx in range(1, len(spot_prices)):
            tau = max(horizon - idx * dt, 0.0)
            price, delta, gamma = _bs_price_delta_gamma(spot_prices[idx], strike, r, sigma, tau, option_type)
            d_spot = spot_prices[idx] - spot_prices[idx - 1]

            # Hedge P&L: gain from short delta hedge offsetting option value change
            hedge_step = -prev_delta * d_spot * notional
            hedge_pnl_series.append(round(hedge_step, 4))

            # Gamma P&L (convexity benefit): long gamma earns 0.5*gamma*dS^2
            gamma_pnl += 0.5 * prev_gamma * (d_spot ** 2) * notional

            # Theta P&L: residual after delta and gamma explain option change
            option_change = (price - prev_price) * notional
            theta_step = option_change - prev_delta * d_spot * notional - 0.5 * prev_gamma * (d_spot ** 2) * notional
            theta_pnl += theta_step

            prev_price, prev_delta, prev_gamma = price, delta, gamma

        option_pnl = (prev_price - initial_price) * notional
        total_hedge_pnl = sum(hedge_pnl_series)
        residual_pnl = option_pnl + total_hedge_pnl
        hedge_effectiveness = 1 - abs(residual_pnl) / (abs(option_pnl) + 1e-9)

        data = {
            "hedge_pnl_series": hedge_pnl_series,
            "option_pnl": round(option_pnl, 2),
            "gamma_pnl": round(gamma_pnl, 2),
            "theta_pnl": round(theta_pnl, 2),
            "residual_pnl": round(residual_pnl, 2),
            "hedge_effectiveness_pct": round(hedge_effectiveness * 100, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson(f"delta_hedging_simulator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
