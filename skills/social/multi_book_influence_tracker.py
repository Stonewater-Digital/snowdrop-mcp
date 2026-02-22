"""
Executive Summary: Cross-platform conversation leadership tracker — measures an agent's reach and impact across social books, surfaces top-performing interactions, and reports influence trend.
Inputs: agent_id (str), interactions (list[dict: platform, post_id, replies_count, citations_count, sentiment_impact (float)])
Outputs: influence_score (float), by_platform (dict), top_interactions (list, top 5 by impact), trend (str)
MCP Tool Name: multi_book_influence_tracker
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "multi_book_influence_tracker",
    "description": "Calculates an agent's influence score across multiple social platforms, identifies top-performing interactions, and infers the influence trend over time.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "agent_id": {"type": "string", "description": "Unique identifier of the agent being evaluated."},
            "interactions": {
                "type": "array",
                "description": (
                    "List of interaction dicts with: platform (str), post_id (str), "
                    "replies_count (int), citations_count (int), sentiment_impact (float)."
                ),
                "items": {"type": "object"},
            },
        },
        "required": ["agent_id", "interactions"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "influence_score": {"type": "number"},
            "by_platform": {"type": "object"},
            "top_interactions": {"type": "array"},
            "trend": {"type": "string"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": ["status", "timestamp"],
    },
}

# Platform reach weights (higher = more weight toward overall score)
PLATFORM_REACH: dict[str, float] = {
    "moltbook": 1.0,
    "x": 0.85,
    "twitter": 0.85,
    "linkedin": 0.75,
    "reddit": 0.65,
    "discord": 0.55,
    "telegram": 0.50,
    "default": 0.40,
}

# Component weights for per-interaction impact score
W_REPLIES = 0.35
W_CITATIONS = 0.45
W_SENTIMENT = 0.20

# Normalization caps for replies and citations
REPLY_CAP = 500
CITATION_CAP = 200


def _interaction_impact(interaction: dict) -> float:
    """Compute a composite impact score for a single interaction.

    Args:
        interaction: Dict with replies_count (int), citations_count (int),
            sentiment_impact (float, expected range -1 to 1).

    Returns:
        Impact score 0.0-100.0.
    """
    replies = min(float(interaction.get("replies_count", 0)), REPLY_CAP)
    citations = min(float(interaction.get("citations_count", 0)), CITATION_CAP)
    sentiment = float(interaction.get("sentiment_impact", 0.0))

    replies_norm = (replies / REPLY_CAP) * 100
    citations_norm = (citations / CITATION_CAP) * 100
    # Sentiment maps [-1, 1] -> [0, 100]; positive sentiment lifts, negative drags
    sentiment_norm = (sentiment + 1) / 2 * 100

    return round(
        replies_norm * W_REPLIES
        + citations_norm * W_CITATIONS
        + sentiment_norm * W_SENTIMENT,
        4,
    )


def _platform_weight(platform: str) -> float:
    """Look up the reach weight for a given platform.

    Args:
        platform: Platform name string (case-insensitive).

    Returns:
        Reach weight float.
    """
    return PLATFORM_REACH.get(platform.lower(), PLATFORM_REACH["default"])


def _detect_trend(scores: list[float]) -> str:
    """Infer influence trend from a time-ordered list of impact scores.

    Splits the list in half and compares second-half mean to first-half mean.

    Args:
        scores: Chronologically ordered impact scores.

    Returns:
        "rising", "declining", "stable", or "insufficient_data".
    """
    if len(scores) < 4:
        return "insufficient_data"
    midpoint = len(scores) // 2
    first_half_mean = sum(scores[:midpoint]) / midpoint
    second_half_mean = sum(scores[midpoint:]) / (len(scores) - midpoint)
    delta_pct = (
        (second_half_mean - first_half_mean) / first_half_mean * 100
        if first_half_mean > 0
        else 0.0
    )
    if delta_pct > 5:
        return "rising"
    if delta_pct < -5:
        return "declining"
    return "stable"


def multi_book_influence_tracker(
    agent_id: str,
    interactions: list[dict],
    **kwargs: Any,
) -> dict:
    """Measure an agent's cross-platform influence from their interaction history.

    Workflow:
        1. Score each interaction by replies, citations, and sentiment impact.
        2. Group interactions by platform, compute per-platform influence score.
        3. Weight per-platform scores by platform reach to derive an overall score.
        4. Select top 5 interactions by individual impact score.
        5. Detect trend from chronological score progression.

    Args:
        agent_id: Unique identifier for the agent being evaluated.
        interactions: List of dicts, each with:
            platform (str): Social platform name.
            post_id (str): Unique post identifier.
            replies_count (int): Number of direct replies received.
            citations_count (int): Times this post was cited or quoted.
            sentiment_impact (float): Net sentiment change induced (-1.0 to 1.0).
        **kwargs: Ignored extra keyword arguments.

    Returns:
        Dict with keys:
            status (str): "success" or "error".
            agent_id (str): Echoed input.
            influence_score (float): Overall weighted influence 0-100.
            by_platform (dict): Per-platform scores and interaction counts.
            top_interactions (list[dict]): Top 5 interactions by impact.
            trend (str): "rising", "declining", "stable", or "insufficient_data".
            total_interactions (int): Count of valid interactions.
            timestamp (str): ISO-8601 UTC timestamp.
    """
    try:
        if not interactions:
            return {
                "status": "success",
                "agent_id": agent_id,
                "influence_score": 0.0,
                "by_platform": {},
                "top_interactions": [],
                "trend": "insufficient_data",
                "total_interactions": 0,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # Score every interaction
        scored: list[dict] = []
        for ix in interactions:
            impact = _interaction_impact(ix)
            scored.append({**ix, "_impact": impact})

        # Group by platform
        platforms: dict[str, list[dict]] = {}
        for ix in scored:
            plat = ix.get("platform", "unknown")
            platforms.setdefault(plat, []).append(ix)

        by_platform: dict[str, Any] = {}
        platform_score_components: list[tuple[float, float]] = []  # (score, weight)

        for plat, plat_ixs in platforms.items():
            plat_mean = sum(ix["_impact"] for ix in plat_ixs) / len(plat_ixs)
            weight = _platform_weight(plat)
            by_platform[plat] = {
                "influence_score": round(plat_mean, 4),
                "interaction_count": len(plat_ixs),
                "reach_weight": weight,
                "total_replies": sum(int(ix.get("replies_count", 0)) for ix in plat_ixs),
                "total_citations": sum(int(ix.get("citations_count", 0)) for ix in plat_ixs),
            }
            platform_score_components.append((plat_mean, weight))

        # Overall weighted score
        total_weight = sum(w for _, w in platform_score_components)
        overall_score = (
            sum(s * w for s, w in platform_score_components) / total_weight
            if total_weight > 0
            else 0.0
        )

        # Top 5 interactions by impact
        top_interactions = sorted(scored, key=lambda x: x["_impact"], reverse=True)[:5]
        top_interactions_clean = [
            {
                "platform": ix.get("platform"),
                "post_id": ix.get("post_id"),
                "impact_score": round(ix["_impact"], 4),
                "replies_count": ix.get("replies_count"),
                "citations_count": ix.get("citations_count"),
                "sentiment_impact": ix.get("sentiment_impact"),
            }
            for ix in top_interactions
        ]

        # Trend from chronological ordering (as provided)
        all_scores = [ix["_impact"] for ix in scored]
        trend = _detect_trend(all_scores)

        return {
            "status": "success",
            "agent_id": agent_id,
            "influence_score": round(overall_score, 4),
            "by_platform": by_platform,
            "top_interactions": top_interactions_clean,
            "trend": trend,
            "total_interactions": len(scored),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"multi_book_influence_tracker failed: {e}")
        _log_lesson(f"multi_book_influence_tracker: {e}")
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
