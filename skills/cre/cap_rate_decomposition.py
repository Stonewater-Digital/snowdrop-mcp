"""Decompose cap rates into risk components."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

PROPERTY_PREMIUM = {"office": 0.02, "retail": 0.025, "industrial": 0.015, "multifamily": 0.01, "hotel": 0.035}
MARKET_PREMIUM = {"gateway": 0.005, "secondary": 0.015, "tertiary": 0.025}
BUILDING_PREMIUM = {"A": 0.0, "B": 0.01, "C": 0.02}

TOOL_META: dict[str, Any] = {
    "name": "cap_rate_decomposition",
    "description": "Breaks down cap rate into risk-free, property, market, and vacancy components.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "cap_rate": {"type": "number"},
            "risk_free_rate": {"type": "number"},
            "property_type": {"type": "string"},
            "market_tier": {"type": "string"},
            "building_class": {"type": "string"},
            "occupancy_pct": {"type": "number"},
        },
        "required": ["cap_rate", "risk_free_rate", "property_type", "market_tier", "building_class", "occupancy_pct"],
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def cap_rate_decomposition(
    cap_rate: float,
    risk_free_rate: float,
    property_type: str,
    market_tier: str,
    building_class: str,
    occupancy_pct: float,
    **_: Any,
) -> dict[str, Any]:
    """Return decomposition and relative value signal."""
    try:
        property_premium = PROPERTY_PREMIUM.get(property_type, 0.02)
        market_premium = MARKET_PREMIUM.get(market_tier, 0.02)
        building_premium = BUILDING_PREMIUM.get(building_class, 0.01)
        vacancy_premium = max(0.0, (1 - occupancy_pct / 100) * 0.03)
        implied_growth = cap_rate - (risk_free_rate + property_premium + market_premium + building_premium + vacancy_premium)
        decomposition = {
            "risk_free": risk_free_rate,
            "property_premium": property_premium,
            "market_premium": market_premium,
            "building_premium": building_premium,
            "vacancy_premium": vacancy_premium,
            "residual_growth": implied_growth,
        }
        spread = cap_rate - risk_free_rate
        relative_value = "attractive" if spread > 0.03 else "fair"
        signal = "compression" if implied_growth > 0 else "expansion"
        data = {
            "decomposition": {k: round(v, 4) for k, v in decomposition.items()},
            "implied_growth_rate": round(implied_growth, 4),
            "spread_over_treasuries": round(spread, 4),
            "relative_value": relative_value,
            "historical_avg_spread": 0.03,
            "compression_expansion_signal": signal,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("cap_rate_decomposition", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
