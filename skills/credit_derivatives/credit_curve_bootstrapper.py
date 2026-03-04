"""
Executive Summary: Bootstraps piecewise-constant hazard rates from CDS spreads using ISDA premium/protection balance.
Inputs: tenors_years (list[float]), spreads_bp (list[float]), discount_factors (list[float]), recovery_rate (float)
Outputs: status (str), timestamp (str), data (dict)
MCP Tool Name: credit_curve_bootstrapper
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "credit_curve_bootstrapper",
    "description": (
        "Solves for piecewise-constant hazard rates that match CDS spreads under the ISDA "
        "standard model (premium leg equals protection leg per tenor)."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "tenors_years": {
                "type": "array",
                "items": {"type": "number"},
                "description": "Ascending list of CDS maturities in years."
            },
            "spreads_bp": {
                "type": "array",
                "items": {"type": "number"},
                "description": "Quoted running spreads in basis points for each tenor."
            },
            "discount_factors": {
                "type": "array",
                "items": {"type": "number"},
                "description": "Discount factors at each tenor from the risk-free curve."
            },
            "recovery_rate": {
                "type": "number",
                "description": "Assumed recovery rate (0-1) used across the curve."
            }
        },
        "required": ["tenors_years", "spreads_bp", "discount_factors", "recovery_rate"]
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


def credit_curve_bootstrapper(**kwargs: Any) -> dict[str, Any]:
    try:
        tenors = _clean_positive_vector(kwargs["tenors_years"])
        spreads = _clean_positive_vector(kwargs["spreads_bp"])
        dfs = _clean_positive_vector(kwargs["discount_factors"], strictly_positive=False)
        recovery = float(kwargs["recovery_rate"])
        if len(tenors) != len(spreads) or len(tenors) != len(dfs):
            raise ValueError("Input vectors must share the same length")
        if not 0.0 <= recovery < 1.0:
            raise ValueError("recovery_rate must lie in [0,1)")

        prev_t = 0.0
        prev_df = 1.0
        survival = 1.0
        hazard_rates: list[float] = []
        survival_curve = [survival]

        for t, spread_bp, df in zip(tenors, spreads, dfs):
            if t <= prev_t:
                raise ValueError("tenors must be strictly increasing")
            delta = t - prev_t
            spread = spread_bp / 10000.0
            df_mid = 0.5 * (prev_df + df)
            premium_coef = spread * df_mid * delta / 2.0
            protection_coef = (1 - recovery) * df
            numerator = protection_coef - premium_coef
            denominator = protection_coef + premium_coef
            if denominator <= 0:
                raise ValueError("Invalid premium/protection balance for tenor")
            s_end = survival * numerator / denominator
            s_end = max(min(s_end, survival * 0.999999), 1e-8)
            hazard = -math.log(s_end / survival) / delta
            hazard_rates.append(hazard)
            survival = s_end
            survival_curve.append(survival)
            prev_t = t
            prev_df = df

        data = {
            "hazard_rates": hazard_rates,
            "survival_probabilities": survival_curve[1:],
            "cumulative_default_probability": [1 - s for s in survival_curve[1:]],
            "tenors_years": tenors
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError, KeyError) as e:
        logger.error("credit_curve_bootstrapper failed: %s", e)
        _log_lesson(f"credit_curve_bootstrapper: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _clean_positive_vector(values: Sequence[Any], strictly_positive: bool = True) -> list[float]:
    if not values:
        raise ValueError("Vector inputs must be non-empty")
    cleaned = []
    for val in values:
        num = float(val)
        if strictly_positive and num <= 0:
            raise ValueError("Values must be positive")
        cleaned.append(num)
    return cleaned


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as file:
            file.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
