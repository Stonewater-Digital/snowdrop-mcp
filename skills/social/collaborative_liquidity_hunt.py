"""
Executive Summary: Coordinated thin-market alpha engine — validates and assembles a trusted agent coalition to capture spread on illiquid opportunities too large for a single bot.
Inputs: opportunity (dict: asset, market, current_spread_bps, estimated_size, min_participants), participants (list[dict: agent_id, available_capital, trust_score])
Outputs: viable (bool), allocation_plan (list[dict]), combined_capital (float), expected_spread_capture_bps (float)
MCP Tool Name: collaborative_liquidity_hunt
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "collaborative_liquidity_hunt",
    "description": "Validates whether a group of trusted agents has sufficient combined capital to exploit a thin-market spread opportunity and produces a pro-rata allocation plan.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "opportunity": {
                "type": "object",
                "description": (
                    "Dict with keys: asset (str), market (str), "
                    "current_spread_bps (float), estimated_size (float), "
                    "min_participants (int)."
                ),
            },
            "participants": {
                "type": "array",
                "description": "List of dicts with agent_id (str), available_capital (float), trust_score (float 0-100).",
                "items": {"type": "object"},
            },
        },
        "required": ["opportunity", "participants"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "viable": {"type": "boolean"},
            "allocation_plan": {"type": "array"},
            "combined_capital": {"type": "number"},
            "expected_spread_capture_bps": {"type": "number"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": ["status", "timestamp"],
    },
}

# Minimum trust score to participate
MIN_TRUST_SCORE = 70.0

# Spread capture efficiency degrades slightly with more participants (coordination overhead)
PARTICIPANT_EFFICIENCY_DECAY = 0.02  # lose 2% capture efficiency per extra participant beyond 2


def _spread_capture(
    spread_bps: float,
    n_participants: int,
    capital_utilization: float,
) -> float:
    """Estimate realizable spread capture in basis points.

    Accounts for coordination overhead with more participants and
    partial capital utilization reducing market impact.

    Args:
        spread_bps: Quoted spread in basis points.
        n_participants: Number of agents in the coalition.
        capital_utilization: Fraction of estimated_size covered (0.0-1.0+).

    Returns:
        Expected spread capture in basis points (never negative).
    """
    efficiency = max(
        0.50,
        1.0 - PARTICIPANT_EFFICIENCY_DECAY * max(0, n_participants - 2),
    )
    # Partial utilization gives partial capture; over-capitalization is fine
    utilization_factor = min(capital_utilization, 1.0)
    return round(spread_bps * efficiency * utilization_factor, 4)


def collaborative_liquidity_hunt(
    opportunity: dict,
    participants: list[dict],
    **kwargs: Any,
) -> dict:
    """Assemble a trusted-agent coalition to exploit a thin-market spread.

    Workflow:
        1. Filter participants with trust_score >= 70.
        2. Sum available capital of eligible participants.
        3. Check minimum participant count and minimum capital requirements.
        4. Allocate capital pro-rata by available_capital.
        5. Estimate spread capture accounting for coordination overhead.

    Args:
        opportunity: Dict with keys:
            asset (str): Ticker or asset identifier.
            market (str): Exchange or venue name.
            current_spread_bps (float): Current bid-ask spread in bps.
            estimated_size (float): Target position size in USD.
            min_participants (int): Minimum agents required.
        participants: List of dicts, each with:
            agent_id (str): Unique agent identifier.
            available_capital (float): USD available to deploy.
            trust_score (float): Trust score 0-100.
        **kwargs: Ignored extra keyword arguments.

    Returns:
        Dict with keys:
            status (str): "success" or "error".
            viable (bool): Whether the opportunity is actionable.
            allocation_plan (list[dict]): Per-agent capital allocation.
            combined_capital (float): Total eligible capital.
            expected_spread_capture_bps (float): Estimated realizable spread.
            ineligible_count (int): Participants filtered out by trust score.
            viability_reasons (list[str]): Reasons if not viable.
            timestamp (str): ISO-8601 UTC timestamp.
    """
    try:
        asset = opportunity.get("asset", "UNKNOWN")
        market = opportunity.get("market", "UNKNOWN")
        spread_bps = float(opportunity.get("current_spread_bps", 0.0))
        estimated_size = float(opportunity.get("estimated_size", 0.0))
        min_participants = int(opportunity.get("min_participants", 2))

        # Step 1: Filter by trust score
        eligible = [
            p for p in participants
            if float(p.get("trust_score", 0)) >= MIN_TRUST_SCORE
            and float(p.get("available_capital", 0)) > 0
        ]
        ineligible_count = len(participants) - len(eligible)

        viability_reasons: list[str] = []

        # Step 2: Combined capital
        combined_capital = sum(float(p.get("available_capital", 0)) for p in eligible)

        # Step 3: Viability checks
        if len(eligible) < min_participants:
            viability_reasons.append(
                f"insufficient_eligible_agents: need {min_participants}, have {len(eligible)}"
            )
        if combined_capital < estimated_size:
            viability_reasons.append(
                f"insufficient_capital: need {estimated_size:.2f}, have {combined_capital:.2f}"
            )
        if spread_bps <= 0:
            viability_reasons.append("spread_bps_must_be_positive")

        viable = len(viability_reasons) == 0

        # Step 4: Pro-rata allocation
        allocation_plan: list[dict] = []
        if eligible and combined_capital > 0:
            # Sort by trust score descending so highest-trust agents appear first
            eligible_sorted = sorted(
                eligible, key=lambda p: float(p.get("trust_score", 0)), reverse=True
            )
            # Allocate up to estimated_size; if over-capitalized, scale down
            deploy_total = min(combined_capital, estimated_size) if viable else combined_capital
            for p in eligible_sorted:
                cap = float(p.get("available_capital", 0))
                share = cap / combined_capital
                allocated = round(share * deploy_total, 2)
                allocation_plan.append({
                    "agent_id": p.get("agent_id", "unknown"),
                    "trust_score": float(p.get("trust_score", 0)),
                    "available_capital": cap,
                    "allocated_amount": allocated,
                    "share_pct": round(share * 100, 2),
                })

        # Step 5: Expected spread capture
        capital_utilization = (
            min(combined_capital, estimated_size) / estimated_size
            if estimated_size > 0 else 0.0
        )
        expected_spread_capture_bps = (
            _spread_capture(spread_bps, len(eligible), capital_utilization)
            if viable else 0.0
        )

        return {
            "status": "success",
            "asset": asset,
            "market": market,
            "viable": viable,
            "viability_reasons": viability_reasons,
            "allocation_plan": allocation_plan,
            "combined_capital": round(combined_capital, 2),
            "estimated_size": estimated_size,
            "capital_utilization_pct": round(capital_utilization * 100, 2),
            "eligible_participant_count": len(eligible),
            "ineligible_count": ineligible_count,
            "expected_spread_capture_bps": expected_spread_capture_bps,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"collaborative_liquidity_hunt failed: {e}")
        _log_lesson(f"collaborative_liquidity_hunt: {e}")
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
