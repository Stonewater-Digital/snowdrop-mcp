"""Distribute marketplace revenue between Snowdrop and contributors."""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any

LOG_PATH = "logs/skill_royalties.jsonl"

TOOL_META: dict[str, Any] = {
    "name": "skill_royalty_splitter",
    "description": "Calculates revenue splits for community skills and tracks contributor balances.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "skill_name": {"type": "string"},
            "revenue": {"type": "number"},
            "contributor_id": {"type": "string"},
            "platform_rate_pct": {"type": "number", "default": 30.0},
        },
        "required": ["skill_name", "revenue", "contributor_id"],
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


def skill_royalty_splitter(
    skill_name: str,
    revenue: float,
    contributor_id: str,
    platform_rate_pct: float = 30.0,
    **_: Any,
) -> dict[str, Any]:
    """Split revenue between platform and contributor."""
    try:
        if revenue < 0:
            raise ValueError("revenue cannot be negative")
        platform_share = revenue * (platform_rate_pct / 100)
        contributor_share = revenue - platform_share
        cumulative = _get_cumulative(contributor_id) + contributor_share
        record = {
            "skill_name": skill_name,
            "revenue": revenue,
            "contributor_id": contributor_id,
            "platform_rate_pct": platform_rate_pct,
            "platform_share": round(platform_share, 2),
            "contributor_share": round(contributor_share, 2),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        _append_jsonl(LOG_PATH, record)
        payout_threshold_met = cumulative >= 25
        data = {
            "contributor_share": round(contributor_share, 2),
            "platform_share": round(platform_share, 2),
            "contributor_cumulative": round(cumulative, 2),
            "payout_threshold_met": payout_threshold_met,
            "execution": "pending_thunder_approval",
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": record["created_at"],
        }
    except Exception as exc:
        _log_lesson("skill_royalty_splitter", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _get_cumulative(contributor_id: str) -> float:
    if not os.path.exists(LOG_PATH):
        return 0.0
    total = 0.0
    with open(LOG_PATH, "r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            payload = json.loads(line)
            if payload.get("contributor_id") == contributor_id:
                total += float(payload.get("contributor_share", 0))
    return total


def _append_jsonl(path: str, payload: dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload) + "\n")


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
