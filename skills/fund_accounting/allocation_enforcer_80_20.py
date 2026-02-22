"""Checks the Boring/Thunder allocation and drafts rebalancing orders."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "allocation_enforcer_80_20",
    "description": "Ensures the Snowdrop portfolio stays within the 80/20 ±5% guardrails.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "positions": {
                "type": "array",
                "items": {"type": "object"},
                "description": "Portfolio positions with name/value/category fields.",
            },
            "overrides": {
                "type": "object",
                "description": "Optional asset→category overrides.",
            },
        },
        "required": ["positions"],
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


def allocation_enforcer_80_20(
    positions: list[dict[str, Any]], overrides: dict[str, str] | None = None, **_: Any
) -> dict[str, Any]:
    """Report allocation mix and propose pending Thunder approvals when drift occurs.

    Args:
        positions: Portfolio holdings including names, values, and optional categories.
        overrides: Manual asset bucket mapping when heuristics are insufficient.

    Returns:
        Envelope summarizing bucket percentages alongside any draft transfer orders.
    """

    try:
        overrides = overrides or {}
        boring_value = 0.0
        thunder_value = 0.0
        classified_positions: list[dict[str, Any]] = []

        for position in positions:
            value = float(position.get("value", 0) or 0)
            asset = position.get("name") or position.get("symbol") or "unknown"
            bucket = overrides.get(asset) or _categorize(position)
            bucket_lower = bucket.lower()
            if bucket_lower == "thunder":
                thunder_value += value
            else:
                boring_value += value
            classified_positions.append({"asset": asset, "value": value, "bucket": bucket_lower})

        total = boring_value + thunder_value
        if total <= 0:
            raise ValueError("Portfolio total must be positive")

        boring_pct = boring_value / total * 100
        thunder_pct = thunder_value / total * 100

        actions = []
        if boring_pct < 75:
            shortfall = total * 0.80 - boring_value
            actions.append(
                {
                    "type": "transfer",
                    "from": "thunder",
                    "to": "boring",
                    "amount": round(shortfall, 2),
                    "status": "pending_thunder_approval",
                }
            )
        elif boring_pct > 85:
            excess = boring_value - total * 0.80
            actions.append(
                {
                    "type": "transfer",
                    "from": "boring",
                    "to": "thunder",
                    "amount": round(excess, 2),
                    "status": "pending_thunder_approval",
                }
            )

        data = {
            "boring_value": round(boring_value, 2),
            "thunder_value": round(thunder_value, 2),
            "boring_pct": round(boring_pct, 2),
            "thunder_pct": round(thunder_pct, 2),
            "positions": classified_positions,
            "actions": actions,
        }

        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("allocation_enforcer_80_20", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _categorize(position: dict[str, Any]) -> str:
    hint = (position.get("category") or position.get("risk_profile") or "boring").lower()
    if any(word in hint for word in ("venture", "degen", "high", "growth", "ton")):
        return "thunder"
    return "boring"


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
