"""
Executive Summary: Builds a transition probability matrix from rating migration counts and reports drift metrics.
Inputs: rating_transitions (list[dict]), rating_scale (list[str])
Outputs: status (str), timestamp (str), data (dict)
MCP Tool Name: credit_migration_matrix
"""
import logging
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "credit_migration_matrix",
    "description": "Converts raw rating transition counts into normalized probability matrices and drift statistics.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "rating_transitions": {
                "type": "array",
                "items": {"type": "object"},
                "description": (
                    "List of records with 'from', 'to', and 'count' fields representing observed migrations."
                )
            },
            "rating_scale": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Ordered ratings from highest quality to default (e.g., ['AAA',...,'D'])."
            }
        },
        "required": ["rating_transitions", "rating_scale"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"}
        },
        "required": ["status", "timestamp"]
    }
}


def credit_migration_matrix(**kwargs: Any) -> dict[str, Any]:
    try:
        transitions = kwargs["rating_transitions"]
        scale = _clean_scale(kwargs["rating_scale"])
        counts = defaultdict(lambda: defaultdict(float))
        for record in transitions:
            frm = str(record.get("from", "")).strip().upper()
            to = str(record.get("to", "")).strip().upper()
            count = float(record.get("count", 0.0))
            if frm not in scale or to not in scale:
                raise ValueError("Transition ratings must exist in rating_scale")
            counts[frm][to] += count

        matrix = []
        upgrade_prob = 0.0
        downgrade_prob = 0.0
        for frm in scale:
            row_total = sum(counts[frm].values())
            if row_total == 0:
                raise ValueError(f"No transition counts found for {frm}")
            row = []
            for to in scale:
                prob = counts[frm][to] / row_total
                row.append(prob)
                if scale.index(to) < scale.index(frm):
                    upgrade_prob += prob
                elif scale.index(to) > scale.index(frm):
                    downgrade_prob += prob
            matrix.append(row)

        net_drift = upgrade_prob - downgrade_prob
        data = {
            "transition_matrix": matrix,
            "rating_scale": scale,
            "upgrade_probability": upgrade_prob,
            "downgrade_probability": downgrade_prob,
            "net_rating_drift": net_drift
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, KeyError) as e:
        logger.error("credit_migration_matrix failed: %s", e)
        _log_lesson(f"credit_migration_matrix: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _clean_scale(scale: Sequence[Any]) -> list[str]:
    if not scale:
        raise ValueError("rating_scale must be non-empty")
    unique = []
    for rating in scale:
        r = str(rating).strip().upper()
        if r in unique:
            raise ValueError("rating_scale contains duplicates")
        unique.append(r)
    return unique


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as file:
            file.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
