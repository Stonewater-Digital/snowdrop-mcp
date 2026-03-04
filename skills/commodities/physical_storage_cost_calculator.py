"""Calculate physical commodity storage cost stack."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "physical_storage_cost_calculator",
    "description": (
        "Quantifies the full carry cost of holding physical commodity inventory: "
        "warehouse/storage fees, insurance, and financing cost over a given horizon. "
        "Returns total cost, per-unit cost, and implied break-even basis appreciation."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "inventory_units": {
                "type": "number",
                "description": "Number of units in inventory (must be > 0).",
            },
            "unit_value": {
                "type": "number",
                "description": "Current market value per unit (must be > 0).",
            },
            "storage_fee_per_unit_month": {
                "type": "number",
                "description": "Flat storage fee per unit per month in currency terms.",
            },
            "insurance_pct_annual": {
                "type": "number",
                "default": 0.5,
                "description": "Annual insurance cost as % of inventory value. Defaults to 0.5%.",
            },
            "financing_rate_pct_annual": {
                "type": "number",
                "default": 6.0,
                "description": "Annual financing (opportunity) cost as % of inventory value. Defaults to 6%.",
            },
            "months": {
                "type": "number",
                "default": 3,
                "description": "Storage horizon in months (must be > 0). Defaults to 3.",
            },
        },
        "required": ["inventory_units", "unit_value", "storage_fee_per_unit_month"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "total_storage_fee": {"type": "number"},
            "insurance_cost": {"type": "number"},
            "financing_cost": {"type": "number"},
            "total_carry_cost": {"type": "number"},
            "carry_cost_per_unit": {"type": "number"},
            "breakeven_price_appreciation_pct": {"type": "number"},
            "timestamp": {"type": "string"},
        },
    },
}


def physical_storage_cost_calculator(
    inventory_units: float,
    unit_value: float,
    storage_fee_per_unit_month: float,
    insurance_pct_annual: float = 0.5,
    financing_rate_pct_annual: float = 6.0,
    months: float = 3,
    **_: Any,
) -> dict[str, Any]:
    """Return full carry cost stack for physical commodity inventory.

    Args:
        inventory_units: Quantity of commodity held (must be > 0).
        unit_value: Spot value per unit (must be > 0).
        storage_fee_per_unit_month: Flat storage charge per unit per month.
        insurance_pct_annual: Annual insurance as % of total inventory value.
        financing_rate_pct_annual: Annual cost of capital as % of inventory value.
        months: Storage horizon in months (must be > 0).

    Returns:
        dict with status, cost components, total carry, per-unit carry, and
        breakeven_price_appreciation_pct (the % price gain needed to cover carry).

    Formulas:
        storage_fee  = inventory_units * storage_fee_per_unit_month * months
        insurance    = inventory_value * (insurance_pct_annual / 100) * (months / 12)
        financing    = inventory_value * (financing_rate_pct_annual / 100) * (months / 12)
        total_carry  = storage_fee + insurance + financing
        per_unit     = total_carry / inventory_units
        breakeven_%  = (per_unit / unit_value) * 100
    """
    try:
        if inventory_units <= 0:
            raise ValueError("inventory_units must be positive")
        if unit_value <= 0:
            raise ValueError("unit_value must be positive")
        if months <= 0:
            raise ValueError("months must be positive")
        if storage_fee_per_unit_month < 0:
            raise ValueError("storage_fee_per_unit_month must be non-negative")
        if insurance_pct_annual < 0:
            raise ValueError("insurance_pct_annual must be non-negative")
        if financing_rate_pct_annual < 0:
            raise ValueError("financing_rate_pct_annual must be non-negative")

        inventory_value = inventory_units * unit_value
        t_fraction = months / 12.0  # year fraction

        storage_fee = inventory_units * storage_fee_per_unit_month * months
        insurance_cost = inventory_value * (insurance_pct_annual / 100.0) * t_fraction
        financing_cost = inventory_value * (financing_rate_pct_annual / 100.0) * t_fraction
        total_carry = storage_fee + insurance_cost + financing_cost
        per_unit = total_carry / inventory_units
        breakeven_pct = (per_unit / unit_value) * 100.0

        return {
            "status": "success",
            "total_storage_fee": round(storage_fee, 2),
            "insurance_cost": round(insurance_cost, 2),
            "financing_cost": round(financing_cost, 2),
            "total_carry_cost": round(total_carry, 2),
            "carry_cost_per_unit": round(per_unit, 4),
            "breakeven_price_appreciation_pct": round(breakeven_pct, 4),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("physical_storage_cost_calculator", str(exc))
        return {
            "status": "error",
            "error": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
