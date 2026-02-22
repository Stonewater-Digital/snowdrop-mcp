"""Calculate Kelly Criterion position sizing."""
from __future__ import annotations

from math import log
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "kelly_criterion_calculator",
    "description": "Computes Kelly fraction, position size, and expected growth rates.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "win_probability": {"type": "number"},
            "win_amount": {"type": "number"},
            "loss_amount": {"type": "number"},
            "current_bankroll": {"type": "number"},
            "kelly_fraction": {"type": "number", "default": 0.5},
        },
        "required": ["win_probability", "win_amount", "loss_amount", "current_bankroll"],
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


def kelly_criterion_calculator(
    win_probability: float,
    win_amount: float,
    loss_amount: float,
    current_bankroll: float,
    kelly_fraction: float = 0.5,
    **_: Any,
) -> dict[str, Any]:
    """Return Kelly sizing guidance."""
    try:
        p = win_probability
        q = 1 - p
        b = win_amount / loss_amount if loss_amount else 0.0
        full_kelly = max((b * p - q) / b if b else 0.0, 0.0)
        fractional = full_kelly * kelly_fraction
        position_size = current_bankroll * fractional
        expected_growth = p * log(1 + full_kelly * b) + q * log(1 - full_kelly) if full_kelly and b else 0.0
        data = {
            "full_kelly_pct": round(full_kelly * 100, 2),
            "fractional_kelly_pct": round(fractional * 100, 2),
            "position_size": round(position_size, 2),
            "expected_growth_rate": round(expected_growth, 4),
            "risk_of_ruin_pct": round(max(q - p, 0) * 100, 2),
            "edge": round(b * p - q, 4),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("kelly_criterion_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
