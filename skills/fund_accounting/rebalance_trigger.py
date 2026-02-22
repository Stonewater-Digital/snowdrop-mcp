"""Monitor the Boring/Thunder split and recommend adjustments."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "rebalance_trigger",
    "description": "Checks portfolio split vs. target bands and surfaces recommended skims or reviews.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "boring_value": {"type": "number", "description": "Safe asset value."},
            "thunder_value": {
                "type": "number",
                "description": "High-conviction asset value.",
            },
        },
        "required": ["boring_value", "thunder_value"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string", "format": "date-time"},
        },
    },
}


def rebalance_trigger(boring_value: float, thunder_value: float, **_: Any) -> dict[str, Any]:
    """Assess the 80/20 allocation and recommend next steps.

    Args:
        boring_value: Total USD value of safe/yield assets.
        thunder_value: Total USD value of high-conviction assets.

    Returns:
        Envelope detailing allocation percentages and any pending rebalance orders.
    """

    try:
        total = boring_value + thunder_value
        if total <= 0:
            raise ValueError("Combined portfolio value must be positive")

        thunder_pct = thunder_value / total * 100
        boring_pct = boring_value / total * 100

        recommendation = "hold"
        orders: list[dict[str, Any]] = []

        if thunder_pct > 25:
            excess = thunder_value - total * 0.20
            recommendation = "skim_to_boring"
            orders.append(
                {
                    "action": "transfer",
                    "from": "thunder",
                    "to": "boring",
                    "amount": round(excess, 2),
                    "status": "pending_thunder_approval",
                }
            )
        elif thunder_pct < 15:
            deficit = total * 0.20 - thunder_value
            recommendation = "thesis_review"
            orders.append(
                {
                    "action": "review",
                    "focus": "thunder pipeline",
                    "notes": f"Allocate ${round(deficit, 2)} once thesis confirmed",
                    "status": "pending_thunder_approval",
                }
            )

        data = {
            "allocation": {
                "boring_pct": round(boring_pct, 2),
                "thunder_pct": round(thunder_pct, 2),
                "boring_value": round(boring_value, 2),
                "thunder_value": round(thunder_value, 2),
            },
            "recommendation": recommendation,
            "orders": orders,
        }

        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("rebalance_trigger", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
