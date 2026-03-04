"""Track inflation versus deflation regimes for Snowdrop tokens."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "inflation_deflation_tracker",
    "description": "Computes inflation rates and estimates deflation crossover dates.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "supply_snapshots": {"type": "array", "items": {"type": "object"}},
            "burn_rate_daily": {"type": "number"},
            "mint_rate_daily": {"type": "number"},
        },
        "required": ["supply_snapshots", "burn_rate_daily", "mint_rate_daily"],
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


def inflation_deflation_tracker(
    supply_snapshots: list[dict[str, Any]],
    burn_rate_daily: float,
    mint_rate_daily: float,
    **_: Any,
) -> dict[str, Any]:
    """Return inflation metrics and regime classification."""
    try:
        if not supply_snapshots:
            raise ValueError("supply_snapshots required")
        if burn_rate_daily < 0 or mint_rate_daily < 0:
            raise ValueError("Rates must be non-negative")
        ordered = sorted(supply_snapshots, key=lambda snap: snap["date"])
        first = ordered[0]
        last = ordered[-1]
        start_supply = float(first.get("circulating_supply", 0))
        end_supply = float(last.get("circulating_supply", 0))
        if start_supply <= 0:
            raise ValueError("Starting supply must be positive")
        start_date = datetime.fromisoformat(first["date"].replace("Z", "+00:00"))
        end_date = datetime.fromisoformat(last["date"].replace("Z", "+00:00"))
        days = max((end_date - start_date).days, 1)
        nominal_growth = (end_supply - start_supply) / start_supply
        annualized = (1 + nominal_growth) ** (365 / days) - 1
        annual_inflation_pct = round(annualized * 100, 4)

        regime = "stable"
        if mint_rate_daily > burn_rate_daily:
            regime = "inflationary"
        elif mint_rate_daily < burn_rate_daily:
            regime = "deflationary"

        deflation_crossover = _estimate_deflation_cross(
            last,
            burn_rate_daily,
            mint_rate_daily,
        )

        data = {
            "annual_inflation_pct": annual_inflation_pct,
            "regime": regime,
            "deflation_crossover_date": deflation_crossover,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("inflation_deflation_tracker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _estimate_deflation_cross(
    last_snapshot: dict[str, Any],
    burn_rate_daily: float,
    mint_rate_daily: float,
) -> str | None:
    last_date = datetime.fromisoformat(last_snapshot["date"].replace("Z", "+00:00"))
    total_supply = float(last_snapshot.get("total_supply", last_snapshot.get("circulating_supply", 0)))
    circulating = float(last_snapshot.get("circulating_supply", 0))
    if burn_rate_daily <= mint_rate_daily:
        return None
    net_burn = burn_rate_daily - mint_rate_daily
    buffer = max(total_supply - circulating, 0)
    if net_burn == 0:
        return None
    days_to_cross = buffer / net_burn if net_burn else 0
    crossover_date = last_date + timedelta(days=days_to_cross)
    return crossover_date.isoformat()


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
