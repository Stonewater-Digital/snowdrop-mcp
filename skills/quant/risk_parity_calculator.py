"""Compute risk parity weights from asset vol inputs."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "risk_parity_calculator",
    "description": "Allocates inverse-volatility weights and scales to a target portfolio volatility.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "asset_vols_pct": {
                "type": "object",
                "additionalProperties": {"type": "number"},
            },
            "target_portfolio_vol_pct": {"type": "number", "default": None},
        },
        "required": ["asset_vols_pct"],
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


def risk_parity_calculator(
    asset_vols_pct: dict[str, float],
    target_portfolio_vol_pct: float | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Return inverse-vol weights and leverage factor."""
    try:
        if not asset_vols_pct:
            raise ValueError("asset_vols_pct cannot be empty")
        inverse_vols = {asset: 1 / vol if vol else 0.0 for asset, vol in asset_vols_pct.items()}
        denom = sum(inverse_vols.values())
        if denom == 0:
            raise ValueError("All volatilities are zero")
        weights = {asset: value / denom for asset, value in inverse_vols.items()}
        portfolio_vol = math.sqrt(sum((weights[a] * asset_vols_pct[a]) ** 2 for a in weights))
        leverage = 1.0
        if target_portfolio_vol_pct and portfolio_vol:
            leverage = target_portfolio_vol_pct / portfolio_vol
        data = {
            "weights": {asset: round(weight, 4) for asset, weight in weights.items()},
            "implied_portfolio_vol_pct": round(portfolio_vol, 2),
            "leverage_factor": round(leverage, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        _log_lesson(f"risk_parity_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
