"""Analyze secondary offering dilution and TERP."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "secondary_offering_dilution",
    "description": "Evaluates dilution, proceeds, and TERP for primary/secondary offerings.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "current_shares": {"type": "integer"},
            "current_price": {"type": "number"},
            "new_shares": {"type": "integer"},
            "offering_price": {"type": "number"},
            "is_primary": {"type": "boolean"},
            "is_secondary": {"type": "boolean"},
            "underwriter_discount_pct": {"type": "number", "default": 5.0},
        },
        "required": ["current_shares", "current_price", "new_shares", "offering_price", "is_primary", "is_secondary"],
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


def secondary_offering_dilution(
    current_shares: int,
    current_price: float,
    new_shares: int,
    offering_price: float,
    is_primary: bool,
    is_secondary: bool,
    underwriter_discount_pct: float = 5.0,
    **_: Any,
) -> dict[str, Any]:
    """Return dilution metrics."""
    try:
        pre_cap = current_shares * current_price
        post_shares = current_shares + (new_shares if is_primary else 0)
        net_proceeds = new_shares * offering_price * (1 - underwriter_discount_pct / 100) if is_primary else 0.0
        terp = (pre_cap + new_shares * offering_price) / (current_shares + new_shares) if (current_shares + new_shares) else current_price
        dilution_pct = (post_shares - current_shares) / current_shares * 100 if is_primary else 0.0
        eps_dilution = dilution_pct / 100
        overhang = new_shares / current_shares * 100 if is_secondary else 0.0
        data = {
            "pre_offering_market_cap": round(pre_cap, 2),
            "post_offering_shares": post_shares,
            "terp": round(terp, 2),
            "dilution_pct": round(dilution_pct, 2),
            "net_proceeds": round(net_proceeds, 2),
            "eps_dilution_pct": round(eps_dilution * 100, 2),
            "overhang_pct": round(overhang, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("secondary_offering_dilution", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
