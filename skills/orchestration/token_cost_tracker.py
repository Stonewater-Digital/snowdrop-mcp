"""Track token and cost usage per API call with a daily cap."""
from __future__ import annotations

import csv
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Iterable

DAILY_CAP_USD = 50.0
DEFAULT_LOG = Path("logs/token_costs.csv")

TOOL_META: dict[str, Any] = {
    "name": "token_cost_tracker",
    "description": "Logs model API usage and enforces the $50/day spend cap.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "entries": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "timestamp": {"type": "string"},
                        "model": {"type": "string"},
                        "tokens_in": {"type": "number"},
                        "tokens_out": {"type": "number"},
                        "cost_usd": {"type": "number"},
                        "purpose": {"type": "string"},
                    },
                },
                "description": "Usage entries to append and track.",
            },
            "log_path": {"type": "string"},
        },
        "required": ["entries"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "daily_total": {"type": "number"},
                    "cap_usd": {"type": "number"},
                    "cap_remaining": {"type": "number"},
                    "cap_breached": {"type": "boolean"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def token_cost_tracker(
    entries: Iterable[dict[str, Any]],
    log_path: str | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Append usage entries and evaluate the daily cap."""
    try:
        log_file = Path(log_path) if log_path else DEFAULT_LOG
        log_file.parent.mkdir(parents=True, exist_ok=True)

        today = datetime.now(timezone.utc).date()
        daily_total = _load_daily_total(log_file, today)

        with log_file.open("a", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            for entry in entries:
                ts = entry.get("timestamp") or datetime.now(timezone.utc).isoformat()
                cost = float(entry.get("cost_usd", 0.0))
                record_date = datetime.fromisoformat(ts.replace("Z", "+00:00")).date()
                if record_date == today:
                    daily_total += cost
                writer.writerow([
                    ts,
                    entry.get("model"),
                    entry.get("tokens_in", 0),
                    entry.get("tokens_out", 0),
                    cost,
                    entry.get("purpose"),
                ])

        cap_breached = daily_total > DAILY_CAP_USD
        cap_remaining = max(DAILY_CAP_USD - daily_total, 0.0)
        data = {
            "daily_total": round(daily_total, 2),
            "cap_usd": DAILY_CAP_USD,
            "cap_remaining": round(cap_remaining, 2),
            "cap_breached": cap_breached,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("token_cost_tracker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _load_daily_total(log_file: Path, target_date: date) -> float:
    if not log_file.exists():
        return 0.0
    total = 0.0
    with log_file.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        for row in reader:
            if len(row) < 5:
                continue
            try:
                ts = datetime.fromisoformat(row[0].replace("Z", "+00:00"))
            except ValueError:
                continue
            if ts.date() == target_date:
                try:
                    total += float(row[4])
                except ValueError:
                    continue
    return total


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
