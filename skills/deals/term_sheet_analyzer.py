"""Analyze investor term sheet economics."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "term_sheet_analyzer",
    "description": "Evaluates post-money, ownership, and liquidation waterfalls for venture deals.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "pre_money_valuation": {"type": "number"},
            "investment_amount": {"type": "number"},
            "liquidation_preference": {"type": "number", "default": 1.0},
            "participation": {"type": "boolean", "default": False},
            "anti_dilution": {
                "type": "string",
                "enum": ["full_ratchet", "weighted_average", "none"],
            },
            "option_pool_pct": {"type": "number"},
        },
        "required": [
            "pre_money_valuation",
            "investment_amount",
            "liquidation_preference",
            "participation",
            "anti_dilution",
            "option_pool_pct",
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


def term_sheet_analyzer(
    pre_money_valuation: float,
    investment_amount: float,
    liquidation_preference: float,
    participation: bool,
    anti_dilution: str,
    option_pool_pct: float,
    **_: Any,
) -> dict[str, Any]:
    """Return ownership math and liquidation waterfall details."""
    try:
        if pre_money_valuation <= 0 or investment_amount <= 0:
            raise ValueError("valuations and investment_amount must be positive")
        post_money = pre_money_valuation + investment_amount
        investor_ownership = investment_amount / post_money
        pool_buffer = max(1e-9, 1 - option_pool_pct)
        fully_diluted_investor = min(1.0, investor_ownership / pool_buffer)
        founder_ownership = max(0.0, 1 - fully_diluted_investor - option_pool_pct)
        exit_values = [post_money * multiple for multiple in (0.5, 2, 5, 10)]
        waterfall = [
            _waterfall_row(
                exit_value,
                investment_amount,
                investor_ownership,
                liquidation_preference,
                participation,
            )
            for exit_value in exit_values
        ]

        data = {
            "post_money_valuation": round(post_money, 2),
            "investor_ownership": round(investor_ownership, 4),
            "fully_diluted_investor": round(fully_diluted_investor, 4),
            "founder_ownership": round(founder_ownership, 4),
            "option_pool_pct": round(option_pool_pct, 4),
            "anti_dilution": anti_dilution,
            "liquidation_waterfall": waterfall,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("term_sheet_analyzer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _waterfall_row(
    exit_value: float,
    investment_amount: float,
    investor_ownership: float,
    liquidation_preference: float,
    participation: bool,
) -> dict[str, Any]:
    preference = investment_amount * liquidation_preference
    remaining_pool = max(0.0, exit_value - preference)
    if participation:
        investor_take = preference + remaining_pool * investor_ownership
    else:
        pro_rata = exit_value * investor_ownership
        investor_take = max(preference, pro_rata)
    founder_take = max(0.0, exit_value - investor_take)
    return {
        "exit_value": round(exit_value, 2),
        "investor_return": round(investor_take, 2),
        "founder_return": round(founder_take, 2),
        "multiple_on_invested_capital": round(investor_take / investment_amount, 2),
    }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
