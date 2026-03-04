"""Add contextual ROI annotations to Ghost Ledger transactions."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "ghost_ledger_enricher",
    "description": "Annotates Ghost Ledger transactions with ROI heuristics and metadata.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "transactions": {
                "type": "array",
                "items": {"type": "object"},
            }
        },
        "required": ["transactions"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "enriched_transactions": {
                        "type": "array",
                        "items": {"type": "object"},
                    }
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}

ROI_NOTES = {
    "api_call": "Enabled downstream analytics queries without throttling",
    "infra": "Sustained uptime for Snowdrop core services",
    "revenue": "Recorded realized inflows to Stonewater treasury",
    "goodwill": "Community or partner goodwill investment",
    "compliance": "Supported regulatory or fiduciary coverage",
}


def ghost_ledger_enricher(transactions: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Attach heuristic ROI labels and timestamps to Ghost Ledger entries."""

    try:
        enriched: list[dict[str, Any]] = []
        enrichment_time = datetime.now(timezone.utc).isoformat()
        for tx in transactions:
            category = str(tx.get("category", "undesignated")).lower()
            amount = tx.get("amount")
            annotation = ROI_NOTES.get(category, "Operational spend awaiting Thunder review")
            value_score = _score_value(category, amount)
            enriched.append(
                {
                    **tx,
                    "roi_annotation": annotation,
                    "value_score": value_score,
                    "enriched_at": enrichment_time,
                }
            )

        return {
            "status": "success",
            "data": {"enriched_transactions": enriched},
            "timestamp": enrichment_time,
        }
    except Exception as exc:
        _log_lesson("ghost_ledger_enricher", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _score_value(category: str, amount: Any) -> float:
    try:
        amt = float(amount)
    except (TypeError, ValueError):
        amt = 0.0
    base = {
        "revenue": 1.5,
        "goodwill": 1.0,
        "api_call": 1.2,
        "infra": 0.9,
        "compliance": 1.1,
    }.get(category, 0.8)
    magnitude = 0.0 if amt == 0 else min(2.0, abs(amt) / 1000)
    return round(base + magnitude, 3)


def _log_lesson(skill_name: str, error: str) -> None:
    """Append a Ralph Wiggum lesson entry."""

    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
