"""Append structured activity rows into the Ghost Ledger notebook."""
from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

import gspread

TOOL_META: dict[str, Any] = {
    "name": "ghost_ledger_sheets_writer",
    "description": "Appends validated ledger rows to Ghost Ledger Google Sheets tabs.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "tab_name": {
                "type": "string",
                "enum": ["VAULT", "WATERING_HOLE"],
                "description": "Target worksheet name.",
            },
            "rows": {
                "type": "array",
                "items": {"type": "object"},
                "description": "Rows to append.",
            },
        },
        "required": ["tab_name", "rows"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "rows_written": {"type": "integer"},
                    "submission_status": {"type": "string"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def ghost_ledger_sheets_writer(
    tab_name: str,
    rows: list[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    """Validate and append Ghost Ledger rows."""

    try:
        tab_schemas: dict[str, tuple[str, ...]] = {
            "VAULT": ("date", "source", "tx_id", "amount", "currency", "balance_after"),
            "WATERING_HOLE": ("date", "agent_id", "skill", "revenue", "cost"),
        }
        if tab_name not in tab_schemas:
            raise ValueError("tab_name must be VAULT or WATERING_HOLE")
        if not rows:
            raise ValueError("rows must include at least one entry")

        creds_path = os.getenv("GOOGLE_SHEETS_CREDS_PATH")
        sheet_id = os.getenv("GHOST_LEDGER_SHEET_ID")
        if not creds_path:
            raise ValueError("GOOGLE_SHEETS_CREDS_PATH missing; see .env.template")
        if not sheet_id:
            raise ValueError("GHOST_LEDGER_SHEET_ID missing; see .env.template")

        required_columns = tab_schemas[tab_name]
        cleaned_rows: list[list[Any]] = []
        preferred_order = list(required_columns)

        extra_columns: list[str] = []
        for entry in rows:
            missing = [col for col in required_columns if col not in entry]
            if missing:
                raise ValueError(f"Missing required columns for {tab_name}: {missing}")
            for column in entry:
                if column not in preferred_order and column not in extra_columns:
                    extra_columns.append(column)

        columns = preferred_order + extra_columns
        for entry in rows:
            cleaned_rows.append([entry.get(col, "") for col in columns])

        client = gspread.service_account(filename=creds_path)
        worksheet = client.open_by_key(sheet_id).worksheet(tab_name)
        worksheet.append_rows(cleaned_rows, value_input_option="USER_ENTERED")

        return {
            "status": "success",
            "data": {
                "rows_written": len(rows),
                "submission_status": "pending_thunder_approval",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("ghost_ledger_sheets_writer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    """Append a Ralph Wiggum lesson entry."""

    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
