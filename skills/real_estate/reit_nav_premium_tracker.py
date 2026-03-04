"""
Executive Summary: Tracks REIT market price premium/discount to NAV and computes z-score vs historical premiums.
Inputs: market_price (float), nav_per_share (float), historical_premiums (list of floats, optional)
Outputs: dict with premium_pct (float), signal (str: overvalued/undervalued/fair), z_score (float or null)
MCP Tool Name: reit_nav_premium_tracker
"""
import os
import logging
import math
from typing import Any, Optional
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "reit_nav_premium_tracker",
    "description": (
        "Tracks the premium or discount of a REIT's market price relative to "
        "Net Asset Value (NAV) per share. Computes a z-score against historical "
        "premiums (when provided) and signals overvalued, undervalued, or fair value."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "market_price": {
                "type": "number",
                "description": "Current market price per share (dollars)."
            },
            "nav_per_share": {
                "type": "number",
                "description": "Estimated NAV per share (dollars)."
            },
            "historical_premiums": {
                "type": "array",
                "items": {"type": "number"},
                "description": "Historical premium percentages (e.g., [5.2, -3.1, 8.0]) for z-score context."
            }
        },
        "required": ["market_price", "nav_per_share"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "premium_pct":  {"type": "number"},
                    "signal":       {"type": "string"},
                    "z_score":      {"type": ["number", "null"]},
                    "historical_avg_premium_pct": {"type": ["number", "null"]}
                },
                "required": ["premium_pct", "signal", "z_score"]
            },
            "timestamp": {"type": "string"}
        },
        "required": ["status", "timestamp"]
    }
}

# Signal thresholds (percentage points from historical mean or absolute)
# Without history: use absolute bands
FAIR_VALUE_BAND_PCT: float = 5.0          # +/- 5% of NAV = fair value (no history)
OVERVALUED_THRESHOLD_PCT: float = 5.0     # > +5% premium = overvalued signal
UNDERVALUED_THRESHOLD_PCT: float = -5.0   # < -5% discount = undervalued signal

# With history: z-score thresholds
Z_OVERVALUED: float = 1.5    # > 1.5 std devs above mean = overvalued
Z_UNDERVALUED: float = -1.5  # < -1.5 std devs below mean = undervalued


def reit_nav_premium_tracker(
    market_price: float,
    nav_per_share: float,
    historical_premiums: Optional[list[float]] = None,
    **kwargs: Any
) -> dict:
    """Compute REIT premium/discount to NAV and generate a valuation signal.

    premium_pct = (market_price - nav_per_share) / nav_per_share * 100

    Signal classification:
    - Without historical_premiums: uses absolute +/-5% bands.
    - With historical_premiums: uses z-score relative to historical mean/std.
      z_score = (current_premium - hist_mean) / hist_std_dev
      Overvalued if z > 1.5, undervalued if z < -1.5, else fair.

    Args:
        market_price: Current market price per share in dollars.
        nav_per_share: Estimated NAV per share in dollars.
        historical_premiums: Optional list of historical premium percentages
            (e.g., [5.2, -3.1, 8.4]) for z-score relative comparison.
        **kwargs: Ignored extra keyword arguments for MCP compatibility.

    Returns:
        dict with keys: status, data (premium_pct, signal, z_score,
        historical_avg_premium_pct, historical_std_dev_pct,
        premium_to_historical_avg), timestamp.

    Raises:
        ValueError: If nav_per_share is zero or negative, or market_price is negative.
    """
    try:
        market_price = float(market_price)
        nav_per_share = float(nav_per_share)

        if nav_per_share <= 0:
            raise ValueError(f"nav_per_share must be positive, got {nav_per_share}")
        if market_price < 0:
            raise ValueError(f"market_price cannot be negative, got {market_price}")

        # Core premium calculation
        premium_pct: float = round((market_price - nav_per_share) / nav_per_share * 100, 4)
        premium_decimal: float = (market_price - nav_per_share) / nav_per_share

        z_score: Optional[float] = None
        hist_avg: Optional[float] = None
        hist_std: Optional[float] = None
        signal: str

        if historical_premiums and len(historical_premiums) >= 2:
            # Normalize historical premiums: if any > 1 and < 100, assume already in %
            # If any > 100, flag as suspicious but use as-is
            hist_pcts = [float(p) for p in historical_premiums]

            n = len(hist_pcts)
            hist_avg = sum(hist_pcts) / n
            variance = sum((p - hist_avg) ** 2 for p in hist_pcts) / n
            hist_std = math.sqrt(variance)

            if hist_std > 0:
                z_score = round((premium_pct - hist_avg) / hist_std, 4)
            else:
                z_score = 0.0  # All historical values identical

            # Signal based on z-score
            if z_score > Z_OVERVALUED:
                signal = "overvalued"
            elif z_score < Z_UNDERVALUED:
                signal = "undervalued"
            else:
                signal = "fair"

        else:
            # No sufficient historical context — use absolute bands
            if historical_premiums and len(historical_premiums) == 1:
                logger.warning(
                    "Only 1 historical premium provided; z-score requires >= 2. Using absolute bands."
                )

            if premium_pct > OVERVALUED_THRESHOLD_PCT:
                signal = "overvalued"
            elif premium_pct < UNDERVALUED_THRESHOLD_PCT:
                signal = "undervalued"
            else:
                signal = "fair"

        result: dict = {
            "market_price": market_price,
            "nav_per_share": nav_per_share,
            "premium_pct": premium_pct,
            "premium_decimal": round(premium_decimal, 6),
            "signal": signal,
            "z_score": z_score,
            "historical_avg_premium_pct": round(hist_avg, 4) if hist_avg is not None else None,
            "historical_std_dev_pct": round(hist_std, 4) if hist_std is not None else None,
            "n_historical_observations": len(historical_premiums) if historical_premiums else 0,
            "signal_method": "z_score" if z_score is not None else "absolute_bands",
            "interpretation": _build_interpretation(premium_pct, signal, z_score, hist_avg)
        }

        logger.info(
            "reit_nav_premium_tracker: premium=%.4f%%, signal=%s, z_score=%s",
            premium_pct, signal, z_score
        )

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except Exception as e:
        logger.error("reit_nav_premium_tracker failed: %s", e)
        _log_lesson(f"reit_nav_premium_tracker: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _build_interpretation(
    premium_pct: float,
    signal: str,
    z_score: Optional[float],
    hist_avg: Optional[float]
) -> str:
    """Construct a human-readable interpretation string.

    Args:
        premium_pct: Current premium as a percentage.
        signal: Valuation signal ('overvalued', 'undervalued', or 'fair').
        z_score: Z-score vs historical or None.
        hist_avg: Historical average premium or None.

    Returns:
        Descriptive interpretation string.
    """
    direction = "premium" if premium_pct >= 0 else "discount"
    abs_pct = abs(premium_pct)

    if z_score is not None and hist_avg is not None:
        return (
            f"Trading at a {abs_pct:.2f}% {direction} to NAV. "
            f"Historical average premium: {hist_avg:.2f}%. "
            f"Z-score of {z_score:.2f} indicates '{signal}' relative to history."
        )
    else:
        return (
            f"Trading at a {abs_pct:.2f}% {direction} to NAV. "
            f"Signal '{signal}' based on absolute +/-{FAIR_VALUE_BAND_PCT:.0f}% fair-value band."
        )


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
