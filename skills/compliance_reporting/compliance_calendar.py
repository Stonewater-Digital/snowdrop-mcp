"""Unified compliance deadline calendar."""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "compliance_calendar",
    "description": "Generates a consolidated compliance deadline calendar with statuses.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "entity": {"type": "object"},
            "filings": {
                "type": "array",
                "items": {"type": "object"},
            },
            "current_date": {
                "type": "string",
                "description": "ISO date used as the reference point.",
            },
        },
        "required": ["entity", "filings", "current_date"],
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


def compliance_calendar(
    entity: dict[str, Any],
    filings: list[dict[str, Any]],
    current_date: str,
    **_: Any,
) -> dict[str, Any]:
    """Build a compliance calendar with standard and custom obligations."""
    try:
        ref_date = _parse_date(current_date, "current_date")
        if not isinstance(entity, dict):
            raise ValueError("entity must be a dict")
        if not isinstance(filings, list):
            raise ValueError("filings must be a list")

        calendar_items = []
        for filing in filings:
            if not isinstance(filing, dict):
                raise ValueError("each filing entry must be a dict")
            filing_type = str(filing.get("type", "unspecified"))
            frequency = str(filing.get("frequency", "annual"))
            last_due = filing.get("last_due")
            due_date = _next_due_date(last_due, frequency, ref_date)
            calendar_items.append(_format_calendar_item(filing_type, due_date, ref_date))

        calendar_items.extend(_standard_requirements(entity, ref_date))
        calendar_items.sort(key=lambda item: item["due_date"])

        result = {"calendar": calendar_items, "entity": entity}
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("compliance_calendar", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _standard_requirements(entity: dict[str, Any], ref_date: date) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    formation_date = entity.get("formation_date")
    fiscal_year_end = entity.get("fiscal_year_end")

    if formation_date:
        anniversary = _next_anniversary(_parse_date(formation_date, "formation_date"), ref_date)
        items.append(_format_calendar_item("LLC annual report", anniversary, ref_date))

    fy_end = _parse_date(fiscal_year_end, "fiscal_year_end") if fiscal_year_end else None
    if fy_end:
        k1_due = date(ref_date.year, 3, 15)
        if ref_date.month > 3:
            k1_due = date(ref_date.year + 1, 3, 15)
        items.append(_format_calendar_item("K-1 distribution", k1_due, ref_date))

    # Estimated taxes: next quarterly stub (Jan 15, Apr 15, Jun 15, Sep 15)
    quarterly_dates = [date(ref_date.year, 1, 15), date(ref_date.year, 4, 15), date(ref_date.year, 6, 15), date(ref_date.year, 9, 15)]
    next_estimated = next((dt for dt in quarterly_dates if dt >= ref_date), date(ref_date.year + 1, 1, 15))
    items.append(_format_calendar_item("Estimated taxes", next_estimated, ref_date))

    # 1099 filing Jan 31
    jan31 = date(ref_date.year, 1, 31)
    if ref_date > jan31:
        jan31 = date(ref_date.year + 1, 1, 31)
    items.append(_format_calendar_item("1099 filings", jan31, ref_date))

    # SAR review monthly
    sar_review_due = (ref_date.replace(day=1) + timedelta(days=32)).replace(day=1)
    items.append(_format_calendar_item("SAR review", sar_review_due, ref_date))

    # AML training annual
    aml_due = _next_anniversary(_parse_date(formation_date, "formation_date"), ref_date) if formation_date else ref_date
    items.append(_format_calendar_item("AML training", aml_due, ref_date))

    return items


def _next_anniversary(original: date, ref_date: date) -> date:
    candidate = original.replace(year=ref_date.year)
    if candidate < ref_date:
        candidate = candidate.replace(year=ref_date.year + 1)
    return candidate


def _next_due_date(last_due: str | None, frequency: str, ref_date: date) -> date:
    allowed = {"monthly": 1, "quarterly": 3, "semiannual": 6, "annual": 12}
    months = allowed.get(frequency.lower(), 12)
    due = _parse_date(last_due, "last_due") if last_due else ref_date
    while due <= ref_date:
        due = _add_months(due, months)
    return due


def _add_months(original: date, months: int) -> date:
    month = original.month - 1 + months
    year = original.year + month // 12
    month = month % 12 + 1
    day = min(original.day, [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
    return date(year, month, day)


def _format_calendar_item(name: str, due_date: date, ref_date: date) -> dict[str, Any]:
    days_until = (due_date - ref_date).days
    if days_until < 0:
        status = "overdue"
    elif days_until <= 14:
        status = "due_soon"
    else:
        status = "scheduled"
    return {
        "name": name,
        "due_date": due_date.isoformat(),
        "days_until_due": days_until,
        "status": status,
    }


def _parse_date(value: str | None, field_name: str) -> date:
    if value is None:
        raise ValueError(f"{field_name} is required for this calculation")
    try:
        return datetime.fromisoformat(value).date()
    except ValueError as exc:  # noqa: B904
        raise ValueError(f"Invalid {field_name}: {value}") from exc


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
