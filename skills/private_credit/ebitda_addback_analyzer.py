"""Normalize EBITDA by categorizing addbacks."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

QUALITY_WEIGHTS = {
    "high": 1.0,
    "medium": 0.5,
    "low": 0.2,
}

TOOL_META: dict[str, Any] = {
    "name": "ebitda_addback_analyzer",
    "description": "Scores EBITDA addbacks by quality to show normalized EBITDA.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "base_ebitda": {"type": "number"},
            "addbacks": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "string"},
                        "amount": {"type": "number"},
                        "quality": {"type": "string", "enum": ["high", "medium", "low"]},
                    },
                    "required": ["category", "amount", "quality"],
                },
            },
        },
        "required": ["base_ebitda", "addbacks"],
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


def ebitda_addback_analyzer(
    base_ebitda: float,
    addbacks: list[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    """Return normalized EBITDA with weighting by addback quality."""
    try:
        weighted_addbacks = 0.0
        category_totals: dict[str, float] = defaultdict(float)
        for entry in addbacks:
            category = entry.get("category", "uncategorized")
            amount = float(entry.get("amount", 0.0))
            quality = entry.get("quality", "low").lower()
            weight = QUALITY_WEIGHTS.get(quality, 0.2)
            weighted_addbacks += amount * weight
            category_totals[category] += amount
        normalized_ebitda = base_ebitda + weighted_addbacks
        recurring_ratio = weighted_addbacks / normalized_ebitda if normalized_ebitda else 0.0
        data = {
            "base_ebitda": round(base_ebitda, 2),
            "gross_addbacks": round(sum(category_totals.values()), 2),
            "weighted_addbacks": round(weighted_addbacks, 2),
            "normalized_ebitda": round(normalized_ebitda, 2),
            "recurring_quality_ratio": round(recurring_ratio, 3),
            "category_breakdown": {k: round(v, 2) for k, v in category_totals.items()},
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("ebitda_addback_analyzer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
