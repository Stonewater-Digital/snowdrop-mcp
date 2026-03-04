"""Estimate portfolio margin requirements."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "margin_requirement_calculator",
    "description": "Computes SPAN-style margin based on risk weights and add-ons.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "positions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "product": {"type": "string"},
                        "notional": {"type": "number"},
                        "risk_weight_pct": {"type": "number"},
                        "liquidity_add_on_pct": {"type": "number", "default": 0.0},
                    },
                    "required": ["product", "notional", "risk_weight_pct"],
                },
            },
            "house_margin_pct": {"type": "number", "default": 0.0},
        },
        "required": ["positions"],
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def margin_requirement_calculator(
    positions: list[dict[str, Any]],
    house_margin_pct: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Return margin requirement by product."""
    try:
        requirements = []
        total_margin = 0.0
        for position in positions:
            base = position.get("notional", 0.0) * (position.get("risk_weight_pct", 0.0) / 100)
            add_on = position.get("notional", 0.0) * (position.get("liquidity_add_on_pct", 0.0) / 100)
            margin = base + add_on
            total_margin += margin
            requirements.append({"product": position.get("product"), "margin": round(margin, 2)})
        total_margin *= 1 + house_margin_pct / 100
        data = {
            "requirements": requirements,
            "total_margin": round(total_margin, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("margin_requirement_calculator", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
