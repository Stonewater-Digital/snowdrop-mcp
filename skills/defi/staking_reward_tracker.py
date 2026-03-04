"""Track validator staking rewards and accruals."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "staking_reward_tracker",
    "description": "Summarizes staking rewards, projected income, and outstanding claims per validator.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "stakes": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["stakes"],
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

_SECONDS_PER_DAY = 86400


def staking_reward_tracker(stakes: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return per-validator reward projections and totals."""
    try:
        breakdown = []
        total_monthly = 0.0
        total_annual = 0.0
        total_unclaimed = 0.0
        now = datetime.now(timezone.utc)
        for stake in stakes:
            staked_amount = float(stake.get("staked_amount", 0.0))
            reward_rate = float(stake.get("reward_rate_annual", 0.0))
            last_claim = stake.get("last_claim_date")
            last_claim_dt = (
                datetime.fromisoformat(str(last_claim)).replace(tzinfo=timezone.utc)
                if last_claim
                else now
            )
            elapsed_days = max(0.0, (now - last_claim_dt).total_seconds() / _SECONDS_PER_DAY)
            daily_rate = reward_rate / 365
            accrued = staked_amount * daily_rate * elapsed_days
            monthly = staked_amount * (reward_rate / 12)
            annual = staked_amount * reward_rate
            total_monthly += monthly
            total_annual += annual
            total_unclaimed += float(stake.get("unclaimed_rewards", 0.0)) + accrued
            breakdown.append(
                {
                    "validator": stake.get("validator"),
                    "chain": stake.get("chain"),
                    "staked_amount": staked_amount,
                    "monthly_rewards": round(monthly, 4),
                    "annual_rewards": round(annual, 4),
                    "accrued_since_last_claim": round(accrued, 4),
                    "unclaimed_total": round(float(stake.get("unclaimed_rewards", 0.0)) + accrued, 4),
                }
            )
        data = {
            "validators": breakdown,
            "total_monthly_rewards": round(total_monthly, 2),
            "total_annual_rewards": round(total_annual, 2),
            "aggregate_unclaimed": round(total_unclaimed, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": now.isoformat(),
        }
    except Exception as exc:
        _log_lesson("staking_reward_tracker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
