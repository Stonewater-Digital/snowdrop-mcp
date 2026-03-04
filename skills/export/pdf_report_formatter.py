"""Structure PDF-ready report documents."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "pdf_report_formatter",
    "description": "Creates a layout-ready dict for PDF renderers (sections, TOC, metadata).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "sections": {"type": "array", "items": {"type": "object"}},
            "author": {"type": "string", "default": "Snowdrop — CFO"},
            "date": {"type": "string"},
        },
        "required": ["title", "sections", "date"],
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


def pdf_report_formatter(
    title: str,
    sections: list[dict[str, Any]],
    date: str,
    author: str = "Snowdrop — CFO",
    **_: Any,
) -> dict[str, Any]:
    """Return structured report specification."""
    try:
        if not sections:
            raise ValueError("sections cannot be empty")
        ordered_sections = [
            {
                "heading": section.get("heading"),
                "content_type": section.get("content_type"),
                "content": section.get("content"),
                "order": idx + 1,
            }
            for idx, section in enumerate(sections)
        ]
        toc = [
            {"heading": section["heading"], "page_estimate": idx + 1}
            for idx, section in enumerate(ordered_sections)
        ]
        payload = {
            "title": title,
            "author": author,
            "date": date,
            "sections": ordered_sections,
            "table_of_contents": toc,
            "layout": {
                "page_size": "A4",
                "margins": {"top": 36, "bottom": 36, "left": 36, "right": 36},
                "font": "Inter",
            },
        }
        return {
            "status": "success",
            "data": payload,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("pdf_report_formatter", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
