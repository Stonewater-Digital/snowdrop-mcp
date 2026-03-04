"""
Executive Summary: Agent social network narrative shift detector — scores Moltbook posts for financial sentiment and flags when a submolt's tone changes significantly.
Inputs: posts (list[dict]: author, content, timestamp, upvotes, submolt), lookback_hours (int, default 24)
Outputs: overall_sentiment (float -1 to 1), by_submolt (dict), narrative_shifts (list), trending_topics (list)
MCP Tool Name: moltbook_sentiment_analyzer
"""
import os
import math
import logging
import re
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "moltbook_sentiment_analyzer",
    "description": "Scores Moltbook posts for financial sentiment and detects narrative shifts within submolts over a configurable lookback window.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "posts": {
                "type": "array",
                "description": "List of post dicts with keys: author (str), content (str), timestamp (ISO-8601 str), upvotes (int), submolt (str).",
                "items": {"type": "object"},
            },
            "lookback_hours": {
                "type": "integer",
                "description": "How many hours back to include in the analysis window.",
                "default": 24,
            },
        },
        "required": ["posts"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "overall_sentiment": {"type": "number"},
            "by_submolt": {"type": "object"},
            "narrative_shifts": {"type": "array"},
            "trending_topics": {"type": "array"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": ["status", "timestamp"],
    },
}

# --- Lexicons ---
POSITIVE_TERMS: list[str] = [
    "bullish", "surge", "rally", "breakout", "upside", "growth", "profit",
    "gains", "beat", "outperform", "buy", "long", "moon", "strong", "upgrade",
    "opportunity", "accumulate", "positive", "recover", "rebound",
]
NEGATIVE_TERMS: list[str] = [
    "bearish", "crash", "dump", "correction", "downside", "loss", "miss",
    "underperform", "sell", "short", "rug", "weak", "downgrade", "risk",
    "warning", "decline", "plunge", "collapse", "panic", "recession",
]
INTENSIFIERS: list[str] = ["very", "extremely", "highly", "massive", "major"]
NEGATIONS: list[str] = ["not", "no", "never", "barely", "hardly"]


def _score_text(text: str) -> float:
    """Score a single text string from -1.0 to 1.0 using keyword matching.

    Args:
        text: Raw post content string.

    Returns:
        Sentiment float in [-1.0, 1.0].
    """
    tokens = re.findall(r"\b\w+\b", text.lower())
    score: float = 0.0
    i = 0
    while i < len(tokens):
        token = tokens[i]
        multiplier = 1.5 if (i > 0 and tokens[i - 1] in INTENSIFIERS) else 1.0
        negated = i > 0 and tokens[i - 1] in NEGATIONS
        if token in POSITIVE_TERMS:
            score += multiplier if not negated else -multiplier
        elif token in NEGATIVE_TERMS:
            score -= multiplier if not negated else -multiplier
        i += 1
    # Normalize to [-1, 1] with a soft clamp
    if score == 0:
        return 0.0
    return max(-1.0, min(1.0, score / max(len(tokens) ** 0.5, 1)))


def _extract_topics(posts: list[dict]) -> list[str]:
    """Extract trending topics via simple token frequency.

    Args:
        posts: Filtered post dicts.

    Returns:
        Top 10 unique tokens (stopwords excluded) sorted by frequency.
    """
    stopwords = {
        "the", "a", "an", "is", "it", "in", "on", "at", "to", "for",
        "of", "and", "or", "but", "this", "that", "with", "from", "by",
        "be", "are", "was", "were", "have", "has", "had", "i", "we",
        "they", "he", "she", "its", "our", "my", "your", "their",
    }
    freq: dict[str, int] = defaultdict(int)
    for post in posts:
        tokens = re.findall(r"\b[a-z]{3,}\b", post.get("content", "").lower())
        for tok in tokens:
            if tok not in stopwords:
                freq[tok] += 1
    sorted_topics = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [t for t, _ in sorted_topics[:10]]


def _detect_shifts(
    submolt: str,
    window_scores: list[float],
    current_score: float,
) -> dict[str, Any] | None:
    """Check if current_score deviates more than 1 stddev from the window mean.

    Args:
        submolt: Name of the submolt being checked.
        window_scores: Historical sentiment scores for the submolt.
        current_score: Most recent aggregate score.

    Returns:
        Shift dict if detected, else None.
    """
    if len(window_scores) < 2:
        return None
    mean = sum(window_scores) / len(window_scores)
    variance = sum((s - mean) ** 2 for s in window_scores) / len(window_scores)
    stddev = math.sqrt(variance)
    if stddev == 0:
        return None
    if abs(current_score - mean) > stddev:
        direction = "positive" if current_score > mean else "negative"
        return {
            "submolt": submolt,
            "direction": direction,
            "previous_mean": round(mean, 4),
            "current_score": round(current_score, 4),
            "stddev": round(stddev, 4),
            "z_score": round((current_score - mean) / stddev, 4),
        }
    return None


def moltbook_sentiment_analyzer(
    posts: list[dict],
    lookback_hours: int = 24,
    **kwargs: Any,
) -> dict:
    """Analyze Moltbook posts for financial sentiment and narrative shifts.

    Args:
        posts: List of post dicts. Each must contain: author (str),
            content (str), timestamp (ISO-8601 str), upvotes (int),
            submolt (str).
        lookback_hours: Number of hours of history to include. Defaults to 24.
        **kwargs: Ignored extra keyword arguments.

    Returns:
        Dict with keys:
            status (str): "success" or "error".
            overall_sentiment (float): Upvote-weighted mean score across all posts.
            by_submolt (dict): Per-submolt sentiment and post count.
            narrative_shifts (list): Submolts whose sentiment shifted > 1 stddev.
            trending_topics (list): Top 10 terms by frequency.
            timestamp (str): ISO-8601 UTC timestamp.
    """
    try:
        cutoff = datetime.now(timezone.utc) - timedelta(hours=lookback_hours)

        filtered: list[dict] = []
        for post in posts:
            try:
                ts = datetime.fromisoformat(post["timestamp"].replace("Z", "+00:00"))
                if ts.tzinfo is None:
                    ts = ts.replace(tzinfo=timezone.utc)
                if ts >= cutoff:
                    filtered.append(post)
            except (KeyError, ValueError):
                # Skip malformed posts
                continue

        if not filtered:
            return {
                "status": "success",
                "overall_sentiment": 0.0,
                "by_submolt": {},
                "narrative_shifts": [],
                "trending_topics": [],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # Score every post
        scored: list[dict] = []
        for post in filtered:
            score = _score_text(post.get("content", ""))
            scored.append({**post, "_sentiment": score})

        # Aggregate by submolt
        submolt_buckets: dict[str, list[dict]] = defaultdict(list)
        for post in scored:
            submolt_buckets[post.get("submolt", "unknown")].append(post)

        by_submolt: dict[str, Any] = {}
        all_weighted_scores: list[float] = []
        all_weights: list[float] = []

        for sm, sm_posts in submolt_buckets.items():
            total_weight = sum(max(p.get("upvotes", 1), 1) for p in sm_posts)
            weighted_score = sum(
                p["_sentiment"] * max(p.get("upvotes", 1), 1) for p in sm_posts
            ) / total_weight
            raw_scores = [p["_sentiment"] for p in sm_posts]
            by_submolt[sm] = {
                "sentiment": round(weighted_score, 4),
                "post_count": len(sm_posts),
                "raw_scores": [round(s, 4) for s in raw_scores],
            }
            all_weighted_scores.append(weighted_score * total_weight)
            all_weights.append(total_weight)

        overall_sentiment = (
            sum(all_weighted_scores) / sum(all_weights) if all_weights else 0.0
        )

        # Detect narrative shifts using rolling half/half split
        narrative_shifts: list[dict] = []
        for sm, sm_posts in submolt_buckets.items():
            scores_sorted = [
                p["_sentiment"]
                for p in sorted(sm_posts, key=lambda x: x.get("timestamp", ""))
            ]
            if len(scores_sorted) >= 4:
                midpoint = len(scores_sorted) // 2
                historical = scores_sorted[:midpoint]
                current_batch = scores_sorted[midpoint:]
                current_score = sum(current_batch) / len(current_batch)
                shift = _detect_shifts(sm, historical, current_score)
                if shift:
                    narrative_shifts.append(shift)

        trending_topics = _extract_topics(filtered)

        return {
            "status": "success",
            "overall_sentiment": round(overall_sentiment, 4),
            "by_submolt": by_submolt,
            "narrative_shifts": narrative_shifts,
            "trending_topics": trending_topics,
            "post_count_analyzed": len(filtered),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"moltbook_sentiment_analyzer failed: {e}")
        _log_lesson(f"moltbook_sentiment_analyzer: {e}")
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
