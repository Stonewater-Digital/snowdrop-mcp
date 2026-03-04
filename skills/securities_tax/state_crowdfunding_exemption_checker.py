"""State crowdfunding exemption checker.
Assesses compliance with intrastate and Tier 1/2 limits.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "state_crowdfunding_exemption_checker",
    "description": "Determines state crowdfunding eligibility based on issuer location and raise size.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "issuer_state": {"type": "string"},
            "investor_state": {"type": "string"},
            "offering_amount": {"type": "number"},
        },
        "required": ["issuer_state", "investor_state", "offering_amount"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}

INTRASTATE_CAP = 5_000_000


def state_crowdfunding_exemption_checker(
    issuer_state: str,
    investor_state: str,
    offering_amount: float,
    **_: Any,
) -> dict[str, Any]:
    """Return exemption availability and disqualification reason."""
    try:
        same_state = issuer_state.upper() == investor_state.upper()
        amount_ok = offering_amount <= INTRASTATE_CAP
        eligible = same_state and amount_ok
        data = {
            "eligible": eligible,
            "same_state": same_state,
            "amount_within_cap": amount_ok,
            "max_allowed": INTRASTATE_CAP,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("state_crowdfunding_exemption_checker failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
