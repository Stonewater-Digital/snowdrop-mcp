"""Perform DuPont analysis decomposing ROE into three components.

MCP Tool Name: dupont_analysis_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "dupont_analysis_calculator",
    "description": (
        "Performs DuPont analysis, decomposing return on equity into net profit "
        "margin, asset turnover, and equity multiplier (ROE = NPM x AT x EM)."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "net_income": {
                "type": "number",
                "description": "Net income for the period.",
            },
            "revenue": {
                "type": "number",
                "description": "Total revenue.",
            },
            "total_assets": {
                "type": "number",
                "description": "Total assets.",
            },
            "total_equity": {
                "type": "number",
                "description": "Total shareholders equity.",
            },
        },
        "required": ["net_income", "revenue", "total_assets", "total_equity"],
    },
}


def dupont_analysis_calculator(
    net_income: float, revenue: float, total_assets: float, total_equity: float
) -> dict[str, Any]:
    """Perform DuPont analysis."""
    try:
        net_income = float(net_income)
        revenue = float(revenue)
        total_assets = float(total_assets)
        total_equity = float(total_equity)

        if revenue == 0:
            raise ValueError("revenue must not be zero.")
        if total_assets == 0:
            raise ValueError("total_assets must not be zero.")
        if total_equity == 0:
            raise ValueError("total_equity must not be zero.")

        net_profit_margin = net_income / revenue
        asset_turnover = revenue / total_assets
        equity_multiplier = total_assets / total_equity
        roe = net_profit_margin * asset_turnover * equity_multiplier

        return {
            "status": "ok",
            "data": {
                "net_profit_margin": round(net_profit_margin, 6),
                "asset_turnover": round(asset_turnover, 6),
                "equity_multiplier": round(equity_multiplier, 6),
                "roe": round(roe, 6),
                "roe_pct": round(roe * 100, 4),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
