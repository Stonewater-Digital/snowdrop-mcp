"""Allocate fund-of-funds capital across underlying funds with constraints."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "fund_of_funds_allocator",
    "description": "Creates a heuristic allocation maximizing expected return under diversification rules.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "fof_capital": {"type": "number"},
            "underlying_funds": {"type": "array", "items": {"type": "object"}},
            "constraints": {"type": "object"},
        },
        "required": ["fof_capital", "underlying_funds", "constraints"],
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


def fund_of_funds_allocator(
    fof_capital: float,
    underlying_funds: list[dict[str, Any]],
    constraints: dict[str, Any],
    **_: Any,
) -> dict[str, Any]:
    """Return allocation suggestions with diversification metrics."""
    try:
        allocations = []
        remaining = fof_capital
        strategy_limits = {}
        max_single_pct = constraints.get("max_single_fund_pct", 0.2)
        max_strategy_pct = constraints.get("max_strategy_pct", 0.4)
        for fund in sorted(underlying_funds, key=lambda x: x.get("target_return", 0.0), reverse=True):
            if remaining <= 0:
                break
            strategy = fund.get("strategy", "other")
            strategy_used = strategy_limits.get(strategy, 0.0)
            max_for_fund = min(
                remaining,
                fof_capital * max_single_pct,
                fof_capital * max_strategy_pct - strategy_used,
            )
            max_for_fund = max(max_for_fund, 0.0)
            allocation = min(max_for_fund, fund.get("max_commitment", max_for_fund))
            allocation = max(allocation, fund.get("min_commitment", 0.0))
            if allocation <= 0:
                continue
            remaining -= allocation
            strategy_limits[strategy] = strategy_limits.get(strategy, 0.0) + allocation
            allocations.append(
                {
                    "fund_name": fund.get("fund_name"),
                    "strategy": strategy,
                    "vintage": fund.get("vintage"),
                    "allocation": round(allocation, 2),
                    "expected_return": fund.get("target_return"),
                    "risk_score": fund.get("risk_score"),
                }
            )
        expected_return = sum(item["allocation"] * item["expected_return"] for item in allocations)
        expected_portfolio_return = expected_return / fof_capital if fof_capital else 0.0
        diversification_score = 1 - max(strategy_limits.values(), default=0) / fof_capital if fof_capital else 0.0
        data = {
            "allocations": allocations,
            "expected_portfolio_return": round(expected_portfolio_return, 4),
            "diversification_score": round(diversification_score, 3),
            "constraint_utilization": strategy_limits,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("fund_of_funds_allocator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
