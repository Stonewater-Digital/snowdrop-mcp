"""
Executive Summary: Forecasts next 3-period occupancy rates via linear regression on historical data with market factor adjustments.
Inputs: historical_rates (list of dicts: period, rate), market_absorption_rate (float, optional), new_supply_pct (float, optional)
Outputs: dict with forecast_next_3 (list of floats), trend (str), confidence (float 0-1)
MCP Tool Name: occupancy_rate_forecaster
"""
import os
import logging
import math
from typing import Any, Optional
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "occupancy_rate_forecaster",
    "description": (
        "Forecasts occupancy rates for the next 3 periods using simple linear "
        "regression on historical data, with optional adjustments for market "
        "absorption rate and new supply entering the market."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "historical_rates": {
                "type": "array",
                "description": "Historical occupancy data points, ordered oldest to newest.",
                "items": {
                    "type": "object",
                    "properties": {
                        "period": {"type": "string", "description": "Period label (e.g., 'Q1-2023')."},
                        "rate":   {"type": "number", "description": "Occupancy rate as decimal (e.g., 0.92) or percent (e.g., 92)."}
                    },
                    "required": ["period", "rate"]
                }
            },
            "market_absorption_rate": {
                "type": "number",
                "description": "Expected net absorption rate as decimal (positive = demand > supply)."
            },
            "new_supply_pct": {
                "type": "number",
                "description": "Percentage of new competing supply entering market as decimal (e.g., 0.03 = 3%)."
            }
        },
        "required": ["historical_rates"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "forecast_next_3":  {"type": "array", "items": {"type": "number"}},
                    "trend":            {"type": "string"},
                    "confidence":       {"type": "number"},
                    "regression_slope": {"type": "number"},
                    "r_squared":        {"type": "number"}
                },
                "required": ["forecast_next_3", "trend", "confidence"]
            },
            "timestamp": {"type": "string"}
        },
        "required": ["status", "timestamp"]
    }
}

TREND_STABLE_BAND: float = 0.002   # Less than 0.2pp per period = stable


def occupancy_rate_forecaster(
    historical_rates: list[dict],
    market_absorption_rate: Optional[float] = None,
    new_supply_pct: Optional[float] = None,
    **kwargs: Any
) -> dict:
    """Forecast next 3-period occupancy rates using OLS linear regression.

    Fits a simple linear trend (y = mx + b) to historical occupancy data.
    Optionally adjusts the forecast by:
      - market_absorption_rate: adds positive pressure (demand > supply)
      - new_supply_pct: adds negative pressure (new competition)

    Confidence is derived from R-squared of the regression fit, reduced by
    data sparsity (fewer than 6 observations lowers confidence).

    Args:
        historical_rates: List of dicts with 'period' (str) and 'rate' (float).
            Rates may be given as decimals (0.92) or percentages (92.0);
            values > 1 are auto-normalized to decimal form.
        market_absorption_rate: Net absorption expressed as decimal adjustment
            per forecast period (optional). Positive increases forecast.
        new_supply_pct: New competing supply as decimal fraction of total market
            (optional). Negative pressure per forecast period.
        **kwargs: Ignored extra keyword arguments for MCP compatibility.

    Returns:
        dict with keys: status, data (forecast_next_3, trend, confidence,
        regression_slope, r_squared, market_adjusted), timestamp.

    Raises:
        ValueError: If fewer than 2 historical data points are provided.
    """
    try:
        if not historical_rates or len(historical_rates) < 2:
            raise ValueError("At least 2 historical_rates data points are required.")

        # Extract and normalize rates
        rates: list[float] = []
        for i, entry in enumerate(historical_rates):
            if "rate" not in entry:
                raise ValueError(f"historical_rates[{i}] missing 'rate' field.")
            r = float(entry["rate"])
            # Auto-normalize: if > 1.0, assume it was given as percentage
            if r > 1.0:
                r = r / 100.0
            if not (0.0 <= r <= 1.0):
                raise ValueError(
                    f"historical_rates[{i}] rate {r} is out of [0, 1] range after normalization."
                )
            rates.append(r)

        n = len(rates)
        xs = list(range(n))

        # OLS linear regression: y = slope * x + intercept
        x_mean = sum(xs) / n
        y_mean = sum(rates) / n

        ss_xy = sum((xs[i] - x_mean) * (rates[i] - y_mean) for i in range(n))
        ss_xx = sum((xs[i] - x_mean) ** 2 for i in range(n))

        slope: float = ss_xy / ss_xx if ss_xx != 0 else 0.0
        intercept: float = y_mean - slope * x_mean

        # R-squared
        ss_res = sum((rates[i] - (slope * xs[i] + intercept)) ** 2 for i in range(n))
        ss_tot = sum((r - y_mean) ** 2 for r in rates)
        r_squared: float = 1.0 - (ss_res / ss_tot) if ss_tot != 0 else 1.0

        # Market factor adjustments per forecast period
        absorption_adj: float = float(market_absorption_rate) if market_absorption_rate is not None else 0.0
        supply_adj: float = -float(new_supply_pct) if new_supply_pct is not None else 0.0
        net_market_adj: float = absorption_adj + supply_adj

        # Generate 3 forecast periods
        forecast_next_3: list[float] = []
        for step in range(1, 4):
            raw_forecast = slope * (n - 1 + step) + intercept
            adjusted = raw_forecast + (net_market_adj * step)
            # Clamp to [0, 1]
            clamped = max(0.0, min(1.0, adjusted))
            forecast_next_3.append(round(clamped, 4))

        # Trend classification based on slope
        if slope > TREND_STABLE_BAND:
            trend = "improving"
        elif slope < -TREND_STABLE_BAND:
            trend = "declining"
        else:
            trend = "stable"

        # Confidence: R-squared penalized for sparse data (< 6 obs)
        sparsity_penalty = max(0.0, (6 - n) * 0.05)
        confidence: float = round(max(0.0, min(1.0, r_squared - sparsity_penalty)), 4)

        market_adjusted: bool = (market_absorption_rate is not None or new_supply_pct is not None)

        result: dict = {
            "historical_periods": [e.get("period", f"T-{n-i}") for i, e in enumerate(historical_rates)],
            "historical_rates_normalized": [round(r, 4) for r in rates],
            "forecast_next_3": forecast_next_3,
            "trend": trend,
            "confidence": confidence,
            "regression_slope": round(slope, 6),
            "regression_intercept": round(intercept, 6),
            "r_squared": round(r_squared, 4),
            "n_observations": n,
            "market_adjusted": market_adjusted,
        }

        if market_adjusted:
            result["net_market_adjustment_per_period"] = round(net_market_adj, 4)
            if market_absorption_rate is not None:
                result["market_absorption_rate"] = market_absorption_rate
            if new_supply_pct is not None:
                result["new_supply_pct"] = new_supply_pct

        logger.info(
            "occupancy_rate_forecaster: trend=%s, slope=%.4f, R2=%.4f, confidence=%.4f",
            trend, slope, r_squared, confidence
        )

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except Exception as e:
        logger.error("occupancy_rate_forecaster failed: %s", e)
        _log_lesson(f"occupancy_rate_forecaster: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _log_lesson(message: str) -> None:
    """Append a lesson-learned entry to the shared lessons log.

    Args:
        message: Description of the error or lesson to record.
    """
    try:
        os.makedirs("logs", exist_ok=True)
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError as log_err:
        logger.warning("Could not write to lessons.md: %s", log_err)
