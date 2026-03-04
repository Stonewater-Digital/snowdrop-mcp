"""Analyze cap rates and implied property values."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "cap_rate_analyzer",
    "description": "Computes actual cap rate and implied value relative to market cap rates.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "net_operating_income": {"type": "number"},
            "asset_value": {"type": "number"},
            "market_cap_rate_pct": {"type": "number"},
        },
        "required": ["net_operating_income", "asset_value", "market_cap_rate_pct"],
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


def cap_rate_analyzer(
    net_operating_income: float,
    asset_value: float,
    market_cap_rate_pct: float,
    **_: Any,
) -> dict[str, Any]:
    """Return cap rate and implied valuation metrics."""
    try:
        actual_cap_rate = net_operating_income / asset_value * 100 if asset_value else 0.0
        implied_value = net_operating_income / (market_cap_rate_pct / 100) if market_cap_rate_pct else 0.0
        premium_pct = (implied_value - asset_value) / asset_value * 100 if asset_value else 0.0
        data = {
            "actual_cap_rate_pct": round(actual_cap_rate, 2),
            "implied_value": round(implied_value, 2),
            "value_premium_pct": round(premium_pct, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("cap_rate_analyzer", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
