"""Compute portfolio beta versus benchmark."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "portfolio_beta_calculator",
    "description": "Calculates weighted average beta from constituent betas and weights.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "positions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "weight": {"type": "number"},
                        "beta": {"type": "number"},
                    },
                    "required": ["name", "weight", "beta"],
                },
            }
        },
        "required": ["positions"],
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def portfolio_beta_calculator(positions: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return weighted beta."""
    try:
        beta = sum(item.get("weight", 0.0) * item.get("beta", 0.0) for item in positions)
        data = {
            "portfolio_beta": round(beta, 3),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("portfolio_beta_calculator", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
