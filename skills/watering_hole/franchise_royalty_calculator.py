"""Calculate franchise royalties for Bar-in-a-Box partners."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable

ROYALTY_RATE = 0.10

TOOL_META: dict[str, Any] = {
    "name": "franchise_royalty_calculator",
    "description": "Computes 10% RSS revenue royalties owed by Bar-in-a-Box franchisees.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "sub_bars": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "rss_revenue": {"type": "number"},
                    },
                },
                "description": "Per-franchise revenue feed entries.",
            }
        },
        "required": ["sub_bars"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "royalties": {"type": "array"},
                    "total_revenue": {"type": "number"},
                    "total_royalty": {"type": "number"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def franchise_royalty_calculator(sub_bars: Iterable[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Calculate 10% revenue share royalties.

    Args:
        sub_bars: Iterable of franchise entries with name and rss_revenue.
        **_: Ignored keyword arguments.

    Returns:
        Royalty ledger plus totals.
    """
    try:
        royalties = []
        total_revenue = 0.0
        total_royalty = 0.0
        for bar in sub_bars:
            name = bar.get("name")
            revenue = float(bar.get("rss_revenue", 0.0))
            if not name:
                raise ValueError("Each sub-bar must include a name")
            if revenue < 0:
                raise ValueError(f"rss_revenue cannot be negative (name={name})")
            royalty = revenue * ROYALTY_RATE
            total_revenue += revenue
            total_royalty += royalty
            royalties.append({
                "name": name,
                "rss_revenue": round(revenue, 2),
                "royalty_due": round(royalty, 2),
            })

        data = {
            "royalties": royalties,
            "total_revenue": round(total_revenue, 2),
            "total_royalty": round(total_royalty, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("franchise_royalty_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
