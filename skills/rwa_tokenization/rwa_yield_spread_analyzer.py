"""Compare RWA token yields versus benchmarks.
Outputs spread, breakeven, and convexity-adjusted metrics."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "rwa_yield_spread_analyzer",
    "description": "Computes yield spreads relative to benchmark bonds and adjusts for duration risk.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "token_yield_pct": {"type": "number", "description": "Yield of the RWA token"},
            "benchmark_yield_pct": {"type": "number", "description": "Comparable benchmark yield"},
            "duration_years": {"type": "number", "description": "Effective duration"},
        },
        "required": ["token_yield_pct", "benchmark_yield_pct", "duration_years"],
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


def rwa_yield_spread_analyzer(
    token_yield_pct: float,
    benchmark_yield_pct: float,
    duration_years: float,
    **_: Any,
) -> dict[str, Any]:
    """Calculate RWA yield spreads.

    Args:
        token_yield_pct: Observed token yield.
        benchmark_yield_pct: Comparable treasury or credit benchmark.
        duration_years: Interest rate duration of the token cash flows.

    Returns:
        Dict summarizing spreads and DV01 sensitivity.
    """
    try:
        spread_bps = (token_yield_pct - benchmark_yield_pct) * 100
        dv01 = duration_years * 0.0001  # price change per bp per $1
        breakeven_move_pct = spread_bps / (duration_years * 100) if duration_years else 0.0
        data = {
            "spread_bps": round(spread_bps, 1),
            "relative_value_flag": spread_bps > 0,
            "duration_dv01": round(dv01, 6),
            "breakeven_rate_move_pct": round(breakeven_move_pct, 4),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("rwa_yield_spread_analyzer failure: %s", exc)
        log_lesson(f"rwa_yield_spread_analyzer: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
