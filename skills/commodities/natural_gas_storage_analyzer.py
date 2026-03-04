"""Evaluate natural gas storage vs seasonal norms."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "natural_gas_storage_analyzer",
    "description": (
        "Compares EIA-style natural gas storage levels to 5-year seasonal averages, "
        "flags injection/withdrawal pace, and provides bullish/bearish market implication."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "storage_bcf": {
                "type": "number",
                "description": "Current storage level in billion cubic feet (must be >= 0).",
            },
            "five_year_avg_bcf": {
                "type": "number",
                "description": "5-year seasonal average storage level in Bcf (must be > 0).",
            },
            "five_year_max_bcf": {
                "type": ["number", "null"],
                "default": None,
                "description": "5-year maximum storage at this date (optional, for range context).",
            },
            "five_year_min_bcf": {
                "type": ["number", "null"],
                "default": None,
                "description": "5-year minimum storage at this date (optional, for range context).",
            },
            "daily_flow_bcf": {
                "type": "number",
                "default": 0.0,
                "description": "Net daily injection (+) or withdrawal (−) in Bcf/day.",
            },
            "season_phase": {
                "type": "string",
                "default": "injection",
                "enum": ["injection", "withdrawal"],
                "description": "Current seasonal phase: 'injection' (Apr–Oct) or 'withdrawal' (Nov–Mar).",
            },
        },
        "required": ["storage_bcf", "five_year_avg_bcf"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "storage_surplus_bcf": {"type": "number"},
            "surplus_pct_vs_norm": {"type": "number"},
            "days_of_cover_at_flow": {"type": ["number", "null"]},
            "within_five_year_range": {"type": ["boolean", "null"]},
            "market_implication": {"type": "string"},
            "timestamp": {"type": "string"},
        },
    },
}


def natural_gas_storage_analyzer(
    storage_bcf: float,
    five_year_avg_bcf: float,
    five_year_max_bcf: float | None = None,
    five_year_min_bcf: float | None = None,
    daily_flow_bcf: float = 0.0,
    season_phase: str = "injection",
    **_: Any,
) -> dict[str, Any]:
    """Return surplus, coverage, and market implication for gas storage.

    Args:
        storage_bcf: Current storage level in Bcf.
        five_year_avg_bcf: 5-year average for this week/date in Bcf (must be > 0).
        five_year_max_bcf: 5-year max for this week (optional).
        five_year_min_bcf: 5-year min for this week (optional).
        daily_flow_bcf: Net daily flow in Bcf/day (positive = injecting).
        season_phase: 'injection' or 'withdrawal'.

    Returns:
        dict with status, surplus/deficit vs 5-year average, surplus as % of average,
        days of cover at current flow rate, range check, and market implication.

    Market implication logic:
        Injection season:
            storage > 5yr avg  =>  bearish (well-supplied)
            storage < 5yr avg  =>  bullish (supply tightness)
        Withdrawal season:
            storage > 5yr avg  =>  bearish (ample stocks, less price support)
            storage < 5yr avg  =>  bullish (draw-down risk)
        Equal to avg  =>  neutral
    """
    try:
        if storage_bcf < 0:
            raise ValueError("storage_bcf must be >= 0")
        if five_year_avg_bcf <= 0:
            raise ValueError("five_year_avg_bcf must be positive")
        phase = season_phase.lower()
        if phase not in ("injection", "withdrawal"):
            raise ValueError("season_phase must be 'injection' or 'withdrawal'")

        deviation = storage_bcf - five_year_avg_bcf
        surplus_pct = (deviation / five_year_avg_bcf) * 100.0

        # Days of cover: how many days until storage reaches zero at current draw rate
        days_of_cover: float | None = None
        if abs(daily_flow_bcf) > 1e-9:
            if phase == "withdrawal" and daily_flow_bcf < 0:
                days_of_cover = storage_bcf / abs(daily_flow_bcf)
            elif phase == "injection" and daily_flow_bcf > 0:
                # Meaningful in injection context as time-to-capacity or pace indicator
                days_of_cover = storage_bcf / abs(daily_flow_bcf)

        # Within 5-year range check
        within_range: bool | None = None
        if five_year_max_bcf is not None and five_year_min_bcf is not None:
            within_range = five_year_min_bcf <= storage_bcf <= five_year_max_bcf

        # Market implication
        if deviation > 0:
            bias = "bearish"  # above average = bearish regardless of season
        elif deviation < 0:
            bias = "bullish"  # below average = bullish regardless of season
        else:
            bias = "neutral"

        return {
            "status": "success",
            "storage_surplus_bcf": round(deviation, 2),
            "surplus_pct_vs_norm": round(surplus_pct, 2),
            "days_of_cover_at_flow": round(days_of_cover, 1) if days_of_cover is not None else None,
            "within_five_year_range": within_range,
            "market_implication": bias,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("natural_gas_storage_analyzer", str(exc))
        return {
            "status": "error",
            "error": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
