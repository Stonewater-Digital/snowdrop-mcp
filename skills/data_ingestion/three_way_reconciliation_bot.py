"""
Executive Summary: Performs GL vs. administrator vs. custodian three-way reconciliations and surfaces breaks with variance context.

Inputs: gl_entries (list[dict]), admin_entries (list[dict]), custodian_entries (list[dict]), tolerance (float, optional)
Outputs: status (str), data (matched/breaks/summary), timestamp (str)
MCP Tool Name: three_way_reconciliation_bot
"""
from __future__ import annotations

from typing import Any

from skills.utils import (
    SkillTelemetryEmitter,
    get_iso_timestamp,
    logger,
    log_lesson as _shared_log_lesson,
)

TOOL_META: dict[str, Any] = {
    "name": "three_way_reconciliation_bot",
    "description": "Matches GL, administrator, and custodian balances to highlight breaks exceeding tolerance.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "gl_entries": {
                "type": "array",
                "items": {"type": "object"},
                "description": "General ledger rows containing id, amount, currency.",
            },
            "admin_entries": {
                "type": "array",
                "items": {"type": "object"},
                "description": "Fund administrator records aligned to the same identifiers.",
            },
            "custodian_entries": {
                "type": "array",
                "items": {"type": "object"},
                "description": "Custodian records with positions/cash for reconciliation.",
            },
            "tolerance": {
                "type": "number",
                "default": 0.01,
                "description": "Absolute variance tolerance (in source currency units).",
            },
        },
        "required": ["gl_entries", "admin_entries", "custodian_entries"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["ok", "error"]},
            "data": {
                "type": "object",
                "properties": {
                    "matched": {"type": "array", "items": {"type": "object"}},
                    "breaks": {"type": "array", "items": {"type": "object"}},
                    "summary": {"type": "object"},
                },
            },
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def three_way_reconciliation_bot(
    gl_entries: list[dict[str, Any]],
    admin_entries: list[dict[str, Any]],
    custodian_entries: list[dict[str, Any]],
    tolerance: float = 0.01,
) -> dict[str, Any]:
    """Run a three-way reconciliation using record identifiers.

    Args:
        gl_entries: Ledger entries keyed by transaction id or reference.
        admin_entries: Administrator statements for the same identifiers.
        custodian_entries: Custodian balances/transactions per identifier.
        tolerance: Maximum allowable absolute difference before flagging a break.

    Returns:
        Snowdrop response dict that separates matched ids from breaks.

    Raises:
        ValueError: If inputs are not lists or tolerance is negative.
    """
    emitter = SkillTelemetryEmitter(
        "three_way_reconciliation_bot",
        {
            "gl_entries": len(gl_entries or []),
            "admin_entries": len(admin_entries or []),
            "custodian_entries": len(custodian_entries or []),
            "tolerance": tolerance,
        },
    )
    try:
        for name, payload in {
            "gl_entries": gl_entries,
            "admin_entries": admin_entries,
            "custodian_entries": custodian_entries,
        }.items():
            if not isinstance(payload, list):
                raise ValueError(f"{name} must be a list of dicts")
        if tolerance < 0:
            raise ValueError("tolerance must be >= 0")

        combined = _aggregate_sources(
            {
                "gl": gl_entries,
                "admin": admin_entries,
                "custodian": custodian_entries,
            }
        )

        matched: list[dict[str, Any]] = []
        breaks: list[dict[str, Any]] = []
        for record_id, amounts in combined.items():
            max_gap = _largest_gap(amounts)
            entry = {
                "record_id": record_id,
                "gl": amounts.get("gl", 0.0),
                "admin": amounts.get("admin", 0.0),
                "custodian": amounts.get("custodian", 0.0),
                "currency": amounts.get("currency"),
                "largest_gap": max_gap,
                "missing_sources": sorted(amounts.get("missing_sources", [])),
            }
            if max_gap <= tolerance and not entry["missing_sources"]:
                matched.append(entry)
            else:
                breaks.append(entry)

        summary = {
            "total_ids": len(combined),
            "matched_ids": len(matched),
            "break_ids": len(breaks),
            "gl_total": round(sum(item.get("gl", 0.0) for item in matched + breaks), 4),
            "admin_total": round(sum(item.get("admin", 0.0) for item in matched + breaks), 4),
            "custodian_total": round(sum(item.get("custodian", 0.0) for item in matched + breaks), 4),
        }
        emitter.record(
            "ok",
            {
                "matched_ids": len(matched),
                "break_ids": len(breaks),
                "tolerance": tolerance,
            },
        )

        return {
            "status": "ok",
            "data": {"matched": matched, "breaks": breaks, "summary": summary},
            "timestamp": get_iso_timestamp(),
        }
    except Exception as exc:
        msg = f"three_way_reconciliation_bot failed: {exc}"
        logger.error(msg)
        _log_lesson("three_way_reconciliation_bot", str(exc))
        emitter.record("error", {"error": str(exc)})
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": get_iso_timestamp()}


def _aggregate_sources(sources: dict[str, list[dict[str, Any]]]) -> dict[str, dict[str, Any]]:
    """Return a map of record_id -> per-source balances and metadata.

    Args:
        sources: Mapping of source label to its list of entries.

    Returns:
        Aggregated dictionary keyed by record identifier.
    """
    aggregated: dict[str, dict[str, Any]] = {}
    for source_name, entries in sources.items():
        for entry in entries or []:
            if not isinstance(entry, dict):
                continue
            record_id = str(entry.get("id") or entry.get("record_id") or entry.get("reference") or "")
            if not record_id:
                continue
            amount = _to_float(entry.get("amount"))
            currency = entry.get("currency")
            bucket = aggregated.setdefault(
                record_id,
                {
                    "gl": 0.0,
                    "admin": 0.0,
                    "custodian": 0.0,
                    "currency": currency,
                    "missing_sources": set(),
                },
            )
            bucket[source_name] = (bucket.get(source_name, 0.0) or 0.0) + (amount or 0.0)
            bucket["currency"] = bucket["currency"] or currency

    for record_id, bucket in aggregated.items():
        missing = {src for src in sources if bucket.get(src) in (None, 0.0)}
        bucket["missing_sources"] = missing
    return aggregated


def _largest_gap(amounts: dict[str, Any]) -> float:
    """Compute the largest absolute difference between any two sources."""
    values = [amounts.get("gl", 0.0), amounts.get("admin", 0.0), amounts.get("custodian", 0.0)]
    max_gap = 0.0
    for i, lhs in enumerate(values):
        for rhs in values[i + 1 :]:
            gap = abs((lhs or 0.0) - (rhs or 0.0))
            max_gap = max(max_gap, gap)
    return round(max_gap, 6)


def _to_float(value: Any) -> float | None:
    """Convert incoming values to floats safely."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _log_lesson(skill_name: str, error: str) -> None:
    """Proxy to shared lesson logger for consistent formatting."""
    _shared_log_lesson(skill_name, error)
