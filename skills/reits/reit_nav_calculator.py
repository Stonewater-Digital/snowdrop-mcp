"""Compute REIT NAV per share."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "reit_nav_calculator",
    "description": "Values properties via NOI/cap rates to derive NAV per share.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "properties": {"type": "array", "items": {"type": "object"}},
            "other_assets": {"type": "number"},
            "total_debt": {"type": "number"},
            "preferred_equity": {"type": "number"},
            "cash": {"type": "number"},
            "shares_outstanding": {"type": "number"},
            "share_price": {"type": "number"},
        },
        "required": ["properties", "other_assets", "total_debt", "preferred_equity", "cash", "shares_outstanding"],
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def reit_nav_calculator(
    properties: list[dict[str, Any]],
    other_assets: float,
    total_debt: float,
    preferred_equity: float,
    cash: float,
    shares_outstanding: float,
    share_price: float | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Return NAV and premium/discount."""
    try:
        property_values = []
        gross_asset_value = other_assets + cash
        for prop in properties:
            noi = prop.get("noi", 0.0)
            cap_rate = prop.get("cap_rate", 0.05)
            value = noi / cap_rate if cap_rate else 0.0
            debt = prop.get("debt_on_property", 0.0)
            property_values.append({"name": prop.get("name"), "value": round(value, 2)})
            gross_asset_value += value - debt
        nav = gross_asset_value - total_debt - preferred_equity
        nav_per_share = nav / shares_outstanding if shares_outstanding else 0.0
        premium = None
        if share_price is not None:
            premium = (share_price / nav_per_share - 1) * 100 if nav_per_share else None
        data = {
            "gross_asset_value": round(gross_asset_value, 2),
            "nav": round(nav, 2),
            "nav_per_share": round(nav_per_share, 2),
            "premium_discount_to_share_price": round(premium, 2) if premium is not None else None,
            "implied_cap_rate": round(sum(prop.get("noi", 0.0) for prop in properties) / gross_asset_value, 4) if gross_asset_value else 0.0,
            "property_values": property_values,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("reit_nav_calculator", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
