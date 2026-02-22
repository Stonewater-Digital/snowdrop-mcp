"""
Executive Summary: Reputation scoring engine for peer agents — combines transaction success, uptime, longevity, skill breadth, and verification into a single 0-100 trust grade.
Inputs: agent_data (dict: agent_id, transaction_history (list[dict: counterparty, amount, success (bool), timestamp]), uptime_pct (float), skill_count (int), verified (bool), age_days (int))
Outputs: trust_score (float 0-100), grade (str: A/B/C/D/F), risk_flags (list), breakdown (dict)
MCP Tool Name: agent_trust_score_calc
"""
import math
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "agent_trust_score_calc",
    "description": "Calculates a 0-100 trust score for a peer agent based on transaction success rate, uptime, longevity, skill breadth, and verification status.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "agent_data": {
                "type": "object",
                "description": (
                    "Agent profile dict with keys: agent_id (str), "
                    "transaction_history (list of dicts with counterparty, amount, success, timestamp), "
                    "uptime_pct (float 0-100), skill_count (int), verified (bool), age_days (int)."
                ),
            }
        },
        "required": ["agent_data"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "trust_score": {"type": "number"},
            "grade": {"type": "string"},
            "risk_flags": {"type": "array"},
            "breakdown": {"type": "object"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": ["status", "timestamp"],
    },
}

# Weight constants (must sum to 1.0)
W_SUCCESS_RATE = 0.40
W_UPTIME = 0.20
W_LONGEVITY = 0.15
W_SKILL_BREADTH = 0.15
W_VERIFICATION = 0.10

# Longevity cap — after this many days the log scale plateaus near 1.0
LONGEVITY_CAP_DAYS = 730  # 2 years

# Skill breadth cap for normalization
SKILL_CAP = 20


def _success_rate_score(history: list[dict]) -> tuple[float, list[str]]:
    """Compute transaction success rate score (0-100) and surface risk flags.

    Args:
        history: List of transaction dicts, each with a 'success' bool.

    Returns:
        Tuple of (score 0-100, list of risk flag strings).
    """
    flags: list[str] = []
    if not history:
        flags.append("no_transaction_history")
        return 0.0, flags

    total = len(history)
    successes = sum(1 for tx in history if tx.get("success", False))
    rate = successes / total
    score = rate * 100

    if total < 5:
        flags.append("thin_transaction_history")
    if rate < 0.80:
        flags.append("high_failure_rate")

    # Check for large failed transactions
    failed_large = [
        tx for tx in history
        if not tx.get("success", True) and tx.get("amount", 0) > 10_000
    ]
    if failed_large:
        flags.append(f"large_failed_transactions_count={len(failed_large)}")

    return round(score, 2), flags


def _longevity_score(age_days: int) -> float:
    """Compute longevity score on a log scale capped at LONGEVITY_CAP_DAYS.

    Args:
        age_days: How many days the agent has existed.

    Returns:
        Score 0-100.
    """
    if age_days <= 0:
        return 0.0
    # log(1) = 0, log(LONGEVITY_CAP_DAYS+1) ~ 6.6 for 730 days
    raw = math.log(min(age_days, LONGEVITY_CAP_DAYS) + 1)
    max_raw = math.log(LONGEVITY_CAP_DAYS + 1)
    return round((raw / max_raw) * 100, 2)


def _skill_breadth_score(skill_count: int) -> float:
    """Normalize skill count against SKILL_CAP to produce a 0-100 score.

    Args:
        skill_count: Number of registered skills.

    Returns:
        Score 0-100.
    """
    return round(min(skill_count / SKILL_CAP, 1.0) * 100, 2)


def _letter_grade(score: float) -> str:
    """Convert numeric score to letter grade.

    Args:
        score: Trust score 0-100.

    Returns:
        Letter grade string: A, B, C, D, or F.
    """
    if score >= 90:
        return "A"
    if score >= 75:
        return "B"
    if score >= 60:
        return "C"
    if score >= 45:
        return "D"
    return "F"


def agent_trust_score_calc(agent_data: dict, **kwargs: Any) -> dict:
    """Calculate a composite trust score for a peer agent.

    Weights:
        - 40% transaction success rate
        - 20% uptime percentage
        - 15% longevity (log-scaled)
        - 15% skill breadth
        - 10% verification bonus

    Args:
        agent_data: Dict containing:
            agent_id (str): Unique identifier.
            transaction_history (list[dict]): Each dict has counterparty (str),
                amount (float), success (bool), timestamp (str).
            uptime_pct (float): 0-100 uptime percentage.
            skill_count (int): Number of registered skills.
            verified (bool): Whether the agent is verified.
            age_days (int): Days since the agent was created.
        **kwargs: Ignored extra keyword arguments.

    Returns:
        Dict with keys:
            status (str): "success" or "error".
            trust_score (float): Composite score 0-100.
            grade (str): Letter grade A/B/C/D/F.
            risk_flags (list[str]): Identified risk indicators.
            breakdown (dict): Per-component raw scores and weights.
            timestamp (str): ISO-8601 UTC timestamp.
    """
    try:
        history: list[dict] = agent_data.get("transaction_history", [])
        uptime_pct: float = float(agent_data.get("uptime_pct", 0.0))
        skill_count: int = int(agent_data.get("skill_count", 0))
        verified: bool = bool(agent_data.get("verified", False))
        age_days: int = int(agent_data.get("age_days", 0))

        success_score, risk_flags = _success_rate_score(history)
        uptime_score = max(0.0, min(100.0, uptime_pct))
        longevity_score = _longevity_score(age_days)
        breadth_score = _skill_breadth_score(skill_count)
        verification_score = 100.0 if verified else 0.0

        if uptime_pct < 95.0:
            risk_flags.append(f"low_uptime={uptime_pct:.1f}%")
        if age_days < 30:
            risk_flags.append("new_agent_less_than_30_days")
        if not verified:
            risk_flags.append("unverified")

        trust_score = (
            success_score * W_SUCCESS_RATE
            + uptime_score * W_UPTIME
            + longevity_score * W_LONGEVITY
            + breadth_score * W_SKILL_BREADTH
            + verification_score * W_VERIFICATION
        )
        trust_score = round(trust_score, 2)

        breakdown = {
            "transaction_success_rate": {
                "raw_score": success_score,
                "weight": W_SUCCESS_RATE,
                "contribution": round(success_score * W_SUCCESS_RATE, 2),
                "sample_size": len(history),
            },
            "uptime": {
                "raw_score": uptime_score,
                "weight": W_UPTIME,
                "contribution": round(uptime_score * W_UPTIME, 2),
            },
            "longevity": {
                "raw_score": longevity_score,
                "weight": W_LONGEVITY,
                "contribution": round(longevity_score * W_LONGEVITY, 2),
                "age_days": age_days,
            },
            "skill_breadth": {
                "raw_score": breadth_score,
                "weight": W_SKILL_BREADTH,
                "contribution": round(breadth_score * W_SKILL_BREADTH, 2),
                "skill_count": skill_count,
            },
            "verification": {
                "raw_score": verification_score,
                "weight": W_VERIFICATION,
                "contribution": round(verification_score * W_VERIFICATION, 2),
                "verified": verified,
            },
        }

        return {
            "status": "success",
            "agent_id": agent_data.get("agent_id", "unknown"),
            "trust_score": trust_score,
            "grade": _letter_grade(trust_score),
            "risk_flags": risk_flags,
            "breakdown": breakdown,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"agent_trust_score_calc failed: {e}")
        _log_lesson(f"agent_trust_score_calc: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    """Append a lesson-learned entry to logs/lessons.md.

    Args:
        message: Description of the error or lesson.
    """
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
