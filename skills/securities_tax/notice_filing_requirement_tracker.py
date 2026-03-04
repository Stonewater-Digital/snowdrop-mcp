"""Notice filing requirement tracker.
Determines which jurisdictions require notice filings for federal exempt offerings.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "notice_filing_requirement_tracker",
    "description": "Tracks Form D notice filing triggers and deadlines by state.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "states": {"type": "array", "items": {"type": "string"}},
            "offering_type": {"type": "string"},
        },
        "required": ["states", "offering_type"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}

FILING_REQUIRED = {"CA", "NY", "IL", "MA"}


def notice_filing_requirement_tracker(states: Sequence[str], offering_type: str, **_: Any) -> dict[str, Any]:
    """Return deadline and fee heuristics for each state."""
    try:
        normalized = offering_type.lower()
        results = []
        for state in states:
            st = state.upper()
            required = st in FILING_REQUIRED or normalized != "reg_d"
            deadline_days = 15 if normalized == "reg_d" else 30
            results.append({
                "state": st,
                "notice_required": required,
                "deadline_days": deadline_days,
                "fee": 300 if required else 0,
            })
        data = {
            "filing_requirements": results,
            "required_count": sum(1 for row in results if row["notice_required"]),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("notice_filing_requirement_tracker failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
