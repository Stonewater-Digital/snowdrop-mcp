"""Brinson-style performance attribution."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "performance_attribution_tool",
    "description": "Performs allocation, selection, and interaction attribution vs a benchmark.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "portfolio_weights": {"type": "object"},
            "benchmark_weights": {"type": "object"},
            "portfolio_returns": {"type": "object"},
            "benchmark_returns": {"type": "object"},
        },
        "required": [
            "portfolio_weights",
            "benchmark_weights",
            "portfolio_returns",
            "benchmark_returns",
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


def performance_attribution_tool(
    portfolio_weights: dict[str, float],
    benchmark_weights: dict[str, float],
    portfolio_returns: dict[str, float],
    benchmark_returns: dict[str, float],
    **_: Any,
) -> dict[str, Any]:
    """Return Brinson attribution components."""
    try:
        sectors = set(portfolio_weights) | set(benchmark_weights)
        allocation_effect = 0.0
        selection_effect = 0.0
        interaction_effect = 0.0
        breakdown: list[dict[str, Any]] = []
        for sector in sorted(sectors):
            pw = portfolio_weights.get(sector, 0.0)
            bw = benchmark_weights.get(sector, 0.0)
            pr = portfolio_returns.get(sector, benchmark_returns.get(sector, 0.0))
            br = benchmark_returns.get(sector, 0.0)
            allocation = (pw - bw) * br
            selection = bw * (pr - br)
            interaction = (pw - bw) * (pr - br)
            allocation_effect += allocation
            selection_effect += selection
            interaction_effect += interaction
            breakdown.append(
                {
                    "sector": sector,
                    "allocation_effect": round(allocation, 6),
                    "selection_effect": round(selection, 6),
                    "interaction_effect": round(interaction, 6),
                    "portfolio_weight": round(pw, 4),
                    "benchmark_weight": round(bw, 4),
                }
            )
        total_active = allocation_effect + selection_effect + interaction_effect
        data = {
            "allocation_effect": round(allocation_effect, 6),
            "selection_effect": round(selection_effect, 6),
            "interaction_effect": round(interaction_effect, 6),
            "total_active_return": round(total_active, 6),
            "sector_breakdown": breakdown,
        }
        return {"status": "ok", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        try:
            with open("logs/lessons.md", "a") as _f:
                _f.write(f"- [{datetime.now(timezone.utc).isoformat()}] performance_attribution_tool: {exc}\n")
        except OSError:
            pass
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
