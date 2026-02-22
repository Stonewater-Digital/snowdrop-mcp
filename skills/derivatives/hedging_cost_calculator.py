"""Estimate costs and protections for hedging overlays."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "hedging_cost_calculator",
    "description": "Quantifies hedging cost, downside, and upside caps across hedge types.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "position_value": {"type": "number"},
            "hedge_type": {
                "type": "string",
                "enum": ["protective_put", "collar", "futures", "inverse_etf"],
            },
            "hedge_params": {"type": "object"},
        },
        "required": ["position_value", "hedge_type", "hedge_params"],
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


def hedging_cost_calculator(
    position_value: float,
    hedge_type: str,
    hedge_params: dict[str, Any],
    **_: Any,
) -> dict[str, Any]:
    """Calculate hedge economics for the requested overlay."""
    try:
        if position_value <= 0:
            raise ValueError("position_value must be positive")
        hedge_type = hedge_type.lower()
        calculators = {
            "protective_put": _protective_put_metrics,
            "collar": _collar_metrics,
            "futures": _futures_metrics,
            "inverse_etf": _inverse_etf_metrics,
        }
        if hedge_type not in calculators:
            raise ValueError(f"Unsupported hedge_type: {hedge_type}")

        result = calculators[hedge_type](position_value, hedge_params)
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("hedging_cost_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _protective_put_metrics(position_value: float, params: dict[str, Any]) -> dict[str, Any]:
    premium = float(params.get("put_premium", 0))
    strike = float(params.get("put_strike", 0))
    if premium <= 0 or strike <= 0:
        raise ValueError("protective_put requires put_premium and put_strike")
    days = int(params.get("days_covered", 90))
    hedge_cost_pct = (premium / position_value) * 100
    max_loss = max(position_value - strike, 0) + premium
    annualized = hedge_cost_pct * (365 / days)
    return {
        "hedge_cost_pct": round(hedge_cost_pct, 4),
        "max_loss_after_hedge": round(max_loss, 4),
        "upside_cap": None,
        "cost_of_protection_annual": round(annualized, 4),
    }


def _collar_metrics(position_value: float, params: dict[str, Any]) -> dict[str, Any]:
    put_premium = float(params.get("put_premium", 0))
    call_premium = float(params.get("call_premium", 0))
    put_strike = float(params.get("collar_put_strike", 0))
    call_strike = float(params.get("collar_call_strike", 0))
    if min(put_premium, put_strike, call_strike) <= 0:
        raise ValueError("collar requires strike and premium inputs")
    days = int(params.get("days_covered", 90))
    net_cost = put_premium - call_premium
    hedge_cost_pct = (net_cost / position_value) * 100
    max_loss = max(position_value - put_strike, 0) + max(net_cost, 0)
    upside_cap = max(call_strike - position_value, 0)
    annualized = hedge_cost_pct * (365 / days)
    return {
        "hedge_cost_pct": round(hedge_cost_pct, 4),
        "max_loss_after_hedge": round(max_loss, 4),
        "upside_cap": round(upside_cap, 4),
        "cost_of_protection_annual": round(annualized, 4),
    }


def _futures_metrics(position_value: float, params: dict[str, Any]) -> dict[str, Any]:
    margin_pct = float(params.get("futures_margin_pct", 5.0))
    basis_cost_pct = float(params.get("basis_cost_pct", 0.25))
    residual_basis_pct = float(params.get("residual_basis_pct", 0.5))
    days = int(params.get("days_covered", 30))
    hedge_cost_pct = margin_pct + basis_cost_pct
    max_loss = position_value * residual_basis_pct / 100
    annualized = hedge_cost_pct * (365 / days)
    return {
        "hedge_cost_pct": round(hedge_cost_pct, 4),
        "max_loss_after_hedge": round(max_loss, 4),
        "upside_cap": None,
        "cost_of_protection_annual": round(annualized, 4),
    }


def _inverse_etf_metrics(position_value: float, params: dict[str, Any]) -> dict[str, Any]:
    expense_ratio_pct = float(params.get("etf_expense_ratio_pct", 1.0))
    tracking_error_pct = float(params.get("tracking_error_pct", 0.75))
    coverage_pct = float(params.get("coverage_pct", 100.0))
    days = int(params.get("days_covered", 60))
    effective_cost_pct = (expense_ratio_pct + tracking_error_pct) * (coverage_pct / 100)
    hedge_cost_pct = effective_cost_pct
    residual = position_value * (1 - coverage_pct / 100)
    annualized = hedge_cost_pct * (365 / days)
    return {
        "hedge_cost_pct": round(hedge_cost_pct, 4),
        "max_loss_after_hedge": round(residual, 4),
        "upside_cap": None,
        "cost_of_protection_annual": round(annualized, 4),
    }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
