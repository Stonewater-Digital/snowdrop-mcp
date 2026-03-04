"""Apply macro shocks to compute portfolio return impact."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping

TOOL_META: dict[str, Any] = {
    "name": "macro_scenario_builder",
    "description": "Applies macro factor shocks to exposures to estimate scenario returns.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "factor_exposures": {
                "type": "object",
                "additionalProperties": {"type": "number"},
            },
            "factor_shocks": {
                "type": "object",
                "additionalProperties": {"type": "number"},
            },
            "base_return_pct": {"type": "number", "default": 0.0},
        },
        "required": ["factor_exposures", "factor_shocks"],
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


def macro_scenario_builder(
    factor_exposures: Mapping[str, float],
    factor_shocks: Mapping[str, float],
    base_return_pct: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Return contribution by factor and total scenario P&L."""
    try:
        if not factor_exposures or not factor_shocks:
            raise ValueError("factor_exposures and factor_shocks cannot be empty")
        contributions = []
        total = base_return_pct
        for factor, beta in factor_exposures.items():
            shock = factor_shocks.get(factor, 0.0)
            impact = beta * shock
            total += impact
            contributions.append({"factor": factor, "shock": shock, "impact_pct": round(impact, 3)})
        data = {
            "contributions": contributions,
            "base_return_pct": base_return_pct,
            "scenario_return_pct": round(total, 3),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        _log_lesson(f"macro_scenario_builder: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
