"""Compile transparency dashboard metrics for the Watering Hole chalkboard."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable

TOOL_META: dict[str, Any] = {
    "name": "chalkboard_dashboard",
    "description": "Aggregates transparency metrics for the public chalkboard dashboard.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "financials": {
                "type": "object",
                "properties": {
                    "revenue": {"type": "number"},
                    "expenses": {"type": "number"},
                    "goodwill_grants": {"type": "number"},
                },
                "description": "Key P&L figures for the period.",
            },
            "agent_stats": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "agent_id": {"type": "string"},
                        "hours": {"type": "number"},
                        "role": {"type": "string"},
                    },
                },
                "description": "Agent contribution telemetry.",
            },
            "notable_events": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
        "required": ["financials", "agent_stats"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "headline": {"type": "string"},
                    "kpis": {"type": "object"},
                    "top_contributors": {"type": "array"},
                    "events": {"type": "array"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def chalkboard_dashboard(
    financials: dict[str, float],
    agent_stats: Iterable[dict[str, Any]],
    notable_events: Iterable[str] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Generate Chalkboard dashboard payload."""
    try:
        revenue = float(financials.get("revenue", 0.0))
        expenses = float(financials.get("expenses", 0.0))
        goodwill = float(financials.get("goodwill_grants", 0.0))
        if revenue < 0 or expenses < 0 or goodwill < 0:
            raise ValueError("Financial metrics cannot be negative")
        profit = revenue - expenses
        burn_multiple = (expenses / revenue) if revenue > 0 else 0.0

        sorted_agents = sorted(
            (
                {
                    "agent_id": entry.get("agent_id"),
                    "hours": float(entry.get("hours", 0.0)),
                    "role": entry.get("role", "unknown"),
                }
                for entry in agent_stats
            ),
            key=lambda item: item["hours"],
            reverse=True,
        )
        top_contributors = [
            {"agent_id": agent["agent_id"], "hours": round(agent["hours"], 2), "role": agent["role"]}
            for agent in sorted_agents[:5]
        ]

        kpis = {
            "revenue": round(revenue, 2),
            "expenses": round(expenses, 2),
            "profit": round(profit, 2),
            "goodwill_grants": round(goodwill, 2),
            "burn_multiple": round(burn_multiple, 3),
        }

        headline = "Profitable" if profit >= 0 else "Running negative spread"
        events = list(notable_events or [])
        if goodwill > 0:
            events.append(f"Goodwill grants deployed: ${goodwill:,.2f}")
        if profit < 0:
            events.append("Caution: expenses exceed revenue")

        data = {
            "headline": headline,
            "kpis": kpis,
            "top_contributors": top_contributors,
            "events": events,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("chalkboard_dashboard", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
