"""Calculate payback period for a renewable energy installation.

MCP Tool Name: renewable_energy_payback_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "renewable_energy_payback_calculator",
    "description": "Calculate the payback period for a renewable energy installation considering installation cost, incentives, annual savings, and maintenance costs.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "installation_cost": {
                "type": "number",
                "description": "Total installation cost in USD.",
            },
            "annual_savings": {
                "type": "number",
                "description": "Expected annual energy savings in USD.",
            },
            "incentives": {
                "type": "number",
                "description": "Total incentives, rebates, and tax credits in USD.",
                "default": 0,
            },
            "annual_maintenance": {
                "type": "number",
                "description": "Expected annual maintenance cost in USD.",
                "default": 0,
            },
        },
        "required": ["installation_cost", "annual_savings"],
    },
}


def renewable_energy_payback_calculator(
    installation_cost: float,
    annual_savings: float,
    incentives: float = 0,
    annual_maintenance: float = 0,
) -> dict[str, Any]:
    """Calculate renewable energy payback period."""
    try:
        if installation_cost <= 0:
            return {
                "status": "error",
                "data": {"error": "installation_cost must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        net_cost = installation_cost - incentives
        if net_cost < 0:
            net_cost = 0  # Incentives exceed cost

        net_annual_benefit = annual_savings - annual_maintenance

        if net_annual_benefit <= 0:
            return {
                "status": "ok",
                "data": {
                    "installation_cost": round(installation_cost, 2),
                    "incentives": round(incentives, 2),
                    "net_cost": round(net_cost, 2),
                    "annual_savings": round(annual_savings, 2),
                    "annual_maintenance": round(annual_maintenance, 2),
                    "net_annual_benefit": round(net_annual_benefit, 2),
                    "payback_years": None,
                    "note": "Annual maintenance exceeds or equals savings — investment does not pay back.",
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        payback_years = net_cost / net_annual_benefit

        # 25-year return
        total_benefit_25yr = net_annual_benefit * 25
        net_return_25yr = total_benefit_25yr - net_cost
        roi_25yr_pct = (net_return_25yr / net_cost * 100) if net_cost > 0 else float("inf")

        # 10-year return
        total_benefit_10yr = net_annual_benefit * 10
        net_return_10yr = total_benefit_10yr - net_cost

        return {
            "status": "ok",
            "data": {
                "installation_cost": round(installation_cost, 2),
                "incentives": round(incentives, 2),
                "net_cost": round(net_cost, 2),
                "annual_savings": round(annual_savings, 2),
                "annual_maintenance": round(annual_maintenance, 2),
                "net_annual_benefit": round(net_annual_benefit, 2),
                "payback_years": round(payback_years, 1),
                "ten_year_net_return": round(net_return_10yr, 2),
                "twenty_five_year_net_return": round(net_return_25yr, 2),
                "roi_25yr_pct": round(roi_25yr_pct, 1),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
