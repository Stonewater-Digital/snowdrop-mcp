"""Estimate liquidity premium from bid-ask spreads and turnover."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable

TOOL_META: dict[str, Any] = {
    "name": "liquidity_premium_calculator",
    "description": "Approximates annual liquidity drag from bid-ask spreads and funding costs.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "assets": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "bid_ask_bps": {"type": "number"},
                        "turnover_per_year": {"type": "number", "default": 4},
                        "financing_cost_bps": {"type": "number", "default": 0},
                    },
                    "required": ["name", "bid_ask_bps"],
                },
            }
        },
        "required": ["assets"],
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


def liquidity_premium_calculator(assets: Iterable[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return estimated annual liquidity premium per asset."""
    try:
        asset_list = list(assets)
        if not asset_list:
            raise ValueError("assets cannot be empty")
        premiums = []
        for asset in asset_list:
            spread_cost = float(asset["bid_ask_bps"]) / 2
            turnover = float(asset.get("turnover_per_year", 4))
            financing = float(asset.get("financing_cost_bps", 0))
            premium = (spread_cost * turnover + financing) / 100
            premiums.append(
                {
                    "name": asset["name"],
                    "turnover_per_year": turnover,
                    "liquidity_premium_pct": round(premium, 3),
                }
            )
        avg_premium = sum(item["liquidity_premium_pct"] for item in premiums) / len(premiums)
        data = {"asset_liquidity_premia": premiums, "average_liquidity_premium_pct": round(avg_premium, 3)}
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        _log_lesson(f"liquidity_premium_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
