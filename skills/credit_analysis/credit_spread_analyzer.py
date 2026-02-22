"""Analyze credit spreads and implied defaults."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "credit_spread_analyzer",
    "description": "Calculates credit spreads, implied default probabilities, and indicative ratings.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "corporate_yield": {"type": "number"},
            "risk_free_yield": {"type": "number"},
            "recovery_rate": {"type": "number", "default": 0.4},
            "maturity_years": {"type": "integer"},
            "leverage_turns": {"type": "number"},
        },
        "required": ["corporate_yield", "risk_free_yield", "maturity_years"],
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


def credit_spread_analyzer(
    corporate_yield: float,
    risk_free_yield: float,
    recovery_rate: float = 0.4,
    maturity_years: int = 5,
    leverage_turns: float | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Return spread metrics and implied default probabilities."""
    try:
        spread = corporate_yield - risk_free_yield
        annual_pd = spread / max(1 - recovery_rate, 0.01)
        cumulative_pd = 1 - (1 - annual_pd) ** maturity_years
        spread_per_turn = spread / leverage_turns if leverage_turns else None
        rating_estimate = "BBB" if spread < 0.02 else "BB" if spread < 0.04 else "B"
        data = {
            "credit_spread_bps": round(spread * 10000, 1),
            "annual_default_prob": round(annual_pd, 4),
            "cumulative_default_prob": round(cumulative_pd, 4),
            "spread_per_turn_leverage": round(spread_per_turn, 4) if spread_per_turn else None,
            "rating_estimate": rating_estimate,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("credit_spread_analyzer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
