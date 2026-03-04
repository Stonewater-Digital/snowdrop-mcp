"""
Executive Summary: Structured haggling protocol for bot-to-bot service trades — calculates counter-offers, measures gap to agreement, and enforces a 5-round walk-away discipline.
Inputs: our_offer (dict: service, price, terms), their_ask (dict: service, price, terms), our_limits (dict: min_price, max_concessions (int)), round_number (int, default 1)
Outputs: counter_offer (dict), gap_pct (float), recommended_action (str: accept/counter/walk_away), rounds_remaining (int)
MCP Tool Name: agent_to_agent_negotiation
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "agent_to_agent_negotiation",
    "description": "Executes one round of a structured bot-to-bot price negotiation, generating a counter-offer or accept/walk-away recommendation within a 5-round protocol.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "our_offer": {
                "type": "object",
                "description": "Dict with service (str), price (float), terms (str).",
            },
            "their_ask": {
                "type": "object",
                "description": "Dict with service (str), price (float), terms (str).",
            },
            "our_limits": {
                "type": "object",
                "description": "Dict with min_price (float) and max_concessions (int, max rounds we'll negotiate).",
            },
            "round_number": {
                "type": "integer",
                "description": "Current negotiation round (1-indexed). Defaults to 1.",
                "default": 1,
            },
        },
        "required": ["our_offer", "their_ask", "our_limits"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "counter_offer": {"type": "object"},
            "gap_pct": {"type": "number"},
            "recommended_action": {"type": "string"},
            "rounds_remaining": {"type": "integer"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": ["status", "timestamp"],
    },
}

MAX_ROUNDS = 5
CLOSE_GAP_THRESHOLD_PCT = 10.0  # below this, split the difference
# Fraction of remaining gap to concede when gap > threshold
CONCESSION_FRACTION = 0.20


def _gap_pct(our_price: float, their_price: float) -> float:
    """Calculate the price gap as a percentage of the midpoint.

    Args:
        our_price: Our current offer price.
        their_price: Their current ask price.

    Returns:
        Gap percentage relative to the midpoint (always positive).
    """
    if our_price <= 0 and their_price <= 0:
        return 0.0
    midpoint = (our_price + their_price) / 2
    if midpoint == 0:
        return 0.0
    return round(abs(their_price - our_price) / midpoint * 100, 4)


def _build_counter(
    our_offer: dict,
    their_ask: dict,
    our_limits: dict,
    round_number: int,
) -> tuple[dict, float, str]:
    """Compute counter-offer price, gap, and recommended action.

    Protocol:
        - Round >= MAX_ROUNDS or rounds exhausted -> walk_away.
        - Gap < CLOSE_GAP_THRESHOLD_PCT -> accept (split diff is trivial).
        - Gap >= CLOSE_GAP_THRESHOLD_PCT -> counter at min_price + 20% of gap
          (moving toward their_ask from our hard floor).

    Args:
        our_offer: Our current offer dict.
        their_ask: Their current ask dict.
        our_limits: Contains min_price and max_concessions.
        round_number: Current round (1-indexed).

    Returns:
        Tuple of (counter_offer dict, gap_pct float, recommended_action str).
    """
    our_price = float(our_offer.get("price", 0.0))
    their_price = float(their_ask.get("price", 0.0))
    min_price = float(our_limits.get("min_price", our_price))
    max_concessions = int(our_limits.get("max_concessions", MAX_ROUNDS))
    effective_max = min(max_concessions, MAX_ROUNDS)

    gap = _gap_pct(our_price, their_price)

    # Determine direction: are they asking more or less than we offer?
    # In service sales: their_ask.price is what they want us to pay.
    # We want to pay as little as possible, so we offer lower.
    rounds_remaining = effective_max - round_number

    if rounds_remaining <= 0:
        return (
            {"service": our_offer.get("service"), "price": min_price, "terms": our_offer.get("terms", "")},
            gap,
            "walk_away",
        )

    # If we're already at or above their ask, accept immediately
    if our_price >= their_price:
        return (
            our_offer,
            0.0,
            "accept",
        )

    if gap < CLOSE_GAP_THRESHOLD_PCT:
        # Gap is trivial — split the difference
        midpoint = round((our_price + their_price) / 2, 4)
        counter_price = max(midpoint, min_price)
        return (
            {"service": our_offer.get("service"), "price": counter_price, "terms": our_offer.get("terms", "")},
            gap,
            "accept",
        )

    # Gap is meaningful — counter from our min_price toward their ask
    remaining_gap = their_price - min_price
    counter_price = round(min_price + CONCESSION_FRACTION * remaining_gap, 4)
    counter_price = max(counter_price, min_price)
    # Cap at their ask (don't overpay)
    counter_price = min(counter_price, their_price)

    counter_offer = {
        "service": our_offer.get("service"),
        "price": counter_price,
        "terms": our_offer.get("terms", ""),
    }
    new_gap = _gap_pct(counter_price, their_price)
    return counter_offer, new_gap, "counter"


def agent_to_agent_negotiation(
    our_offer: dict,
    their_ask: dict,
    our_limits: dict,
    round_number: int = 1,
    **kwargs: Any,
) -> dict:
    """Execute one round of a structured agent-to-agent negotiation.

    Protocol summary:
        - Max 5 rounds enforced globally; also bounded by our_limits.max_concessions.
        - If gap < 10%: recommend accept (split difference is noise).
        - If gap >= 10%: counter at min_price + 20% of gap toward their ask.
        - If rounds exhausted: walk_away at min_price.

    Args:
        our_offer: Dict with service (str), price (float), terms (str).
        their_ask: Dict with service (str), price (float), terms (str).
        our_limits: Dict with:
            min_price (float): Absolute floor — never go below this.
            max_concessions (int): Max rounds we will negotiate.
        round_number: Current round number (1-indexed). Defaults to 1.
        **kwargs: Ignored extra keyword arguments.

    Returns:
        Dict with keys:
            status (str): "success" or "error".
            counter_offer (dict): Our counter-offer for this round.
            gap_pct (float): Price gap as percentage of midpoint.
            recommended_action (str): "accept", "counter", or "walk_away".
            rounds_remaining (int): Rounds left before forced walk-away.
            negotiation_summary (dict): Key figures for this round.
            timestamp (str): ISO-8601 UTC timestamp.
    """
    try:
        max_concessions = int(our_limits.get("max_concessions", MAX_ROUNDS))
        effective_max = min(max_concessions, MAX_ROUNDS)
        rounds_remaining = max(0, effective_max - round_number)

        counter_offer, gap, action = _build_counter(
            our_offer, their_ask, our_limits, round_number
        )

        our_price = float(our_offer.get("price", 0.0))
        their_price = float(their_ask.get("price", 0.0))
        midpoint = round((our_price + their_price) / 2, 4)

        summary = {
            "our_current_price": our_price,
            "their_ask_price": their_price,
            "midpoint": midpoint,
            "counter_price": counter_offer.get("price"),
            "gap_pct_before": _gap_pct(our_price, their_price),
            "gap_pct_after_counter": gap,
            "round": round_number,
            "effective_max_rounds": effective_max,
        }

        return {
            "status": "success",
            "counter_offer": counter_offer,
            "gap_pct": gap,
            "recommended_action": action,
            "rounds_remaining": rounds_remaining,
            "negotiation_summary": summary,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"agent_to_agent_negotiation failed: {e}")
        _log_lesson(f"agent_to_agent_negotiation: {e}")
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
