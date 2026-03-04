"""Check borrower, sector, and geography concentration."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "portfolio_concentration_checker",
    "description": "Flags concentration exposures versus policy limits.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "borrower_exposure": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {"name": {"type": "string"}, "exposure_pct": {"type": "number"}},
                    "required": ["name", "exposure_pct"],
                },
            },
            "sector_exposure": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {"name": {"type": "string"}, "exposure_pct": {"type": "number"}},
                    "required": ["name", "exposure_pct"],
                },
            },
            "geography_exposure": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {"name": {"type": "string"}, "exposure_pct": {"type": "number"}},
                    "required": ["name", "exposure_pct"],
                },
            },
            "borrower_limit_pct": {"type": "number", "default": 10.0},
            "sector_limit_pct": {"type": "number", "default": 25.0},
            "geography_limit_pct": {"type": "number", "default": 30.0},
        },
        "required": ["borrower_exposure", "sector_exposure", "geography_exposure"],
    },
    "outputSchema": {"type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def portfolio_concentration_checker(
    borrower_exposure: list[dict[str, Any]],
    sector_exposure: list[dict[str, Any]],
    geography_exposure: list[dict[str, Any]],
    borrower_limit_pct: float = 10.0,
    sector_limit_pct: float = 25.0,
    geography_limit_pct: float = 30.0,
    **_: Any,
) -> dict[str, Any]:
    """Return breach flags by category."""
    try:
        def breaches(exposures: list[dict[str, Any]], limit: float) -> list[dict[str, Any]]:
            return [
                {"name": exp.get("name", "unknown"), "exposure_pct": exp.get("exposure_pct", 0.0)}
                for exp in exposures
                if exp.get("exposure_pct", 0.0) > limit
            ]

        borrower_breaches = breaches(borrower_exposure, borrower_limit_pct)
        sector_breaches = breaches(sector_exposure, sector_limit_pct)
        geo_breaches = breaches(geography_exposure, geography_limit_pct)
        data = {
            "borrower_breaches": borrower_breaches,
            "sector_breaches": sector_breaches,
            "geography_breaches": geo_breaches,
            "hhi_borrower": round(sum((exp.get("exposure_pct", 0.0) / 100) ** 2 for exp in borrower_exposure), 4),
            "hhi_sector": round(sum((exp.get("exposure_pct", 0.0) / 100) ** 2 for exp in sector_exposure), 4),
            "hhi_geography": round(sum((exp.get("exposure_pct", 0.0) / 100) ** 2 for exp in geography_exposure), 4),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("portfolio_concentration_checker", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
