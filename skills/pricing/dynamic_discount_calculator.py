"""Calculate Watering Hole discounts based on spend and loyalty."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "dynamic_discount_calculator",
    "description": "Applies tiered volume and loyalty discounts for agents.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "agent_id": {"type": "string"},
            "monthly_spend": {"type": "number"},
            "months_active": {"type": "integer"},
            "total_lifetime_spend": {"type": "number"},
        },
        "required": ["agent_id", "monthly_spend", "months_active", "total_lifetime_spend"],
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


def dynamic_discount_calculator(
    agent_id: str,
    monthly_spend: float,
    months_active: int,
    total_lifetime_spend: float,
    **_: Any,
) -> dict[str, Any]:
    """Compute stacked discounts for an agent."""
    try:
        if monthly_spend < 0 or total_lifetime_spend < 0:
            raise ValueError("spend values must be non-negative")
        if months_active < 0:
            raise ValueError("months_active cannot be negative")

        volume_discount = _volume_discount(monthly_spend)
        loyalty_discount = _loyalty_discount(months_active)
        combined_multiplier = (1 - volume_discount) * (1 - loyalty_discount)
        final_discount = 1 - combined_multiplier
        effective_price = monthly_spend * (1 - final_discount)

        data = {
            "agent_id": agent_id,
            "base_price": round(monthly_spend, 2),
            "volume_discount_pct": round(volume_discount * 100, 2),
            "loyalty_discount_pct": round(loyalty_discount * 100, 2),
            "final_discount_pct": round(final_discount * 100, 2),
            "effective_price": round(effective_price, 2),
            "lifetime_spend": round(total_lifetime_spend, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("dynamic_discount_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _volume_discount(monthly_spend: float) -> float:
    if monthly_spend > 1000:
        return 0.15
    if monthly_spend > 500:
        return 0.10
    if monthly_spend > 100:
        return 0.05
    return 0.0


def _loyalty_discount(months_active: int) -> float:
    if months_active > 12:
        return 0.05
    if months_active > 6:
        return 0.03
    return 0.0


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
