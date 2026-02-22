"""Evaluate price alert triggers for Snowdrop agents."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "price_alert_evaluator",
    "description": "Checks price conditions (above, below, pct_change) and prioritizes alerts.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "alerts": {
                "type": "array",
                "items": {"type": "object"},
            }
        },
        "required": ["alerts"],
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


def price_alert_evaluator(alerts: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Evaluate price alerts and categorize triggered ones."""
    try:
        if not isinstance(alerts, list):
            raise ValueError("alerts must be a list")

        triggered: list[dict[str, Any]] = []
        not_triggered: list[dict[str, Any]] = []

        for alert in alerts:
            if not isinstance(alert, dict):
                raise ValueError("each alert must be a dict")
            asset = str(alert.get("asset", "unknown"))
            condition = str(alert.get("condition", "above")).lower()
            threshold = float(alert.get("threshold"))
            current_price = float(alert.get("current_price"))
            reference = alert.get("reference_price")

            met, delta_pct = _check_condition(condition, current_price, threshold, reference)
            if met:
                priority = _priority_from_delta(delta_pct)
                triggered.append(
                    {
                        "asset": asset,
                        "condition": condition,
                        "current_price": current_price,
                        "threshold": threshold,
                        "delta_pct": round(delta_pct, 2) if delta_pct is not None else None,
                        "priority": priority,
                    }
                )
            else:
                not_triggered.append({"asset": asset, "condition": condition})

        result = {
            "triggered": triggered,
            "not_triggered": not_triggered,
            "triggered_count": len(triggered),
        }
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("price_alert_evaluator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _check_condition(
    condition: str,
    current_price: float,
    threshold: float,
    reference: Any,
) -> tuple[bool, float | None]:
    if condition == "above":
        return current_price >= threshold, ((current_price / threshold) - 1) * 100 if threshold else None
    if condition == "below":
        return current_price <= threshold, ((threshold / current_price) - 1) * 100 if current_price else None
    if condition == "pct_change":
        if reference is None:
            raise ValueError("reference_price required for pct_change alerts")
        reference_val = float(reference)
        if reference_val == 0:
            raise ValueError("reference_price cannot be zero")
        change_pct = ((current_price - reference_val) / reference_val) * 100
        return abs(change_pct) >= threshold, change_pct
    raise ValueError(f"Unsupported condition: {condition}")


def _priority_from_delta(delta: float | None) -> str:
    if delta is None:
        return "normal"
    if abs(delta) >= 15:
        return "urgent"
    if abs(delta) >= 5:
        return "high"
    return "normal"


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
