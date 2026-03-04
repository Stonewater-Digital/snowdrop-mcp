"""Price FX options using Garman-Kohlhagen."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "fx_option_pricer",
    "description": "Calculates FX option premiums and Greeks via Garman-Kohlhagen model.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "spot_rate": {"type": "number"},
            "strike": {"type": "number"},
            "domestic_rate": {"type": "number"},
            "foreign_rate": {"type": "number"},
            "volatility": {"type": "number"},
            "time_to_expiry_years": {"type": "number"},
            "option_type": {"type": "string", "enum": ["call", "put"]},
            "notional": {"type": "number"},
        },
        "required": [
            "spot_rate",
            "strike",
            "domestic_rate",
            "foreign_rate",
            "volatility",
            "time_to_expiry_years",
            "option_type",
            "notional",
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


def fx_option_pricer(
    spot_rate: float,
    strike: float,
    domestic_rate: float,
    foreign_rate: float,
    volatility: float,
    time_to_expiry_years: float,
    option_type: str,
    notional: float,
    **_: Any,
) -> dict[str, Any]:
    """Return option premium and Greeks."""
    try:
        if time_to_expiry_years <= 0 or volatility <= 0:
            raise ValueError("time_to_expiry_years and volatility must be positive")
        sigma_sqrt = volatility * math.sqrt(time_to_expiry_years)
        d1 = (math.log(spot_rate / strike) + (domestic_rate - foreign_rate + 0.5 * volatility**2) * time_to_expiry_years) / sigma_sqrt
        d2 = d1 - sigma_sqrt
        disc_dom = math.exp(-domestic_rate * time_to_expiry_years)
        disc_for = math.exp(-foreign_rate * time_to_expiry_years)
        if option_type == "call":
            premium = notional * (spot_rate * disc_for * _norm_cdf(d1) - strike * disc_dom * _norm_cdf(d2))
        else:
            premium = notional * (strike * disc_dom * _norm_cdf(-d2) - spot_rate * disc_for * _norm_cdf(-d1))
        delta = disc_for * _norm_cdf(d1) if option_type == "call" else -disc_for * _norm_cdf(-d1)
        gamma = disc_for * math.exp(-0.5 * d1**2) / (spot_rate * sigma_sqrt * math.sqrt(2 * math.pi))
        vega = spot_rate * disc_for * math.sqrt(time_to_expiry_years) * math.exp(-0.5 * d1**2) / math.sqrt(2 * math.pi)
        theta = (
            -spot_rate * disc_for * math.exp(-0.5 * d1**2) * volatility / (2 * math.sqrt(2 * math.pi * time_to_expiry_years))
            - domestic_rate * strike * disc_dom * (_norm_cdf(d2) if option_type == "call" else _norm_cdf(-d2))
            + foreign_rate * spot_rate * disc_for * (_norm_cdf(d1) if option_type == "call" else _norm_cdf(-d1))
        )
        breakeven = strike + premium / notional if option_type == "call" else strike - premium / notional
        data = {
            "premium": round(premium, 4),
            "premium_pips": round(premium / notional * 10000, 2),
            "delta": round(delta, 4),
            "gamma": round(gamma, 6),
            "vega": round(vega, 4),
            "theta": round(theta, 4),
            "breakeven_rate": round(breakeven, 4),
            "notional_risk": round(delta * notional, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("fx_option_pricer", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _norm_cdf(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
