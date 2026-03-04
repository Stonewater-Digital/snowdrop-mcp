"""Compute Sharpe, Sortino, and Calmar ratios."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "sharpe_ratio_calculator",
    "description": "Calculates Sharpe, Sortino, and Calmar ratios from a return series.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "returns": {"type": "array", "items": {"type": "number"}},
            "risk_free_rate": {"type": "number", "default": 0.0},
            "periods_per_year": {"type": "integer", "default": 252},
        },
        "required": ["returns"],
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


def sharpe_ratio_calculator(
    returns: list[float],
    risk_free_rate: float = 0.0,
    periods_per_year: int = 252,
    **_: Any,
) -> dict[str, Any]:
    """Return Sharpe, Sortino, Calmar, and helper stats."""
    try:
        if not returns:
            raise ValueError("returns must not be empty")
        avg_return = sum(returns) / len(returns)
        excess_returns = [r - risk_free_rate / periods_per_year for r in returns]
        variance = sum((r - avg_return) ** 2 for r in returns) / len(returns)
        volatility = math.sqrt(max(variance, 0.0))
        annualized_return = (1 + avg_return) ** periods_per_year - 1
        annualized_vol = volatility * math.sqrt(periods_per_year)
        downside_returns = [min(0.0, r - risk_free_rate / periods_per_year) for r in returns]
        downside_var = sum(dr ** 2 for dr in downside_returns) / len(returns)
        downside_vol = math.sqrt(max(downside_var, 0.0))
        sharpe = (
            (annualized_return - risk_free_rate) / annualized_vol if annualized_vol else 0.0
        )
        sortino = (
            (annualized_return - risk_free_rate) / (downside_vol * math.sqrt(periods_per_year))
            if downside_vol
            else 0.0
        )
        cumulative = 1.0
        peak = 1.0
        max_drawdown = 0.0
        for r in returns:
            cumulative *= 1 + r
            peak = max(peak, cumulative)
            drawdown = (cumulative - peak) / peak
            max_drawdown = min(max_drawdown, drawdown)
        calmar = (annualized_return - risk_free_rate) / abs(max_drawdown) if max_drawdown else 0.0
        data = {
            "sharpe_ratio": round(sharpe, 4),
            "sortino_ratio": round(sortino, 4),
            "calmar_ratio": round(calmar, 4),
            "annualized_return_pct": round(annualized_return * 100, 2),
            "annualized_volatility_pct": round(annualized_vol * 100, 2),
            "max_drawdown_pct": round(abs(max_drawdown) * 100, 2),
        }
        return {"status": "ok", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        try:
            with open("logs/lessons.md", "a") as _f:
                _f.write(f"- [{datetime.now(timezone.utc).isoformat()}] sharpe_ratio_calculator: {exc}\n")
        except OSError:
            pass
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
