"""Calculate GP clawback obligations based on fund-level economics."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "gp_clawback_calculator",
    "description": "Evaluates carry distributions versus whole-fund entitlement and recommends clawback.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "fund_distributions": {"type": "array", "items": {"type": "object"}},
            "fund_total_contributions": {"type": "number"},
            "preferred_return_pct": {"type": "number", "default": 8.0},
            "gp_carry_pct": {"type": "number", "default": 20.0},
        },
        "required": ["fund_distributions", "fund_total_contributions"],
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


def gp_clawback_calculator(
    fund_distributions: list[dict[str, Any]],
    fund_total_contributions: float,
    preferred_return_pct: float = 8.0,
    gp_carry_pct: float = 20.0,
    **_: Any,
) -> dict[str, Any]:
    """Return GP clawback metrics based on whole-fund performance."""
    try:
        gp_received = sum(float(item.get("gp_carry_amount", 0.0)) for item in fund_distributions)
        lp_received = sum(float(item.get("lp_amount", 0.0)) for item in fund_distributions)
        total_distributions = gp_received + lp_received
        pref_required = fund_total_contributions * (preferred_return_pct / 100)
        whole_fund_profit = max(total_distributions - fund_total_contributions - pref_required, 0.0)
        gp_entitled = whole_fund_profit * (gp_carry_pct / 100)
        excess = max(gp_received - gp_entitled, 0.0)
        clawback_amount = excess
        escrow = max(clawback_amount * 0.25, 0.0)
        deals_underwater = [
            {
                "deal_name": item.get("deal_name"),
                "lp_shortfall": max(fund_total_contributions - item.get("lp_amount", 0.0), 0.0),
            }
            for item in fund_distributions
            if item.get("lp_amount", 0.0) < 0
        ]
        data = {
            "clawback_amount": round(clawback_amount, 2),
            "gp_carry_received": round(gp_received, 2),
            "gp_carry_entitled": round(gp_entitled, 2),
            "excess_carry": round(excess, 2),
            "escrow_recommended": round(escrow, 2),
            "deals_underwater": deals_underwater,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("gp_clawback_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
