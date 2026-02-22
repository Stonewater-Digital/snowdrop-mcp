"""Evaluate FX exposure for a portfolio."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "fx_risk_exposure_calculator",
    "description": "Aggregates gross/net FX exposures and estimates VaR.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "positions": {"type": "array", "items": {"type": "object"}},
            "base_currency": {"type": "string", "default": "USD"},
            "fx_rates": {"type": "object"},
            "vol_estimates": {"type": "object"},
        },
        "required": ["positions", "fx_rates", "vol_estimates"],
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def fx_risk_exposure_calculator(
    positions: list[dict[str, Any]],
    fx_rates: dict[str, float],
    vol_estimates: dict[str, float],
    base_currency: str = "USD",
    **_: Any,
) -> dict[str, Any]:
    """Return FX exposure metrics"""
    try:
        gross = {}
        net = {}
        var_components = []
        for pos in positions:
            currency = pos.get("currency", base_currency)
            value_local = pos.get("value_local", 0.0)
            rate = fx_rates.get(currency, 1.0)
            hedged_pct = pos.get("hedged_pct", 0.0)
            value_base = value_local * rate
            gross[currency] = gross.get(currency, 0.0) + abs(value_base)
            net_exposure = value_base * (1 - hedged_pct)
            net[currency] = net.get(currency, 0.0) + net_exposure
            sigma = vol_estimates.get(currency, 0.1)
            var_components.append((net_exposure, sigma))
        fx_var = math.sqrt(sum((exp * vol) ** 2 for exp, vol in var_components)) * 1.65
        largest = max(net, key=lambda k: abs(net[k]), default=base_currency)
        hedges = [
            {"currency": curr, "suggested_hedge": -amount}
            for curr, amount in net.items()
            if abs(amount) > 0.05 * gross.get(curr, 1)
        ]
        portfolio_beta = sum(net.values()) / sum(gross.values()) if gross else 0.0
        data = {
            "gross_exposure": gross,
            "net_exposure": net,
            "fx_var_95": round(fx_var, 2),
            "largest_risk": largest,
            "hedge_recommendations": hedges,
            "portfolio_fx_beta": round(portfolio_beta, 3),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("fx_risk_exposure_calculator", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
