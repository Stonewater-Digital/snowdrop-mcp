"""Model LP commitment pacing to maintain target allocation."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "commitment_pacing_model",
    "description": "Suggests annual commitments and overcommitment ratios for PE allocation targets.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "total_portfolio": {"type": "number"},
            "target_pe_allocation_pct": {"type": "number"},
            "current_pe_nav": {"type": "number"},
            "unfunded_commitments": {"type": "number"},
            "expected_distributions_annual": {"type": "number"},
            "expected_calls_annual": {"type": "number"},
            "new_fund_avg_size": {"type": "number"},
        },
        "required": [
            "total_portfolio",
            "target_pe_allocation_pct",
            "current_pe_nav",
            "unfunded_commitments",
            "expected_distributions_annual",
            "expected_calls_annual",
            "new_fund_avg_size",
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


def commitment_pacing_model(
    total_portfolio: float,
    target_pe_allocation_pct: float,
    current_pe_nav: float,
    unfunded_commitments: float,
    expected_distributions_annual: float,
    expected_calls_annual: float,
    new_fund_avg_size: float,
    **_: Any,
) -> dict[str, Any]:
    """Return commitment pacing metrics."""
    try:
        target_nav = total_portfolio * (target_pe_allocation_pct / 100)
        current_allocation_pct = (current_pe_nav / total_portfolio) * 100 if total_portfolio else 0.0
        nav_gap = target_nav - current_pe_nav
        overcommitment_ratio = (current_pe_nav + unfunded_commitments) / target_nav if target_nav else 0.0
        net_cashflow = expected_calls_annual - expected_distributions_annual
        commitment_budget = max(nav_gap + net_cashflow, 0.0)
        years_to_target = int(max(nav_gap / (net_cashflow + new_fund_avg_size), 1)) if net_cashflow + new_fund_avg_size else 1
        projected_nav_path = []
        nav = current_pe_nav
        for year in range(1, years_to_target + 1):
            nav = nav + new_fund_avg_size - expected_distributions_annual
            projected_nav_path.append({"year": year, "projected_nav": round(nav, 2)})
        data = {
            "current_allocation_pct": round(current_allocation_pct, 2),
            "overcommitment_ratio": round(overcommitment_ratio, 2),
            "annual_commitment_budget": round(commitment_budget, 2),
            "years_to_target": years_to_target,
            "projected_nav_path": projected_nav_path,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("commitment_pacing_model", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
