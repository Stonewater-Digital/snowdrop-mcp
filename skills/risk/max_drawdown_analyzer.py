"""Maximum drawdown analytics for Snowdrop portfolios."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "max_drawdown_analyzer",
    "description": "Computes maximum drawdown statistics from an equity curve.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "equity_curve": {
                "type": "array",
                "items": {"type": "number"},
            }
        },
        "required": ["equity_curve"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "max_drawdown_pct": {"type": "number"},
                    "peak_date_index": {"type": "integer"},
                    "trough_date_index": {"type": "integer"},
                    "recovery_date_index": {"type": ["integer", "null"]},
                    "current_drawdown_pct": {"type": "number"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def max_drawdown_analyzer(equity_curve: list[float], **_: Any) -> dict[str, Any]:
    """Return drawdown depth, timing, and recovery diagnostics."""

    try:
        if len(equity_curve) < 2:
            raise ValueError("equity_curve requires at least two observations")

        peak_value = equity_curve[0]
        peak_index = 0
        max_drawdown = 0.0
        max_peak_index = 0
        max_trough_index = 0
        recovery_index: int | None = None
        reference_peak_value = peak_value

        for idx, value in enumerate(equity_curve):
            if value > peak_value:
                peak_value = value
                peak_index = idx
            drawdown = (value - peak_value) / peak_value
            if drawdown < max_drawdown:
                max_drawdown = drawdown
                max_peak_index = peak_index
                max_trough_index = idx
                reference_peak_value = peak_value
                recovery_index = None
            elif (
                recovery_index is None
                and idx > max_trough_index
                and reference_peak_value > 0
                and value >= reference_peak_value
            ):
                recovery_index = idx

        if peak_value <= 0:
            raise ValueError("Equity values must be positive")
        current_drawdown = (equity_curve[-1] - peak_value) / peak_value

        data = {
            "max_drawdown_pct": round(-max_drawdown * 100, 4),
            "peak_date_index": max_peak_index,
            "trough_date_index": max_trough_index,
            "recovery_date_index": recovery_index,
            "current_drawdown_pct": round(-current_drawdown * 100, 4),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("max_drawdown_analyzer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    """Append a Ralph Wiggum lesson entry."""

    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
