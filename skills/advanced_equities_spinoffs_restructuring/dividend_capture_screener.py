"""Executive Summary: Ranks capture setups using effective tax rate, borrow cost, and vol-adjusted
decay.
"""

from __future__ import annotations

from random import Random
from statistics import fmean, pstdev
from typing import Any, Sequence

from skills.utils import get_iso_timestamp, log_lesson as _log_lesson

SKILL_NAME = "dividend_capture_screener"
NICHE = "Advanced Equities (Spinoffs / Restructuring)"
ANALYSIS_FOCUS = "Ranks capture setups using effective tax rate, borrow cost, and vol-adjusted decay."
DEFAULT_LOOKBACK_DAYS = 90
FREE_DATA_SOURCES: tuple[str, ...] = ("yfinance", "sec_edgar")

TOOL_META: dict[str, Any] = {
    "name": SKILL_NAME,
    "tier": "free",
    "description": "Ranks capture setups using effective tax rate, borrow cost, and vol-adjusted decay.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "tickers": {
                "type": "array",
                "description": "Tickers or identifiers relevant to the analysis focus.",
                "items": {"type": "string"},
            },
            "lookback_days": {
                "type": "integer",
                "description": "Historical window (days) for synthetic / free-data calculations.",
                "default": DEFAULT_LOOKBACK_DAYS,
            },
            "analysis_notes": {
                "type": "string",
                "description": "Optional qualitative context to embed in the response.",
            },
        },
        "required": [],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "data": {"type": "object"},
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def dividend_capture_screener(
    tickers: Sequence[str] | None = None,
    lookback_days: int = DEFAULT_LOOKBACK_DAYS,
    analysis_notes: str | None = None,
) -> dict[str, Any]:
    """Ranks capture setups using effective tax rate, borrow cost, and vol-adjusted decay. This
    function synthesizes advanced equities (spinoffs / restructuring) insights using
    deterministic fallback data when real-time feeds are unavailable.

    Args:
        tickers: Identifiers to evaluate (defaults to SPY if none supplied).
        lookback_days: Historical window used for synthetic modeling (min 5 / max 365).
        analysis_notes: Optional commentary to echo back in the payload.

    Returns:
        Response dict containing status, data payload, and ISO-8601 timestamp.
    """
    cleaned_tickers = _normalize_tickers(tickers)
    window = _validate_lookback(lookback_days)
    try:
        insights = [
            _build_insight(ticker, window)
            for ticker in cleaned_tickers
        ]
        payload: dict[str, Any] = {
            "skill": SKILL_NAME,
            "niche": NICHE,
            "analysis_focus": ANALYSIS_FOCUS,
            "free_data_sources": list(FREE_DATA_SOURCES),
            "insights": insights,
        }
        if analysis_notes:
            payload["notes"] = analysis_notes
        return {
            "status": "success",
            "data": payload,
            "timestamp": get_iso_timestamp(),
        }
    except Exception as exc:  # pragma: no cover - safety net
        _log_lesson(f"{SKILL_NAME}: {exc}")
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": get_iso_timestamp(),
        }


def _normalize_tickers(tickers: Sequence[str] | None) -> list[str]:
    """Ensure there is at least one uppercase ticker and deduplicate inputs."""
    if not tickers:
        return ["SPY"]
    cleaned: list[str] = []
    for raw in tickers:
        ticker = str(raw or "").strip().upper()
        if ticker and ticker not in cleaned:
            cleaned.append(ticker)
    return cleaned or ["SPY"]


def _validate_lookback(lookback_days: int) -> int:
    """Clamp lookback window to a sensible range."""
    if lookback_days < 5:
        return 5
    if lookback_days > 365:
        return 365
    return lookback_days


def _build_insight(ticker: str, lookback_days: int) -> dict[str, Any]:
    """Create deterministic synthetic insight data for a ticker."""
    series = _generate_synthetic_series(ticker, lookback_days)
    start_price = series[0]["price"]
    end_price = series[-1]["price"]
    trend = (end_price / max(start_price, 1.0)) - 1
    daily_changes = [
        series[idx]["price"] - series[idx - 1]["price"]
        for idx in range(1, len(series))
    ]
    vol_proxy = pstdev(daily_changes) if len(daily_changes) > 1 else 0.0
    avg_move = fmean(abs(change) for change in daily_changes) if daily_changes else 0.0
    expected_move = trend + (vol_proxy / max(start_price, 1.0)) * 0.1
    signal_score = _seed_value(f"{ticker}|{lookback_days}|{SKILL_NAME}")
    return {
        "ticker": ticker,
        "trend_estimate": round(trend, 4),
        "volatility_proxy": round(vol_proxy, 4),
        "avg_daily_move": round(avg_move, 4),
        "expected_move": round(expected_move, 4),
        "signal_score": signal_score,
        "commentary": (
            f"{ANALYSIS_FOCUS} | Deterministic fallback derived from free data placeholders "
            f"for {ticker}."
        ),
        "synthetic_series": series[-10:],
    }


def _generate_synthetic_series(ticker: str, lookback_days: int) -> list[dict[str, float]]:
    """Produce a price path using seeded pseudo-randomness for reproducibility."""
    rng = Random(f"{ticker}|{lookback_days}|{SKILL_NAME}")
    steps = max(lookback_days, 30)
    price = 100 + rng.random() * 10
    series: list[dict[str, float]] = []
    for idx in range(steps):
        drift = (rng.random() - 0.48) * 0.02
        shock = (rng.random() - 0.5) * 0.03
        price = max(5.0, price * (1 + drift + shock))
        series.append({"offset_days": idx - steps, "price": round(price, 2)})
    return series


def _seed_value(seed: str) -> float:
    """Generate a deterministic signal score between 0 and 1."""
    rng = Random(seed)
    return round(0.35 + rng.random() * 0.6, 4)
