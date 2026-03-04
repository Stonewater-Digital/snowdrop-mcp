"""Rank collateral options by funding efficiency."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "collateral_management_optimizer",
    "description": "Ranks collateral by haircut-adjusted funding cost versus yield.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "collateral_pool": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "asset": {"type": "string"},
                        "market_value": {"type": "number"},
                        "haircut_pct": {"type": "number"},
                        "yield_pct": {"type": "number"},
                    },
                    "required": ["asset", "market_value", "haircut_pct", "yield_pct"],
                },
            },
            "funding_rate_pct": {"type": "number", "default": 5.0},
        },
        "required": ["collateral_pool"],
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def collateral_management_optimizer(
    collateral_pool: list[dict[str, Any]],
    funding_rate_pct: float = 5.0,
    **_: Any,
) -> dict[str, Any]:
    """Return ranking of collateral assets."""
    try:
        ranking = []
        for asset in collateral_pool:
            haircut = asset.get("haircut_pct", 0.0) / 100
            effective_value = asset.get("market_value", 0.0) * (1 - haircut)
            opportunity_cost = effective_value * (funding_rate_pct / 100)
            yield_income = asset.get("market_value", 0.0) * (asset.get("yield_pct", 0.0) / 100)
            net_cost = opportunity_cost - yield_income
            ranking.append(
                {
                    "asset": asset.get("asset"),
                    "effective_value": round(effective_value, 2),
                    "net_cost": round(net_cost, 2),
                }
            )
        ranking.sort(key=lambda item: item["net_cost"])
        data = {"ranking": ranking}
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("collateral_management_optimizer", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
