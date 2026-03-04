"""Prepare a Grok sentiment analysis request for Twitter/X."""
from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "x_sentiment_grok",
    "description": "Constructs xAI Grok payloads for sentiment queries.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "query": {"type": "string"},
            "timeframe_hours": {"type": "integer"},
        },
        "required": ["query", "timeframe_hours"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
    },
}


def x_sentiment_grok(query: str, timeframe_hours: int, **_: Any) -> dict[str, Any]:
    """Build a Grok request envelope.

    Args:
        query: Search query to hand to Grok (e.g., "TON sentiment").
        timeframe_hours: How far back the search window should go in hours.

    Returns:
        Envelope with the prepared API request marked pending Thunder approval.
    """

    try:
        api_key = os.getenv("XAI_API_KEY")
        if not api_key:
            raise ValueError("XAI_API_KEY missing; see .env.template")

        payload = {
            "endpoint": "https://api.x.ai/v1/grok/sentiment",
            "headers": {"Authorization": "Bearer ***redacted***"},
            "body": {
                "query": query,
                "timeframe_hours": timeframe_hours,
                "priority": "insights",
            },
        }

        data = {
            "prepared_request": payload,
            "submission_status": "pending_thunder_approval",
        }

        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("x_sentiment_grok", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
