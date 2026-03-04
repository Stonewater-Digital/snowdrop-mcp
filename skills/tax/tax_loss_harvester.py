"""Identify tax-loss harvesting opportunities."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "tax_loss_harvester",
    "description": "Ranks positions by after-tax savings potential with wash sale warnings.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "positions": {"type": "array", "items": {"type": "object"}},
            "short_term_rate": {"type": "number", "default": 0.37},
            "long_term_rate": {"type": "number", "default": 0.20},
        },
        "required": ["positions"],
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


def tax_loss_harvester(
    positions: list[dict[str, Any]],
    short_term_rate: float = 0.37,
    long_term_rate: float = 0.20,
    **_: Any,
) -> dict[str, Any]:
    """Return ranked harvest ideas with risk annotations."""
    try:
        if not positions:
            raise ValueError("positions cannot be empty")

        harvestable: list[dict[str, Any]] = []
        for position in positions:
            asset = position.get("asset")
            cost_basis = float(position.get("cost_basis", 0.0))
            current_value = float(position.get("current_value", 0.0))
            holding_days = int(position.get("holding_period_days", 0))
            if current_value >= cost_basis:
                continue

            loss = cost_basis - current_value
            applicable_rate = short_term_rate if holding_days < 365 else long_term_rate
            tax_savings = loss * applicable_rate
            warning = holding_days < 31
            harvestable.append(
                {
                    "asset": asset,
                    "loss_amount": round(loss, 2),
                    "tax_savings_potential": round(tax_savings, 2),
                    "holding_period_days": holding_days,
                    "wash_sale_warning": warning,
                    "recommended_replacement": _replacement_hint(asset),
                }
            )

        harvestable.sort(key=lambda entry: entry["tax_savings_potential"], reverse=True)
        data = {"opportunities": harvestable}
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("tax_loss_harvester", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _replacement_hint(asset: str | None) -> str:
    if not asset:
        return "rotate into diversified ETF or cash for 31 days"
    if asset.upper().startswith("BTC"):
        return "Consider ETH or broad crypto beta ETN"
    if asset.upper().startswith("ETH"):
        return "Rotate into L2 basket ETF"
    return "Use sector ETF or factor proxy for 31 days"


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
