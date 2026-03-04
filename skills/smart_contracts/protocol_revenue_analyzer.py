"""Aggregate fee streams to estimate protocol revenue run-rates.
Supports multiple product segments and flags dependency risk."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Sequence
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "protocol_revenue_analyzer",
    "description": "Calculates revenue per product and annualizes it to monitor concentration risk.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "fee_streams": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "volume_usd": {"type": "number"},
                        "fee_bps": {"type": "number"},
                    },
                    "required": ["name", "volume_usd", "fee_bps"],
                },
                "description": "Per-product fee streams.",
            },
            "annualization_factor": {
                "type": "number",
                "description": "Multiplier to annualize the provided period",
                "default": 52,
            },
        },
        "required": ["fee_streams"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"},
            "error": {"type": "string"},
        },
    },
}


def protocol_revenue_analyzer(
    fee_streams: Sequence[dict[str, Any]],
    annualization_factor: float = 52.0,
    **_: Any,
) -> dict[str, Any]:
    """Compute per-product revenue splits and totals.

    Args:
        fee_streams: List of volume and fee inputs per product.
        annualization_factor: Multiplier to annualize the reporting period.

    Returns:
        Dict with per-segment revenue, totals, and concentration metrics.
    """
    try:
        if annualization_factor <= 0:
            raise ValueError("annualization_factor must be positive")
        per_stream = []
        total_revenue = 0.0
        for stream in fee_streams:
            name = stream.get("name", "segment")
            volume = float(stream.get("volume_usd", 0))
            fee_bps = float(stream.get("fee_bps", 0))
            revenue = volume * fee_bps / 10_000
            annual_revenue = revenue * annualization_factor
            per_stream.append({"name": name, "period_revenue": round(revenue, 2), "annualized_revenue": round(annual_revenue, 2)})
            total_revenue += annual_revenue
        concentration = 0.0
        if total_revenue > 0:
            concentration = max((entry["annualized_revenue"] for entry in per_stream), default=0) / total_revenue * 100
        data = {
            "streams": per_stream,
            "annualized_revenue_total": round(total_revenue, 2),
            "largest_stream_pct": round(concentration, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("protocol_revenue_analyzer failure: %s", exc)
        log_lesson(f"protocol_revenue_analyzer: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
