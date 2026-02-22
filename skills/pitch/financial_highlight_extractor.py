"""Extract high-signal financial storytelling points."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "financial_highlight_extractor",
    "description": "Summarizes headline metrics, growth narratives, and risks for presentations.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "financials": {"type": "object"},
        },
        "required": ["financials"],
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


def financial_highlight_extractor(financials: dict[str, Any], **_: Any) -> dict[str, Any]:
    """Return highlight-ready storytelling components."""
    try:
        revenue = financials.get("revenue_monthly", []) or []
        expenses = financials.get("expenses_monthly", []) or []
        cash_balance = float(financials.get("cash_balance", 0.0))
        active_agents = financials.get("active_agents", 0)
        skills_count = financials.get("skills_count", 0)

        revenue_growth = _growth(revenue)
        expense_growth = _growth(expenses)
        best_metric = "MRR growth" if revenue_growth >= expense_growth else "Efficiency"
        headline = f"${revenue[-1]:,.0f} MRR" if revenue else "Momentum building"
        growth_story = f"Revenue up {revenue_growth:.1f}% in the latest period"
        risk_callout = None
        if expense_growth > revenue_growth:
            risk_callout = "Expense growth outpacing revenue; tighten opex"

        key_metrics = [
            {"name": "MRR", "value": revenue[-1] if revenue else 0, "growth_pct": revenue_growth},
            {"name": "Cash", "value": cash_balance, "growth_pct": None},
            {"name": "Active Agents", "value": active_agents, "growth_pct": None},
            {"name": "Skills", "value": skills_count, "growth_pct": None},
        ]
        one_liner = f"Snowdrop posts {headline} servicing {active_agents} active agents across {skills_count} skills."
        data = {
            "headline": headline,
            "key_metrics": key_metrics,
            "growth_story": growth_story,
            "risk_callout": risk_callout,
            "one_liner": one_liner,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("financial_highlight_extractor", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _growth(series: list[Any]) -> float:
    if len(series) < 2:
        return 0.0
    start = float(series[0])
    end = float(series[-1])
    if start == 0:
        return 100.0 if end > 0 else 0.0
    return ((end - start) / start) * 100


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
