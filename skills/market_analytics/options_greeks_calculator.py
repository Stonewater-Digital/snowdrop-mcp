"""
Execuve Summary: Calculates Black-Scholes option price and Greeks.
Inputs: stock_price (float), strike (float), time_to_expiry_years (float), risk_free_rate (float), volatility (float), option_type (str)
Outputs: price (float), delta (float), gamma (float), theta (float), vega (float), rho (float), intrinsic_value (float), time_value (float)
MCP Tool Name: options_greeks_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "options_greeks_calculator",
    "description": "Computes Black-Scholes option price and Greeks for calls and puts.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "stock_price": {"type": "number", "description": "Underlying price."},
            "strike": {"type": "number", "description": "Option strike."},
            "time_to_expiry_years": {"type": "number", "description": "Time to expiration in years."},
            "risk_free_rate": {"type": "number", "description": "Risk-free rate (decimal)."},
            "volatility": {"type": "number", "description": "Implied volatility (decimal)."},
            "option_type": {"type": "string", "description": "call or put."}
        },
        "required": ["stock_price", "strike", "time_to_expiry_years", "risk_free_rate", "volatility", "option_type"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def options_greeks_calculator(**kwargs: Any) -> dict:
    """Applies Black-Scholes formulas."""
    try:
        s = kwargs.get("stock_price")
        k = kwargs.get("strike")
        t = kwargs.get("time_to_expiry_years")
        r = kwargs.get("risk_free_rate")
        vol = kwargs.get("volatility")
        option_type = kwargs.get("option_type", "call").lower()
        for label, value in (("stock_price", s), ("strike", k), ("time_to_expiry_years", t), ("risk_free_rate", r), ("volatility", vol)):
            if not isinstance(value, (int, float)) or value <= 0:
                raise ValueError(f"{label} must be positive")
        if option_type not in {"call", "put"}:
            raise ValueError("option_type must be 'call' or 'put'")

        d1 = (math.log(s / k) + (r + 0.5 * vol ** 2) * t) / (vol * math.sqrt(t))
        d2 = d1 - vol * math.sqrt(t)
        nd1 = _norm_cdf(d1)
        nd2 = _norm_cdf(d2)
        price = s * nd1 - k * math.exp(-r * t) * nd2 if option_type == "call" else k * math.exp(-r * t) * _norm_cdf(-d2) - s * _norm_cdf(-d1)
        delta = nd1 if option_type == "call" else nd1 - 1
        gamma = _norm_pdf(d1) / (s * vol * math.sqrt(t))
        theta = (
            - (s * _norm_pdf(d1) * vol) / (2 * math.sqrt(t))
            - r * k * math.exp(-r * t) * nd2
            if option_type == "call"
            else - (s * _norm_pdf(d1) * vol) / (2 * math.sqrt(t)) + r * k * math.exp(-r * t) * _norm_cdf(-d2)
        )
        vega = s * _norm_pdf(d1) * math.sqrt(t)
        rho = k * t * math.exp(-r * t) * nd2 if option_type == "call" else -k * t * math.exp(-r * t) * _norm_cdf(-d2)
        intrinsic = max(s - k, 0) if option_type == "call" else max(k - s, 0)
        time_value = price - intrinsic

        return {
            "status": "success",
            "data": {
                "price": price,
                "delta": delta,
                "gamma": gamma,
                "theta": theta,
                "vega": vega,
                "rho": rho,
                "intrinsic_value": intrinsic,
                "time_value": time_value
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"options_greeks_calculator failed: {e}")
        _log_lesson(f"options_greeks_calculator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _norm_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)


def _norm_cdf(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
