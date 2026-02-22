"""Draft LP-ready investor communication."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "investor_letter_drafter",
    "description": "Builds executive-ready investor letter sections.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "period": {"type": "string"},
            "fund_performance": {"type": "object"},
            "market_commentary": {"type": "string"},
            "outlook": {"type": "string"},
            "key_decisions": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
        "required": [
            "period",
            "fund_performance",
            "market_commentary",
            "outlook",
            "key_decisions",
        ],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "letter": {"type": "object"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def investor_letter_drafter(
    period: str,
    fund_performance: dict[str, Any],
    market_commentary: str,
    outlook: str,
    key_decisions: list[str],
    **_: Any,
) -> dict[str, Any]:
    """Return letter sections for Thunder review."""

    try:
        sections = [
            {
                "title": f"Performance {period}",
                "content": _format_performance(fund_performance),
            },
            {
                "title": "Market Commentary",
                "content": market_commentary,
            },
            {
                "title": "Outlook",
                "content": outlook,
            },
            {
                "title": "Decisions Requested",
                "content": "\n".join(f"- {item}" for item in key_decisions) or "- None",
            },
        ]
        letter = {"period": period, "sections": sections, "status": "pending_thunder_approval"}
        return {
            "status": "success",
            "data": {"letter": letter},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("investor_letter_drafter", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _format_performance(perf: dict[str, Any]) -> str:
    bullets = []
    for key, value in perf.items():
        bullets.append(f"- {key}: {value}")
    return "\n".join(bullets)


def _log_lesson(skill_name: str, error: str) -> None:
    """Append a Ralph Wiggum lesson entry."""

    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
