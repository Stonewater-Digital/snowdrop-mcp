"""Perform DuPont ROE decomposition."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "dupont_analysis",
    "description": "Returns 3-stage and 5-stage DuPont ROE decomposition.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "net_income": {"type": "number"},
            "revenue": {"type": "number"},
            "total_assets": {"type": "number"},
            "total_equity": {"type": "number"},
            "ebit": {"type": "number"},
            "pretax_income": {"type": "number"},
            "interest_expense": {"type": "number"},
        },
        "required": [
            "net_income",
            "revenue",
            "total_assets",
            "total_equity",
            "ebit",
            "pretax_income",
            "interest_expense",
        ],
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


def dupont_analysis(
    net_income: float,
    revenue: float,
    total_assets: float,
    total_equity: float,
    ebit: float,
    pretax_income: float,
    interest_expense: float,
    **_: Any,
) -> dict[str, Any]:
    """Return DuPont ratios and improvement levers."""
    try:
        profit_margin = net_income / revenue if revenue else 0.0
        asset_turnover = revenue / total_assets if total_assets else 0.0
        equity_multiplier = total_assets / total_equity if total_equity else 0.0
        roe = profit_margin * asset_turnover * equity_multiplier
        tax_burden = net_income / pretax_income if pretax_income else 0.0
        interest_burden = pretax_income / ebit if ebit else 0.0
        ebit_margin = ebit / revenue if revenue else 0.0
        five_stage = {
            "tax_burden": tax_burden,
            "interest_burden": interest_burden,
            "ebit_margin": ebit_margin,
            "asset_turnover": asset_turnover,
            "equity_multiplier": equity_multiplier,
        }
        three_stage = {
            "profit_margin": profit_margin,
            "asset_turnover": asset_turnover,
            "equity_multiplier": equity_multiplier,
        }
        primary_driver = max(three_stage, key=three_stage.get)
        improvement_lever = min(three_stage, key=three_stage.get)
        data = {
            "roe": round(roe, 4),
            "three_stage": {k: round(v, 4) for k, v in three_stage.items()},
            "five_stage": {k: round(v, 4) for k, v in five_stage.items()},
            "primary_driver": primary_driver,
            "improvement_lever": improvement_lever,
            "peer_comparison_note": "Focus on asset turnover if lagging peers.",
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("dupont_analysis", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
