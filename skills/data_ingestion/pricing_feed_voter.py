"""
Executive Summary: Aggregates vendor quotes, applies voting logic, and surfaces consensus pricing plus outliers for NAV sign-off.

Inputs: quotes (list[dict]), method (str, optional), spread_threshold_bps (float, optional), min_sources (int, optional)
Outputs: status (str), data (consensus_price/spread/flagged), timestamp (str)
MCP Tool Name: pricing_feed_voter
"""
from __future__ import annotations

from statistics import median, fmean
from typing import Any

from skills.utils import (
    SkillTelemetryEmitter,
    get_iso_timestamp,
    logger,
    log_lesson as _shared_log_lesson,
)

TOOL_META: dict[str, Any] = {
    "name": "pricing_feed_voter",
    "description": "Computes a consensus price across vendor feeds and flags quotes outside tolerance bands.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "quotes": {
                "type": "array",
                "items": {"type": "object"},
                "description": "List of quotes containing source, price, and timestamp.",
            },
            "method": {
                "type": "string",
                "enum": ["median", "trimmed_mean"],
                "default": "median",
                "description": "Voting method for consensus price calculation.",
            },
            "spread_threshold_bps": {
                "type": "number",
                "default": 25.0,
                "description": "Absolute deviation threshold (in bps) before a quote is flagged.",
            },
            "min_sources": {
                "type": "integer",
                "default": 2,
                "description": "Minimum number of valid quotes required to emit a price.",
            },
        },
        "required": ["quotes"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["ok", "error"]},
            "data": {
                "type": "object",
                "properties": {
                    "consensus_price": {"type": ["number", "null"]},
                    "method": {"type": "string"},
                    "spread_bps": {"type": "number"},
                    "sources_used": {"type": "array", "items": {"type": "string"}},
                    "flagged_sources": {"type": "array", "items": {"type": "string"}},
                    "quote_count": {"type": "integer"},
                },
            },
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def pricing_feed_voter(
    quotes: list[dict[str, Any]],
    method: str = "median",
    spread_threshold_bps: float = 25.0,
    min_sources: int = 2,
) -> dict[str, Any]:
    """Calculate a consensus price and identify outliers.

    Args:
        quotes: Vendor quote payloads containing `source` and `price`.
        method: Voting method (`median` or `trimmed_mean`).
        spread_threshold_bps: Deviation band to label outliers.
        min_sources: Minimum quotes required for consensus.

    Returns:
        Snowdrop response dict with consensus price data and flags.

    Raises:
        ValueError: If insufficient quotes or unsupported method is supplied.
    """
    emitter = SkillTelemetryEmitter(
        "pricing_feed_voter",
        {
            "quote_count": len(quotes or []),
            "method": method,
            "spread_threshold_bps": spread_threshold_bps,
        },
    )
    try:
        valid_quotes = [q for q in quotes if isinstance(q, dict) and _is_number(q.get("price"))]
        if len(valid_quotes) < min_sources:
            raise ValueError(f"Need at least {min_sources} valid quotes to vote")

        consensus = _compute_consensus(valid_quotes, method)
        if consensus is None:
            raise ValueError("Consensus calculation failed (method mismatch)")

        spread_bps = _compute_spread(valid_quotes, consensus)
        flagged_sources = _flag_outliers(valid_quotes, consensus, spread_threshold_bps)

        data = {
            "consensus_price": consensus,
            "method": method,
            "spread_bps": spread_bps,
            "sources_used": [str(q.get("source")) for q in valid_quotes],
            "flagged_sources": sorted(flagged_sources),
            "quote_count": len(valid_quotes),
        }
        emitter.record(
            "ok",
            {
                "quote_count": len(valid_quotes),
                "flagged_sources": len(flagged_sources),
                "spread_bps": round(spread_bps, 2),
            },
        )
        return {"status": "ok", "data": data, "timestamp": get_iso_timestamp()}
    except Exception as exc:
        msg = f"pricing_feed_voter failed: {exc}"
        logger.error(msg)
        _log_lesson("pricing_feed_voter", str(exc))
        emitter.record("error", {"error": str(exc)})
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": get_iso_timestamp(),
        }


def _compute_consensus(quotes: list[dict[str, Any]], method: str) -> float | None:
    """Return consensus price given a voting method."""
    prices = [float(q["price"]) for q in quotes]
    if method == "median":
        return float(median(prices))
    if method == "trimmed_mean":
        if len(prices) <= 2:
            return float(fmean(prices))
        trimmed = sorted(prices)[1:-1]
        return float(fmean(trimmed))
    return None


def _compute_spread(quotes: list[dict[str, Any]], consensus: float) -> float:
    """Compute spread in basis points between high and low quotes."""
    prices = [float(q["price"]) for q in quotes]
    if not prices or consensus == 0:
        return 0.0
    return ((max(prices) - min(prices)) / consensus) * 10_000


def _flag_outliers(
    quotes: list[dict[str, Any]],
    consensus: float,
    threshold_bps: float,
) -> set[str]:
    """Return sources whose quotes deviate beyond the threshold."""
    flagged: set[str] = set()
    for quote in quotes:
        price = float(quote["price"])
        deviation_bps = abs(price - consensus) / consensus * 10_000 if consensus else 0.0
        if deviation_bps > threshold_bps:
            flagged.add(str(quote.get("source")))
    return flagged


def _is_number(value: Any) -> bool:
    """Check whether a value can be cast to float."""
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def _log_lesson(skill_name: str, error: str) -> None:
    """Proxy to shared lesson logger for consistent formatting."""
    _shared_log_lesson(skill_name, error)
