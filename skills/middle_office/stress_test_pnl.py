"""Stress test P&L calculator."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "stress_test_pnl",
    "description": "Applies factor shocks to estimate stressed P&L for positions.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "positions": {"type": "array", "items": {"type": "object"}},
            "shocks": {"type": "object"},
        },
        "required": ["positions", "shocks"],
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


def stress_test_pnl(positions: list[dict[str, Any]], shocks: dict[str, float], **_: Any) -> dict[str, Any]:
    """Return total and factor-level stressed P&L."""
    try:
        eq_shock = shocks.get("equity_shock_pct", 0.0) / 100.0
        rate_shock = shocks.get("rate_shock_bps", 0.0) / 10000.0
        credit_shock = shocks.get("credit_spread_shock_bps", 0.0) / 10000.0
        fx_shock = shocks.get("fx_shock_pct", 0.0) / 100.0
        equity_pnl = 0.0
        rates_pnl = 0.0
        credit_pnl = 0.0
        fx_pnl = 0.0
        breakdown: list[dict[str, Any]] = []
        for row in positions or []:
            market_value = float(row.get("market_value", 0.0))
            beta = float(row.get("beta", 0.0))
            duration = float(row.get("duration", 0.0))
            delta = float(row.get("delta", 0.0))
            equity_move = market_value * beta * eq_shock
            rate_move = -market_value * duration * rate_shock
            credit_move = -market_value * credit_shock
            fx_move = market_value * delta * fx_shock
            position_pnl = equity_move + rate_move + credit_move + fx_move
            equity_pnl += equity_move
            rates_pnl += rate_move
            credit_pnl += credit_move
            fx_pnl += fx_move
            breakdown.append(
                {
                    "security_id": row.get("security_id"),
                    "stressed_pnl": round(position_pnl, 2),
                }
            )
        total = equity_pnl + rates_pnl + credit_pnl + fx_pnl
        data = {
            "total_stressed_pnl": round(total, 2),
            "equity_pnl": round(equity_pnl, 2),
            "rates_pnl": round(rates_pnl, 2),
            "credit_pnl": round(credit_pnl, 2),
            "fx_pnl": round(fx_pnl, 2),
            "position_breakdown": breakdown,
        }
        return {"status": "ok", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        try:
            with open("logs/lessons.md", "a") as _f:
                _f.write(f"- [{datetime.now(timezone.utc).isoformat()}] stress_test_pnl: {exc}\n")
        except OSError:
            pass
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
