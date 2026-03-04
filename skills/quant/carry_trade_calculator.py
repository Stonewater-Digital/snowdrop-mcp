"""Evaluate FX carry attractiveness."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable

TOOL_META: dict[str, Any] = {
    "name": "carry_trade_calculator",
    "description": "Computes carry-to-vol metrics for FX pairs using interest differentials.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "pairs": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "domestic_rate_pct": {"type": "number"},
                        "foreign_rate_pct": {"type": "number"},
                        "spot_rate": {"type": "number"},
                        "forward_rate": {"type": "number"},
                        "volatility_pct": {"type": "number", "default": 10.0},
                    },
                    "required": ["name", "domestic_rate_pct", "foreign_rate_pct", "spot_rate", "forward_rate"],
                },
            }
        },
        "required": ["pairs"],
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


def carry_trade_calculator(pairs: Iterable[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return carry metrics for FX pairs."""
    try:
        pair_list = list(pairs)
        if not pair_list:
            raise ValueError("pairs cannot be empty")
        metrics = []
        for pair in pair_list:
            domestic = float(pair["domestic_rate_pct"])
            foreign = float(pair["foreign_rate_pct"])
            spot = float(pair["spot_rate"])
            forward = float(pair["forward_rate"])
            vol = float(pair.get("volatility_pct", 10.0))
            interest_diff = domestic - foreign
            implied_forward = spot * (1 + domestic / 100) / (1 + foreign / 100)
            basis = (forward - implied_forward) / spot * 100
            carry_to_vol = interest_diff / vol if vol else 0.0
            metrics.append(
                {
                    "name": pair["name"],
                    "interest_diff_pct": round(interest_diff, 2),
                    "forward_basis_pct": round(basis, 2),
                    "carry_to_vol": round(carry_to_vol, 3),
                }
            )
        data = {"pair_metrics": metrics}
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        _log_lesson(f"carry_trade_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
