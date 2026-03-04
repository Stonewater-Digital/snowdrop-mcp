"""
Executive Summary: Prices payer/receiver CDS options using the Black (1976) framework with risky DV01 scaling.
Inputs: forward_spread_bp (float), strike_bp (float), volatility (float), maturity_years (float), risk_free_rate (float), hazard_rate (float), notional (float), option_type (str)
Outputs: status (str), timestamp (str), data (dict)
MCP Tool Name: cds_option_pricer
"""
import logging
import math
from datetime import datetime, timezone
from statistics import NormalDist
from typing import Any

logger = logging.getLogger("snowdrop.skills")
ND = NormalDist()

TOOL_META = {
    "name": "cds_option_pricer",
    "description": "Applies the Black (1976) model with risky DV01 scaling to CDS swaptions for payer/receiver structures.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "forward_spread_bp": {
                "type": "number",
                "description": "Forward CDS spread in basis points over the option expiry."
            },
            "strike_bp": {
                "type": "number",
                "description": "Strike spread in basis points."
            },
            "volatility": {
                "type": "number",
                "description": "Black implied volatility (decimal)."
            },
            "maturity_years": {
                "type": "number",
                "description": "Option expiry in years."
            },
            "risk_free_rate": {
                "type": "number",
                "description": "Continuously compounded risk-free rate."
            },
            "hazard_rate": {
                "type": "number",
                "description": "Flat hazard rate used for risky DV01."
            },
            "notional": {
                "type": "number",
                "description": "Reference notional in currency units."
            },
            "option_type": {
                "type": "string",
                "description": "'payer' for payer swaption (call on spread) or 'receiver' (put)."
            }
        },
        "required": [
            "forward_spread_bp",
            "strike_bp",
            "volatility",
            "maturity_years",
            "risk_free_rate",
            "hazard_rate",
            "notional",
            "option_type"
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


def cds_option_pricer(**kwargs: Any) -> dict[str, Any]:
    try:
        f_spread = float(kwargs["forward_spread_bp"]) / 10000.0
        strike = float(kwargs["strike_bp"]) / 10000.0
        vol = float(kwargs["volatility"])
        maturity = float(kwargs["maturity_years"])
        rate = float(kwargs["risk_free_rate"])
        hazard = float(kwargs["hazard_rate"])
        notional = float(kwargs["notional"])
        opt_type = str(kwargs["option_type"]).strip().lower()
        if maturity <= 0 or vol <= 0:
            raise ValueError("maturity_years and volatility must be positive")
        if opt_type not in {"payer", "receiver"}:
            raise ValueError("option_type must be 'payer' or 'receiver'")

        sigma_root_t = vol * math.sqrt(maturity)
        if sigma_root_t == 0:
            raise ValueError("volatility * sqrt(maturity) cannot be zero")
        variance_term = vol * vol * maturity
        d1 = (math.log(f_spread / strike) + 0.5 * variance_term) / sigma_root_t
        d2 = d1 - sigma_root_t
        discount_factor = math.exp(-rate * maturity)
        risky_dv01 = discount_factor * (1 - math.exp(-(hazard + rate) * maturity)) / max(hazard + rate, 1e-8)

        if opt_type == "payer":
            price = risky_dv01 * (f_spread * ND.cdf(d1) - strike * ND.cdf(d2)) * notional
            delta = risky_dv01 * ND.cdf(d1) * notional
        else:
            price = risky_dv01 * (strike * ND.cdf(-d2) - f_spread * ND.cdf(-d1)) * notional
            delta = -risky_dv01 * ND.cdf(-d1) * notional

        implied_spread_move = price / max(risky_dv01 * notional, 1e-8)
        data = {
            "option_price": price,
            "discount_factor": discount_factor,
            "risky_dv01": risky_dv01,
            "delta": delta,
            "implied_spread_move": implied_spread_move,
            "d1": d1,
            "d2": d2
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError, KeyError) as e:
        logger.error("cds_option_pricer failed: %s", e)
        _log_lesson(f"cds_option_pricer: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as file:
            file.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
