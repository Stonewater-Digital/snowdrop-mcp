"""Read Ghost Ledger activity from Google Sheets."""
from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

import gspread

TOOL_META: dict[str, Any] = {
    "name": "ghost_ledger_sheets_reader",
    "description": (
        "Loads Ghost Ledger rows from Google Sheets for the requested notebook section and"
        " filters them to a date range."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "ab_name": {
                "type": "string",
                "description": "Ghost Ledger tab name.",
                "enum": ["VAULT", "WATERING_HOLE", "LOGIC_LOG", "GOODWILL"],
            },
            "date_range_start": {
                "type": "string",
                "description": "Inclusive ISO-8601 date for the start of the query window.",
            },
            "date_range_end": {
                "type": "string",
                "description": "Inclusive ISO-8601 date for the end of the query window.",
            },
        },
        "required": ["ab_name", "date_range_start", "date_range_end"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "rows": {
                        "type": "array",
                        "items": {"type": "object"},
                    }
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def ghost_ledger_sheets_reader(
    ab_name: str,
    date_range_start: str,
    date_range_end: str,
    **_: Any,
) -> dict[str, Any]:
    """Fetch and filter Ghost Ledger rows via gspread."""

    def _parse_date(date_text: str) -> datetime:
        try:
            parsed = datetime.fromisoformat(date_text)
        except ValueError as exc:  # pragma: no cover - ValueError message carries detail
            raise ValueError(
                "date strings must be ISO-8601 format (YYYY-MM-DD or full timestamp)"
            ) from exc
        return parsed

    try:
        allowed_tabs = {"VAULT", "WATERING_HOLE", "LOGIC_LOG", "GOODWILL"}
        if ab_name not in allowed_tabs:
            raise ValueError(f"ab_name must be one of {sorted(allowed_tabs)}")

        creds_path = os.getenv("GOOGLE_SHEETS_CREDS_PATH")
        sheet_id = os.getenv("GHOST_LEDGER_SHEET_ID")
        if not creds_path:
            raise ValueError("GOOGLE_SHEETS_CREDS_PATH missing; see .env.template")
        if not sheet_id:
            raise ValueError("GHOST_LEDGER_SHEET_ID missing; see .env.template")
        if not os.path.exists(creds_path):
            raise FileNotFoundError(f"Google Sheets credentials file not found: {creds_path}")

        start_date = _parse_date(date_range_start).date()
        end_date = _parse_date(date_range_end).date()
        if end_date < start_date:
            raise ValueError("date_range_end must be >= date_range_start")

        client = gspread.service_account(filename=creds_path)
        worksheet = client.open_by_key(sheet_id).worksheet(ab_name)
        rows = worksheet.get_all_records()

        filtered_rows: list[dict[str, Any]] = []
        for row in rows:
            raw_date = row.get("date") or row.get("Date")
            if not raw_date:
                continue
            try:
                row_date = datetime.fromisoformat(str(raw_date)).date()
            except ValueError:
                continue
            if start_date <= row_date <= end_date:
                filtered_rows.append(row)

        return {
            "status": "success",
            "data": {"rows": filtered_rows},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("ghost_ledger_sheets_reader", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    """Append a Ralph Wiggum lesson entry."""

    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
