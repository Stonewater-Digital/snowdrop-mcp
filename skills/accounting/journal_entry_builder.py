"""Create balanced double-entry journal entries."""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "journal_entry_builder",
    "description": "Builds balanced journal entries and assigns sequential IDs.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "date": {"type": "string"},
            "description": {"type": "string"},
            "lines": {
                "type": "array",
                "items": {"type": "object"},
                "description": "Journal lines with account_number, debit, credit",
            },
        },
        "required": ["date", "description", "lines"],
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

_JE_LOG = "logs/journal_entries.jsonl"


def journal_entry_builder(
    date: str,
    description: str,
    lines: list[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    """Validate and store double-entry journal data."""
    try:
        if not lines:
            raise ValueError("lines cannot be empty")
        total_debits = round(sum(float(line.get("debit", 0.0)) for line in lines), 2)
        total_credits = round(sum(float(line.get("credit", 0.0)) for line in lines), 2)
        if total_debits != total_credits:
            raise ValueError("Journal entry is not balanced")
        entry_id = _next_entry_id()
        entry = {
            "entry_id": entry_id,
            "date": date,
            "description": description,
            "lines": lines,
            "total": total_debits,
        }
        _append_entry(entry)
        data = {
            "entry_id": entry_id,
            "balanced": True,
            "lines": lines,
            "total": total_debits,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("journal_entry_builder", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _next_entry_id() -> str:
    if not os.path.exists(_JE_LOG):
        return "JE-0001"
    with open(_JE_LOG, "r", encoding="utf-8") as handle:
        lines = handle.readlines()
    if not lines:
        return "JE-0001"
    last_entry = json.loads(lines[-1])
    last_number = int(last_entry["entry_id"].split("-")[-1])
    return f"JE-{last_number + 1:04d}"


def _append_entry(entry: dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(_JE_LOG), exist_ok=True)
    with open(_JE_LOG, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry) + "\n")


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
