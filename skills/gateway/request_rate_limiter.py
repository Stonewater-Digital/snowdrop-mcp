"""Token bucket limiter for Snowdrop agents."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "request_rate_limiter",
    "description": "Enforces per-agent token bucket rate limits and returns retry hints.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "agent_id": {"type": "string"},
            "bucket_state": {"type": "object"},
            "current_time": {"type": "string"},
        },
        "required": ["agent_id", "bucket_state", "current_time"],
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


def request_rate_limiter(
    agent_id: str,
    bucket_state: dict[str, Any],
    current_time: str,
    **_: Any,
) -> dict[str, Any]:
    """Return rate-limit decision and updated bucket."""

    try:
        tokens = float(bucket_state.get("tokens", 0))
        last_refill = bucket_state.get("last_refill")
        max_tokens = float(bucket_state.get("max_tokens", 1))
        refill_rate = float(bucket_state.get("refill_rate_per_sec", 0))
        now = datetime.fromisoformat(current_time)
        last_refill_time = datetime.fromisoformat(last_refill) if last_refill else now
        elapsed = max((now - last_refill_time).total_seconds(), 0)
        tokens = min(max_tokens, tokens + elapsed * refill_rate)
        allowed = tokens >= 1
        retry_after = None
        if allowed:
            tokens -= 1
        elif refill_rate > 0:
            retry_after = round((1 - tokens) / refill_rate, 2)
        updated_bucket = {
            "agent_id": agent_id,
            "tokens": round(tokens, 4),
            "last_refill": now.isoformat(),
            "max_tokens": max_tokens,
            "refill_rate_per_sec": refill_rate,
        }
        data = {
            "allowed": allowed,
            "tokens_remaining": updated_bucket["tokens"],
            "retry_after_sec": retry_after,
            "updated_bucket": updated_bucket,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": now.isoformat(),
        }
    except Exception as exc:
        _log_lesson("request_rate_limiter", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
