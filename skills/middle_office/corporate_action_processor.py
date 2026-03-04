"""Process equity corporate action adjustments."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "corporate_action_processor",
    "description": "Adjusts position quantities and cash for announced corporate actions.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "position_quantity": {"type": "number"},
            "action_type": {
                "type": "string",
                "enum": ["split", "reverse_split", "spinoff", "merger"],
            },
            "ratio": {"type": "number"},
            "cash_component": {"type": "number", "default": 0.0},
        },
        "required": ["position_quantity", "action_type", "ratio"],
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


def corporate_action_processor(
    position_quantity: float,
    action_type: str,
    ratio: float,
    cash_component: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Return adjusted quantities and proceeds for common action types."""
    try:
        if ratio <= 0:
            raise ValueError("ratio must be positive")
        adjusted_quantity = position_quantity
        adjustment_factor = 1.0
        cash_proceeds = cash_component
        action_type = action_type.lower()
        if action_type == "split":
            adjustment_factor = ratio
        elif action_type == "reverse_split":
            adjustment_factor = 1 / ratio
        elif action_type == "spinoff":
            adjustment_factor = 1.0
            cash_proceeds += position_quantity * cash_component
        elif action_type == "merger":
            adjustment_factor = ratio
            cash_proceeds += position_quantity * cash_component
        else:
            raise ValueError(f"unsupported action_type {action_type}")
        adjusted_quantity = position_quantity * adjustment_factor
        data = {
            "action_type": action_type,
            "adjusted_quantity": round(adjusted_quantity, 6),
            "adjustment_factor": round(adjustment_factor, 6),
            "cash_proceeds": round(cash_proceeds, 6),
        }
        return {"status": "ok", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        try:
            with open("logs/lessons.md", "a") as _f:
                _f.write(f"- [{datetime.now(timezone.utc).isoformat()}] corporate_action_processor: {exc}\n")
        except OSError:
            pass
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
