"""Calculate net counterparty exposures with collateral offsets."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "counterparty_exposure_calculator",
    "description": "Aggregates MTM by counterparty, applies collateral, and flags threshold breaches.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "positions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "counterparty": {"type": "string"},
                        "mtm": {"type": "number"},
                        "collateral": {"type": "number", "default": 0.0},
                        "threshold": {"type": "number", "default": 0.0},
                    },
                    "required": ["counterparty", "mtm"],
                },
            }
        },
        "required": ["positions"],
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def counterparty_exposure_calculator(positions: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return net exposure by counterparty."""
    try:
        exposure_map: dict[str, float] = {}
        thresholds: dict[str, float] = {}
        for pos in positions:
            cpty = pos.get("counterparty", "unknown")
            exposure_map[cpty] = exposure_map.get(cpty, 0.0) + pos.get("mtm", 0.0) - pos.get("collateral", 0.0)
            thresholds[cpty] = pos.get("threshold", thresholds.get(cpty, 0.0))
        summary = []
        for cpty, exposure in exposure_map.items():
            threshold = thresholds.get(cpty, 0.0)
            summary.append(
                {
                    "counterparty": cpty,
                    "net_exposure": round(exposure, 2),
                    "threshold": threshold,
                    "breach": exposure > threshold,
                }
            )
        data = {"counterparties": summary}
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("counterparty_exposure_calculator", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
