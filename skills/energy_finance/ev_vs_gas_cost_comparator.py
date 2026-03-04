"""Compare annual fuel costs: electric vehicle vs gasoline vehicle.

MCP Tool Name: ev_vs_gas_cost_comparator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "ev_vs_gas_cost_comparator",
    "description": "Compare annual fuel costs between an EV and a gasoline vehicle based on annual miles, efficiency, and energy prices.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "annual_miles": {
                "type": "number",
                "description": "Annual miles driven.",
            },
            "ev_efficiency_kwh_per_mile": {
                "type": "number",
                "description": "EV energy consumption in kWh per mile.",
                "default": 0.30,
            },
            "gas_mpg": {
                "type": "number",
                "description": "Gasoline vehicle fuel efficiency in miles per gallon.",
                "default": 30,
            },
            "electricity_rate": {
                "type": "number",
                "description": "Electricity cost in $/kWh.",
                "default": 0.16,
            },
            "gas_price": {
                "type": "number",
                "description": "Gasoline price in $/gallon.",
                "default": 3.50,
            },
        },
        "required": ["annual_miles"],
    },
}


def ev_vs_gas_cost_comparator(
    annual_miles: float,
    ev_efficiency_kwh_per_mile: float = 0.30,
    gas_mpg: float = 30,
    electricity_rate: float = 0.16,
    gas_price: float = 3.50,
) -> dict[str, Any]:
    """Compare EV vs gas annual fuel costs."""
    try:
        if annual_miles < 0:
            return {
                "status": "error",
                "data": {"error": "annual_miles must be non-negative."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if gas_mpg <= 0:
            return {
                "status": "error",
                "data": {"error": "gas_mpg must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # EV costs
        ev_kwh_annual = annual_miles * ev_efficiency_kwh_per_mile
        ev_annual_cost = ev_kwh_annual * electricity_rate
        ev_cost_per_mile = ev_efficiency_kwh_per_mile * electricity_rate

        # Gas costs
        gas_gallons_annual = annual_miles / gas_mpg
        gas_annual_cost = gas_gallons_annual * gas_price
        gas_cost_per_mile = gas_price / gas_mpg

        # Comparison
        annual_savings = gas_annual_cost - ev_annual_cost
        savings_pct = (annual_savings / gas_annual_cost * 100) if gas_annual_cost > 0 else 0

        # 5-year projection (assume 3% annual price increases)
        ev_5yr = sum(ev_annual_cost * (1.03 ** yr) for yr in range(5))
        gas_5yr = sum(gas_annual_cost * (1.03 ** yr) for yr in range(5))

        return {
            "status": "ok",
            "data": {
                "annual_miles": round(annual_miles, 0),
                "ev": {
                    "efficiency_kwh_per_mile": ev_efficiency_kwh_per_mile,
                    "annual_kwh": round(ev_kwh_annual, 1),
                    "electricity_rate": electricity_rate,
                    "annual_cost": round(ev_annual_cost, 2),
                    "cost_per_mile": round(ev_cost_per_mile, 4),
                    "five_year_cost": round(ev_5yr, 2),
                },
                "gas": {
                    "mpg": gas_mpg,
                    "annual_gallons": round(gas_gallons_annual, 1),
                    "gas_price": gas_price,
                    "annual_cost": round(gas_annual_cost, 2),
                    "cost_per_mile": round(gas_cost_per_mile, 4),
                    "five_year_cost": round(gas_5yr, 2),
                },
                "annual_savings_with_ev": round(annual_savings, 2),
                "savings_pct": round(savings_pct, 1),
                "five_year_savings": round(gas_5yr - ev_5yr, 2),
                "recommendation": "EV" if annual_savings > 0 else "Gas",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
