"""Merit review state identifier.
Flags states requiring substantive review vs disclosure-based registration.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "merit_review_state_identifier",
    "description": "Identifies merit review states for state securities registration planning.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "states": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["states"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}

MERIT_STATES = {"AL", "MS", "SC", "ND"}


def merit_review_state_identifier(states: Sequence[str], **_: Any) -> dict[str, Any]:
    """Return lists of merit vs notice states."""
    try:
        merit = [state.upper() for state in states if state.upper() in MERIT_STATES]
        notice = [state.upper() for state in states if state.upper() not in MERIT_STATES]
        data = {
            "merit_states": merit,
            "notice_states": notice,
            "merit_ratio_pct": round(len(merit) / len(states) * 100 if states else 0.0, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("merit_review_state_identifier failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
