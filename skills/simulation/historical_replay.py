"""Replay historical stress periods against the current portfolio."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "historical_replay",
    "description": "Applies historical drawdowns to portfolio weights to estimate losses.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "portfolio": {
                "type": "array",
                "items": {"type": "object"},
            },
            "historical_period": {"type": "object"},
        },
        "required": ["portfolio", "historical_period"],
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


def historical_replay(
    portfolio: list[dict[str, Any]],
    historical_period: dict[str, Any],
    **_: Any,
) -> dict[str, Any]:
    """Estimate losses under a named stress period."""
    try:
        if not isinstance(portfolio, list) or not portfolio:
            raise ValueError("portfolio must be a non-empty list")
        if not isinstance(historical_period, dict):
            raise ValueError("historical_period must be a dict")

        drawdowns = historical_period.get("asset_drawdowns", {}) or {}
        if not isinstance(drawdowns, dict):
            raise ValueError("historical_period.asset_drawdowns must be a dict")

        weights_sum = sum(float(asset.get("weight", 0.0)) for asset in portfolio)
        if weights_sum <= 0:
            raise ValueError("Portfolio weights must sum to a positive number")

        contributions: list[dict[str, Any]] = []
        total_loss_pct = 0.0
        for asset in portfolio:
            name = str(asset.get("asset", "unknown"))
            weight = float(asset.get("weight", 0.0)) / weights_sum
            drawdown_pct = float(drawdowns.get(name, drawdowns.get("default", 0.0)))
            contribution = weight * drawdown_pct
            total_loss_pct += contribution
            contributions.append(
                {
                    "asset": name,
                    "weight_pct": round(weight * 100, 2),
                    "drawdown_pct": round(drawdown_pct * 100, 2),
                    "contribution_pct": round(contribution * 100, 2),
                }
            )

        contributions.sort(key=lambda item: item["contribution_pct"])  # most negative first
        recovery_months = int(historical_period.get("recovery_months") or max(int(abs(total_loss_pct) * 18), 1))

        result = {
            "scenario_name": str(historical_period.get("name", "unknown_period")),
            "projected_portfolio_loss_pct": round(total_loss_pct * 100, 2),
            "loss_contributors": contributions,
            "recovery_timeline_months": recovery_months,
            "top_drawdown_drivers": contributions[:3],
        }
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("historical_replay", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
