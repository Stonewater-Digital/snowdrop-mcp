"""Compute Altman Z-Scores for bankruptcy risk analysis."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "altman_z_score",
    "description": "Calculates Altman Z, identifies zone, and estimates distress probability.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "working_capital": {"type": "number"},
            "total_assets": {"type": "number"},
            "retained_earnings": {"type": "number"},
            "ebit": {"type": "number"},
            "market_cap": {"type": "number"},
            "total_liabilities": {"type": "number"},
            "revenue": {"type": "number"},
            "model": {
                "type": "string",
                "enum": ["original", "private", "emerging"],
                "default": "original",
            },
        },
        "required": [
            "working_capital",
            "total_assets",
            "retained_earnings",
            "ebit",
            "market_cap",
            "total_liabilities",
            "revenue",
        ],
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


def altman_z_score(
    working_capital: float,
    total_assets: float,
    retained_earnings: float,
    ebit: float,
    market_cap: float,
    total_liabilities: float,
    revenue: float,
    model: str = "original",
    **_: Any,
) -> dict[str, Any]:
    """Return Altman Z components and risk classification."""
    try:
        if total_assets <= 0 or total_liabilities <= 0:
            raise ValueError("Assets and liabilities must be positive")
        book_equity = max(total_assets - total_liabilities, 0)
        factors = {
            "original": (1.2, 1.4, 3.3, 0.6, 1.0),
            "private": (0.717, 0.847, 3.107, 0.420, 0.998),
            "emerging": (3.25, 6.56, 6.72, 4.03, 1.0),
        }
        a, b, c, d, e = factors[model]
        x1 = working_capital / total_assets
        x2 = retained_earnings / total_assets
        x3 = ebit / total_assets
        x4 = (market_cap if model != "private" else book_equity) / total_liabilities
        x5 = revenue / total_assets
        z = a * x1 + b * x2 + c * x3 + d * x4 + e * x5
        if z > 2.99:
            zone = "safe"
            bankruptcy_probability = "<5%"
        elif z >= 1.81:
            zone = "grey"
            bankruptcy_probability = "5-20%"
        else:
            zone = "distress"
            bankruptcy_probability = ">20%"
        data = {
            "z_score": round(z, 3),
            "zone": zone,
            "components": {"x1": x1, "x2": x2, "x3": x3, "x4": x4, "x5": x5},
            "bankruptcy_probability": bankruptcy_probability,
            "model_used": model,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("altman_z_score", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
