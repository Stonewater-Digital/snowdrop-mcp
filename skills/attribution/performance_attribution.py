"""Brinson-Fachler performance attribution."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "performance_attribution",
    "description": "Decomposes active return into allocation, selection, and interaction components.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "portfolio_weights": {"type": "object"},
            "portfolio_returns": {"type": "object"},
            "benchmark_weights": {"type": "object"},
            "benchmark_returns": {"type": "object"},
        },
        "required": [
            "portfolio_weights",
            "portfolio_returns",
            "benchmark_weights",
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


def performance_attribution(
    portfolio_weights: dict[str, float],
    portfolio_returns: dict[str, float],
    benchmark_weights: dict[str, float],
    benchmark_returns: dict[str, float],
    **_: Any,
) -> dict[str, Any]:
    """Return Brinson-Fachler attribution components."""

    try:
        assets = sorted(
            set(portfolio_weights) | set(benchmark_weights) | set(portfolio_returns) | set(benchmark_returns)
        )
        components: list[dict[str, Any]] = []
        total_active = 0.0
        for asset in assets:
            pw = float(portfolio_weights.get(asset, 0))
            bw = float(benchmark_weights.get(asset, 0))
            pr = float(portfolio_returns.get(asset, 0))
            br = float(benchmark_returns.get(asset, 0))
            allocation = (pw - bw) * br
            selection = bw * (pr - br)
            interaction = (pw - bw) * (pr - br)
            components.append(
                {
                    "asset": asset,
                    "allocation_effect": round(allocation, 6),
                    "selection_effect": round(selection, 6),
                    "interaction_effect": round(interaction, 6),
                }
            )
            total_active += pw * pr - bw * br

        data = {
            "components": components,
            "total_active_return": round(total_active, 6),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("performance_attribution", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
