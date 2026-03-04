"""State securities exemption checker.
Flags whether an offering qualifies for common state exemptions.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "state_securities_exemption_checker",
    "description": "Determines state exemption availability by offering type and investor count.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "states": {"type": "array", "items": {"type": "string"}},
            "offering_type": {"type": "string"},
            "investor_count": {"type": "number"},
        },
        "required": ["states", "offering_type", "investor_count"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}

SAFE_HARBOR_STATES = {"CA", "NY", "TX", "WA", "CO"}


def state_securities_exemption_checker(states: Sequence[str], offering_type: str, investor_count: int, **_: Any) -> dict[str, Any]:
    """Return per-state exemption status using simple heuristics."""
    try:
        normalized_type = offering_type.lower()
        results = []
        for state in states:
            upper_state = state.upper()
            qualifies = normalized_type in {"reg_d", "private"} and investor_count <= 35
            if upper_state in SAFE_HARBOR_STATES:
                qualifies = True
            results.append({"state": upper_state, "exempt": qualifies})
        exemption_rate = sum(1 for row in results if row["exempt"]) / len(results) if results else 0.0
        data = {
            "state_results": results,
            "exemption_rate_pct": round(exemption_rate * 100, 2),
            "offering_type": normalized_type,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("state_securities_exemption_checker failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
