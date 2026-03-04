"""Calculate ROI and payback period for a solar panel installation.

MCP Tool Name: solar_panel_roi_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "solar_panel_roi_calculator",
    "description": "Calculate solar panel ROI including federal ITC, annual degradation, payback period, and 25-year total return.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "system_cost": {
                "type": "number",
                "description": "Total system installation cost in USD.",
            },
            "annual_production_kwh": {
                "type": "number",
                "description": "Expected first-year energy production in kWh.",
            },
            "electricity_rate": {
                "type": "number",
                "description": "Current electricity rate in $/kWh.",
                "default": 0.16,
            },
            "annual_degradation": {
                "type": "number",
                "description": "Annual panel output degradation rate as a decimal.",
                "default": 0.005,
            },
            "federal_itc": {
                "type": "number",
                "description": "Federal Investment Tax Credit rate as a decimal (30% through 2032).",
                "default": 0.30,
            },
        },
        "required": ["system_cost", "annual_production_kwh"],
    },
}


def solar_panel_roi_calculator(
    system_cost: float,
    annual_production_kwh: float,
    electricity_rate: float = 0.16,
    annual_degradation: float = 0.005,
    federal_itc: float = 0.30,
) -> dict[str, Any]:
    """Calculate solar panel ROI."""
    try:
        if system_cost <= 0 or annual_production_kwh <= 0:
            return {
                "status": "error",
                "data": {"error": "system_cost and annual_production_kwh must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        itc_savings = system_cost * federal_itc
        net_cost = system_cost - itc_savings

        # Year-by-year analysis over 25 years
        total_savings = 0.0
        payback_year = None
        cumulative = -net_cost
        yearly_data = []

        for year in range(1, 26):
            production = annual_production_kwh * (1 - annual_degradation) ** (year - 1)
            # Assume electricity rate increases 2.5% per year
            rate = electricity_rate * (1.025) ** (year - 1)
            savings = production * rate
            total_savings += savings
            cumulative += savings

            if payback_year is None and cumulative >= 0:
                payback_year = year

            if year <= 5 or year % 5 == 0:
                yearly_data.append({
                    "year": year,
                    "production_kwh": round(production, 0),
                    "rate_per_kwh": round(rate, 4),
                    "annual_savings": round(savings, 2),
                    "cumulative_net": round(cumulative, 2),
                })

        total_return = total_savings - net_cost
        roi_pct = (total_return / net_cost * 100) if net_cost > 0 else 0

        first_year_savings = annual_production_kwh * electricity_rate
        simple_payback = net_cost / first_year_savings if first_year_savings > 0 else float("inf")

        return {
            "status": "ok",
            "data": {
                "system_cost": round(system_cost, 2),
                "federal_itc_savings": round(itc_savings, 2),
                "net_cost_after_itc": round(net_cost, 2),
                "first_year_production_kwh": round(annual_production_kwh, 0),
                "first_year_savings": round(first_year_savings, 2),
                "simple_payback_years": round(simple_payback, 1),
                "actual_payback_year": payback_year,
                "total_25yr_savings": round(total_savings, 2),
                "total_25yr_return": round(total_return, 2),
                "roi_25yr_pct": round(roi_pct, 1),
                "selected_yearly_data": yearly_data,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
