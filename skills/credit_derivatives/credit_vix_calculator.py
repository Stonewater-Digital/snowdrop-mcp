"""
Executive Summary: Computes implied credit volatility (credit VIX) from CDS option quotes via the CBOE variance methodology.
Inputs: strikes_bp (list[float]), option_prices_bp (list[float]), forward_spread_bp (float), maturity_years (float)
Outputs: status (str), timestamp (str), data (dict)
MCP Tool Name: credit_vix_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "credit_vix_calculator",
    "description": "Uses the VIX variance replication formula on CDS option strips to infer an implied volatility index for credit spreads.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "strikes_bp": {
                "type": "array",
                "items": {"type": "number"},
                "description": "Ordered strike spreads in basis points."
            },
            "option_prices_bp": {
                "type": "array",
                "items": {"type": "number"},
                "description": "Out-of-the-money option mid prices in basis points of spread PV."
            },
            "forward_spread_bp": {
                "type": "number",
                "description": "Forward CDS spread in basis points corresponding to the strip."
            },
            "maturity_years": {
                "type": "number",
                "description": "Time to option expiry in years."
            }
        },
        "required": ["strikes_bp", "option_prices_bp", "forward_spread_bp", "maturity_years"]
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


def credit_vix_calculator(**kwargs: Any) -> dict[str, Any]:
    try:
        strikes = _clean_vector(kwargs["strikes_bp"])
        prices = _clean_vector(kwargs["option_prices_bp"])
        forward = float(kwargs["forward_spread_bp"]) / 10000.0
        maturity = float(kwargs["maturity_years"])
        if len(strikes) != len(prices):
            raise ValueError("strikes_bp and option_prices_bp must align")
        if maturity <= 0:
            raise ValueError("maturity_years must be positive")

        strikes_dec = [k / 10000.0 for k in strikes]
        option_prices = [max(p, 0.0) / 10000.0 for p in prices]
        if any(k <= forward for k in strikes_dec):
            k0_idx = max(i for i, k in enumerate(strikes_dec) if k <= forward)
        else:
            k0_idx = 0
        variance_sum = 0.0
        for i in range(len(strikes_dec)):
            if i == 0:
                delta_k = strikes_dec[1] - strikes_dec[0]
            elif i == len(strikes_dec) - 1:
                delta_k = strikes_dec[-1] - strikes_dec[-2]
            else:
                delta_k = 0.5 * (strikes_dec[i + 1] - strikes_dec[i - 1])
            price = option_prices[i]
            variance_sum += (delta_k / (strikes_dec[i] ** 2)) * price

        variance = (2 / maturity) * variance_sum - (
            (forward / strikes_dec[k0_idx] - 1) ** 2 / maturity
        )
        variance = max(variance, 0.0)
        credit_vix = math.sqrt(variance) * 100

        data = {
            "variance": variance,
            "credit_vix": credit_vix,
            "forward_spread": forward,
            "time_to_expiry": maturity,
            "k0": strikes[k0_idx]
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError, KeyError) as e:
        logger.error("credit_vix_calculator failed: %s", e)
        _log_lesson(f"credit_vix_calculator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _clean_vector(values: Sequence[Any]) -> list[float]:
    if not values:
        raise ValueError("Input arrays must be non-empty")
    return [float(v) for v in values]


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as file:
            file.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
