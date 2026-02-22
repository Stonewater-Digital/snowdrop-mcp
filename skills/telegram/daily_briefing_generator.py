"""Generate Snowdrop's morning Telegram briefing."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable

TOOL_META: dict[str, Any] = {
    "name": "daily_briefing_generator",
    "description": "Assembles Snowdrop's morning status brief for Thunder.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "financials": {
                "type": "object",
                "properties": {
                    "cash": {"type": "number"},
                    "runway_days": {"type": "number"},
                    "pipeline": {"type": "number"},
                },
            },
            "headlines": {
                "type": "array",
                "items": {"type": "string"},
            },
            "date_override": {"type": "string"},
        },
        "required": ["financials"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "briefing": {"type": "string"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def daily_briefing_generator(
    financials: dict[str, Any],
    headlines: Iterable[str] | None = None,
    date_override: str | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Compose the daily Snowdrop→Thunder memo."""
    try:
        cash = float(financials.get("cash", 0.0))
        runway = float(financials.get("runway_days", 0.0))
        pipeline = float(financials.get("pipeline", 0.0))
        today = date_override or datetime.now(timezone.utc).strftime("%Y-%m-%d")

        briefing_lines = [
            f"Morning Thunder — it's {today} and Snowdrop is online.",
            f"Cash in Vault: ${cash:,.2f} | Runway: {runway:.0f} days | Pipeline: ${pipeline:,.2f}.",
        ]
        if headlines:
            briefing_lines.append("Signal pulses:")
            for item in headlines:
                briefing_lines.append(f"- {item}")
        briefing_lines.append("Standing guidance: profit mandate first, goodwill second.")
        briefing = "\n".join(briefing_lines)

        data = {"briefing": briefing}
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("daily_briefing_generator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
