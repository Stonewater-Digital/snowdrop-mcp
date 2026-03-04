"""Calculate ROI from community contributions."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from skills.utils import _log_lesson

TOOL_META: dict[str, Any] = {
    "name": "crowd_roi_calculator",
    "description": "Measures value created by community contributions versus review cost.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "community_contributions": {"type": "array", "items": {"type": "object"}},
            "token_price_per_mtok": {"type": "number", "default": 3.0},
        },
        "required": ["community_contributions"],
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


def crowd_roi_calculator(
    community_contributions: list[dict[str, Any]],
    token_price_per_mtok: float = 3.0,
    **_: Any,
) -> dict[str, Any]:
    """Return ROI metrics for Snowdrop community contributions."""

    try:
        totals = {
            "value": 0.0,
            "review": 0.0,
        }
        best: dict[str, Any] | None = None
        for contrib in community_contributions:
            replacement_tokens = contrib.get("estimated_replacement_cost_tokens", 0)
            review_tokens = contrib.get("review_cost_tokens", 0)
            quality = contrib.get("quality_score", 1)
            value_usd = replacement_tokens / 1000 * token_price_per_mtok * quality
            review_usd = review_tokens / 1000 * token_price_per_mtok
            totals["value"] += value_usd
            totals["review"] += review_usd
            roi = (value_usd - review_usd) / review_usd if review_usd else float("inf")
            if best is None or roi > best["roi"]:
                best = {"skill_name": contrib.get("skill_name"), "roi": roi}
        net_value = totals["value"] - totals["review"]
        roi_pct = (net_value / totals["review"] * 100) if totals["review"] else float("inf")
        data = {
            "total_value_contributed_usd": round(totals["value"], 2),
            "total_review_cost_usd": round(totals["review"], 2),
            "net_value_gained_usd": round(net_value, 2),
            "roi_pct": round(roi_pct, 2) if roi_pct != float("inf") else float("inf"),
            "best_contributor_roi": best,
            "avg_review_cost_per_skill": (
                round(totals["review"] / len(community_contributions), 2)
                if community_contributions
                else 0.0
            ),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("crowd_roi_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
