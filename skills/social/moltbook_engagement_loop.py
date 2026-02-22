"""
Executive Summary: Moltbook "Agent Front Page" optimizer — analyzes historical post performance to recommend optimal posting times, content mix, and cadence for maximum engagement.
Inputs: content_history (list[dict: post_id, content_type, posting_time_utc, engagement_score, submolt]), target_submolt (str, optional)
Outputs: optimal_times_utc (list), best_content_types (list sorted by avg engagement), recommended_frequency (str), engagement_forecast (float)
MCP Tool Name: moltbook_engagement_loop
"""
import logging
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "moltbook_engagement_loop",
    "description": "Analyzes Moltbook post history to determine optimal posting times (UTC), best-performing content types, recommended posting frequency, and forecasts expected engagement for the next post.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "content_history": {
                "type": "array",
                "description": (
                    "List of post dicts with: post_id (str), content_type (str), "
                    "posting_time_utc (ISO-8601 str), engagement_score (float), "
                    "submolt (str)."
                ),
                "items": {"type": "object"},
            },
            "target_submolt": {
                "type": "string",
                "description": "Optional: filter analysis to a specific submolt.",
            },
        },
        "required": ["content_history"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "optimal_times_utc": {"type": "array"},
            "best_content_types": {"type": "array"},
            "recommended_frequency": {"type": "string"},
            "engagement_forecast": {"type": "number"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": ["status", "timestamp"],
    },
}

# Hour blocks for time-of-day analysis
HOUR_BLOCK_LABELS: dict[str, list[int]] = {
    "early_morning_00-06": list(range(0, 6)),
    "morning_06-10": list(range(6, 10)),
    "mid_morning_10-12": list(range(10, 12)),
    "lunch_12-14": list(range(12, 14)),
    "afternoon_14-17": list(range(14, 17)),
    "evening_17-20": list(range(17, 20)),
    "night_20-24": list(range(20, 24)),
}

# Minimum posts required for a time slot to be considered statistically meaningful
MIN_POSTS_PER_SLOT = 2


def _parse_utc_hour(posting_time_utc: str) -> int | None:
    """Extract the UTC hour (0-23) from an ISO-8601 timestamp string.

    Args:
        posting_time_utc: ISO-8601 datetime string.

    Returns:
        UTC hour integer 0-23, or None if parsing fails.
    """
    try:
        dt = datetime.fromisoformat(posting_time_utc.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.hour
    except (ValueError, AttributeError):
        return None


def _hour_to_block(hour: int) -> str:
    """Map an hour 0-23 to its time block label.

    Args:
        hour: UTC hour integer.

    Returns:
        Block label string.
    """
    for label, hours in HOUR_BLOCK_LABELS.items():
        if hour in hours:
            return label
    return "unknown"


def _recommend_frequency(post_count: int, day_span: float) -> str:
    """Determine recommended posting frequency from history stats.

    Args:
        post_count: Total number of posts in the history.
        day_span: Number of days the history covers.

    Returns:
        Human-readable frequency recommendation string.
    """
    if day_span <= 0 or post_count == 0:
        return "1x per day (default — insufficient history)"
    rate = post_count / day_span  # posts per day
    if rate >= 5:
        return f"{round(rate)}x per day (maintain current cadence)"
    if rate >= 3:
        return f"{round(rate)}x per day"
    if rate >= 1:
        return "1-2x per day (consider increasing to 3x for Front Page reach)"
    return "less than daily (increase to at least 1x per day)"


def _forecast_engagement(
    best_content_types: list[dict],
    optimal_hour_avg: float,
    overall_avg: float,
) -> float:
    """Estimate engagement score for the next optimally-timed post.

    Simple model: take the best content type's average, boost by the
    ratio of optimal-hour mean to overall mean.

    Args:
        best_content_types: Sorted list of content type performance dicts.
        optimal_hour_avg: Average engagement in the best time slot.
        overall_avg: Overall average engagement across all posts.

    Returns:
        Forecast engagement score float.
    """
    if not best_content_types:
        return overall_avg
    best_avg = best_content_types[0].get("avg_engagement", overall_avg)
    boost = (optimal_hour_avg / overall_avg) if overall_avg > 0 else 1.0
    forecast = best_avg * boost
    return round(min(forecast, 100.0), 4)


def moltbook_engagement_loop(
    content_history: list[dict],
    target_submolt: str | None = None,
    **kwargs: Any,
) -> dict:
    """Analyze Moltbook post history to optimize the engagement loop.

    Workflow:
        1. Optionally filter by target_submolt.
        2. Parse posting_time_utc to extract UTC hour for each post.
        3. Bucket posts by time block; compute average engagement per block.
        4. Rank content types by average engagement score.
        5. Determine posting frequency from history cadence.
        6. Forecast next-post engagement using best type + optimal time.

    Args:
        content_history: List of post dicts, each with:
            post_id (str): Unique post identifier.
            content_type (str): Post category (e.g., "analysis", "chart", "meme").
            posting_time_utc (str): ISO-8601 UTC timestamp of when posted.
            engagement_score (float): Numeric engagement metric (e.g., 0-100).
            submolt (str): Moltbook community the post was made in.
        target_submolt: If provided, restrict analysis to this submolt only.
        **kwargs: Ignored extra keyword arguments.

    Returns:
        Dict with keys:
            status (str): "success" or "error".
            optimal_times_utc (list[dict]): Time blocks sorted by avg engagement.
            best_content_types (list[dict]): Content types sorted by avg engagement.
            recommended_frequency (str): Human-readable posting cadence suggestion.
            engagement_forecast (float): Predicted score for next optimal post.
            analyzed_post_count (int): Posts included in analysis.
            submolt_filter (str | None): Echoed target_submolt filter.
            timestamp (str): ISO-8601 UTC timestamp.
    """
    try:
        # Step 1: Optional submolt filter
        if target_submolt:
            history = [
                p for p in content_history
                if p.get("submolt", "").lower() == target_submolt.lower()
            ]
        else:
            history = list(content_history)

        if not history:
            return {
                "status": "success",
                "optimal_times_utc": [],
                "best_content_types": [],
                "recommended_frequency": "no history available",
                "engagement_forecast": 0.0,
                "analyzed_post_count": 0,
                "submolt_filter": target_submolt,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # Parse and score each post
        parsed: list[dict] = []
        timestamps_seen: list[datetime] = []
        for post in history:
            hour = _parse_utc_hour(post.get("posting_time_utc", ""))
            if hour is None:
                continue
            try:
                score = float(post.get("engagement_score", 0.0))
            except (TypeError, ValueError):
                score = 0.0
            block = _hour_to_block(hour)
            parsed.append({
                **post,
                "_hour": hour,
                "_block": block,
                "_score": score,
            })
            try:
                dt = datetime.fromisoformat(
                    post["posting_time_utc"].replace("Z", "+00:00")
                )
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                timestamps_seen.append(dt)
            except (KeyError, ValueError):
                pass

        if not parsed:
            return {
                "status": "success",
                "optimal_times_utc": [],
                "best_content_types": [],
                "recommended_frequency": "insufficient_parseable_history",
                "engagement_forecast": 0.0,
                "analyzed_post_count": 0,
                "submolt_filter": target_submolt,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        overall_avg = sum(p["_score"] for p in parsed) / len(parsed)

        # Step 3: Time block analysis
        block_scores: dict[str, list[float]] = defaultdict(list)
        for p in parsed:
            block_scores[p["_block"]].append(p["_score"])

        optimal_times: list[dict] = []
        for block, scores in block_scores.items():
            if len(scores) < MIN_POSTS_PER_SLOT:
                continue
            avg = sum(scores) / len(scores)
            # Map block back to representative UTC hours
            hours_in_block = HOUR_BLOCK_LABELS.get(block, [])
            optimal_times.append({
                "time_block": block,
                "representative_hours_utc": hours_in_block,
                "avg_engagement": round(avg, 4),
                "post_count": len(scores),
            })

        optimal_times.sort(key=lambda x: x["avg_engagement"], reverse=True)

        # Best time slot avg for forecast
        optimal_hour_avg = optimal_times[0]["avg_engagement"] if optimal_times else overall_avg

        # Step 4: Content type analysis
        type_scores: dict[str, list[float]] = defaultdict(list)
        for p in parsed:
            ct = p.get("content_type", "unknown")
            type_scores[ct].append(p["_score"])

        best_content_types: list[dict] = []
        for ct, scores in type_scores.items():
            avg = sum(scores) / len(scores)
            best_content_types.append({
                "content_type": ct,
                "avg_engagement": round(avg, 4),
                "post_count": len(scores),
            })
        best_content_types.sort(key=lambda x: x["avg_engagement"], reverse=True)

        # Step 5: Frequency recommendation
        if len(timestamps_seen) >= 2:
            earliest = min(timestamps_seen)
            latest = max(timestamps_seen)
            day_span = max((latest - earliest).total_seconds() / 86400, 1)
        else:
            day_span = 1.0
        freq = _recommend_frequency(len(parsed), day_span)

        # Step 6: Engagement forecast
        forecast = _forecast_engagement(best_content_types, optimal_hour_avg, overall_avg)

        return {
            "status": "success",
            "optimal_times_utc": optimal_times,
            "best_content_types": best_content_types,
            "recommended_frequency": freq,
            "engagement_forecast": forecast,
            "overall_avg_engagement": round(overall_avg, 4),
            "analyzed_post_count": len(parsed),
            "submolt_filter": target_submolt,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"moltbook_engagement_loop failed: {e}")
        _log_lesson(f"moltbook_engagement_loop: {e}")
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
