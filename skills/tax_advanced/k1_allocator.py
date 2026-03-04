"""Allocate partnership K-1 amounts and capital accounts."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "k1_allocator",
    "description": "Allocates income, deductions, and distributions across partners with special allocations.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "partners": {"type": "array", "items": {"type": "object"}},
            "fund_income": {"type": "object"},
            "fund_deductions": {"type": "object"},
            "distributions": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["partners", "fund_income", "fund_deductions", "distributions"],
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


def k1_allocator(
    partners: list[dict[str, Any]],
    fund_income: dict[str, float],
    fund_deductions: dict[str, float],
    distributions: list[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    """Return partner K-1 allocations and capital account roll-forward."""
    try:
        total_ownership = sum(partner.get("ownership_pct", 0.0) for partner in partners) or 1.0
        k1_data = []
        capital_accounts = []
        total_allocated = {key: 0.0 for key in fund_income.keys() | fund_deductions.keys()}
        dist_map = {dist.get("partner"): dist.get("amount", 0.0) for dist in distributions}
        for partner in partners:
            share = partner.get("ownership_pct", 0.0) / total_ownership
            special = partner.get("special_allocations", {}) or {}
            income_alloc = {key: value * share for key, value in fund_income.items()}
            deduction_alloc = {key: value * share for key, value in fund_deductions.items()}
            for key, override in special.items():
                income_alloc[key] = override
            for key, amount in income_alloc.items():
                total_allocated[key] = total_allocated.get(key, 0.0) + amount
            for key, amount in deduction_alloc.items():
                total_allocated[key] = total_allocated.get(key, 0.0) - amount
            capital_begin = partner.get("capital_account", 0.0)
            net = sum(income_alloc.values()) - sum(deduction_alloc.values())
            ending_capital = capital_begin + net - dist_map.get(partner.get("name"), 0.0)
            k1_data.append(
                {
                    "partner": partner.get("name"),
                    "income": income_alloc,
                    "deductions": deduction_alloc,
                    "distributions": dist_map.get(partner.get("name"), 0.0),
                }
            )
            capital_accounts.append(
                {
                    "partner": partner.get("name"),
                    "beginning": capital_begin,
                    "net_income": net,
                    "distributions": dist_map.get(partner.get("name"), 0.0),
                    "ending": ending_capital,
                }
            )
        data = {
            "k1_data": k1_data,
            "capital_accounts": capital_accounts,
            "total_allocated": total_allocated,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("k1_allocator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
