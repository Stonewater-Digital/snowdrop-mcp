"""Score DAO participation depth across voters and proposals.
Provides quick governance health diagnostics for contributors."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "dao_governance_participation_scorer",
    "description": "Assesses voter turnout and proposal engagement to highlight DAO governance strength.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "eligible_votes": {"type": "number", "description": "Total votes that could have been cast"},
            "votes_cast": {"type": "number", "description": "Actual votes submitted"},
            "proposals_total": {"type": "integer", "description": "Proposals during the measurement window"},
            "proposals_participated": {
                "type": "integer",
                "description": "Number of proposals with quorum participation",
            },
            "quorum_threshold_pct": {"type": "number", "description": "Quorum percentage target", "default": 20},
        },
        "required": ["eligible_votes", "votes_cast", "proposals_total", "proposals_participated"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"},
            "error": {"type": "string"},
        },
    },
}


def dao_governance_participation_scorer(
    eligible_votes: float,
    votes_cast: float,
    proposals_total: int,
    proposals_participated: int,
    quorum_threshold_pct: float = 20.0,
    **_: Any,
) -> dict[str, Any]:
    """Generate a composite DAO governance engagement score.

    Args:
        eligible_votes: Number of token votes outstanding.
        votes_cast: Votes counted in the window.
        proposals_total: Total proposals raised.
        proposals_participated: Proposals achieving quorum participation.
        quorum_threshold_pct: Target quorum share for success.

    Returns:
        Payload with turnout ratio, proposal engagement, and risk flags.
    """
    try:
        turnout_pct = votes_cast / eligible_votes * 100 if eligible_votes else 0.0
        proposal_participation_pct = (
            proposals_participated / proposals_total * 100 if proposals_total else 0.0
        )
        composite_score = round((turnout_pct * 0.6 + proposal_participation_pct * 0.4) / 100, 3)
        quorum_gap = max(quorum_threshold_pct - turnout_pct, 0)
        data = {
            "turnout_pct": round(turnout_pct, 2),
            "proposal_participation_pct": round(proposal_participation_pct, 2),
            "composite_score": composite_score,
            "quorum_gap_pct": round(quorum_gap, 2),
            "governance_health_flag": composite_score >= 0.5,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("dao_governance_participation_scorer failure: %s", exc)
        log_lesson(f"dao_governance_participation_scorer: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
