"""Classify market regime using rolling volatility and trend filters."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Sequence

TOOL_META: dict[str, Any] = {
    "name": "regime_detector",
    "description": "Detects bull vs bear regimes using realized volatility and return trends.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "return_series": {"type": "array", "items": {"type": "number"}},
            "vol_window": {"type": "integer", "default": 30},
            "vol_threshold_pct": {"type": "number", "default": 20.0},
        },
        "required": ["return_series"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
    },
}


def regime_detector(
    return_series: Sequence[float],
    vol_window: int = 30,
    vol_threshold_pct: float = 20.0,
    **_: Any,
) -> dict[str, Any]:
    """Return regime classification based on volatility and drawdown."""
    try:
        if len(return_series) < vol_window:
            raise ValueError("return_series shorter than vol_window")
        tail = [float(r) for r in return_series[-vol_window:]]
        avg_return = sum(tail) / vol_window
        variance = sum((r - avg_return) ** 2 for r in tail) / max(vol_window - 1, 1)
        realized_vol = (variance**0.5) * (252**0.5) * 100
        cumulative = 1.0
        peak = 1.0
        max_drawdown = 0.0
        for r in (1 + x for x in return_series[-vol_window:]):
            cumulative *= r
            peak = max(peak, cumulative)
            max_drawdown = min(max_drawdown, (cumulative / peak) - 1)
        state = "risk_off" if realized_vol > vol_threshold_pct or max_drawdown < -0.1 else "risk_on"
        data = {
            "realized_vol_pct": round(realized_vol, 2),
            "average_return_pct": round(avg_return * 100, 2),
            "max_drawdown_pct": round(max_drawdown * 100, 2),
            "regime": state,
            "vol_threshold_pct": vol_threshold_pct,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        _log_lesson(f"regime_detector: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
