"""
Executive Summary: Calculates investor-level withholding obligations for upcoming distributions with treaty overrides.

Inputs: distributions (list[dict]), default_rate (float, optional), treaty_overrides (dict[str, float], optional), base_currency (str, optional)
Outputs: status (str), data (withholding/summary), timestamp (str)
MCP Tool Name: withholding_obligation_tracker
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
    "name": "withholding_obligation_tracker",
    "description": "Compute gross vs. net distributions and withholding requirements per LP.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "distributions": {
                "type": "array",
                "items": {"type": "object"},
                "description": "Entries with lp_name, amount, residency, and classification.",
            },
            "default_rate": {
                "type": "number",
                "default": 0.30,
                "description": "Fallback withholding rate when no treaty override exists.",
            },
            "treaty_overrides": {
                "type": "object",
                "description": "Map of residency or LP name to withholding rate.",
            },
            "base_currency": {
                "type": "string",
                "default": "USD",
                "description": "Currency label for reporting.",
            },
        },
        "required": ["distributions"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["ok", "error"]},
            "data": {
                "type": "object",
                "properties": {
                    "withholding": {"type": "array", "items": {"type": "object"}},
                    "summary": {"type": "object"},
                },
            },
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def withholding_obligation_tracker(
    distributions: list[dict[str, Any]],
    default_rate: float = 0.30,
    treaty_overrides: dict[str, float] | None = None,
    base_currency: str = "USD",
) -> dict[str, Any]:
    """Calculate withholding obligations for investor distributions."""
    emitter = SkillTelemetryEmitter(
        "withholding_obligation_tracker",
        {"records": len(distributions or []), "default_rate": default_rate},
    )
    try:
        if not distributions:
            raise ValueError("distributions cannot be empty")
        if default_rate < 0 or default_rate > 1:
            raise ValueError("default_rate must be between 0 and 1")

        overrides = {key.lower(): float(value) for key, value in (treaty_overrides or {}).items()}

        withholding_rows: list[dict[str, Any]] = []
        totals = {"gross": 0.0, "withheld": 0.0, "net": 0.0}

        for entry in distributions:
            lp_name = str(entry.get("lp_name") or "unknown")
            amount = float(entry.get("amount") or 0.0)
            residency = str(entry.get("residency") or "").lower()
            classification = str(entry.get("classification") or "general")
            override_key = lp_name.lower()
            rate = overrides.get(override_key, overrides.get(residency, default_rate))
            withheld = amount * rate
            net = amount - withheld
            withheld_row = {
                "lp_name": lp_name,
                "residency": residency.upper(),
                "classification": classification,
                "gross_amount": round(amount, 2),
                "withholding_rate": round(rate, 4),
                "withheld_amount": round(withheld, 2),
                "net_amount": round(net, 2),
                "currency": base_currency,
            }
            withholding_rows.append(withheld_row)
            totals["gross"] += amount
            totals["withheld"] += withheld
            totals["net"] += net

        summary = {
            "base_currency": base_currency,
            "total_gross": round(totals["gross"], 2),
            "total_withheld": round(totals["withheld"], 2),
            "total_net": round(totals["net"], 2),
            "average_rate": round(totals["withheld"] / totals["gross"], 4) if totals["gross"] else 0.0,
        }
        emitter.record("ok", summary)
        return {
            "status": "ok",
            "data": {"withholding": withholding_rows, "summary": summary},
            "timestamp": get_iso_timestamp(),
        }
    except Exception as exc:  # noqa: BLE001
        logger.error(f"withholding_obligation_tracker failed: {exc}")
        _log_lesson("withholding_obligation_tracker", str(exc))
        emitter.record("error", {"error": str(exc)})
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": get_iso_timestamp()}


def _log_lesson(skill_name: str, error: str) -> None:
    """Proxy shared logger."""
    _shared_log_lesson(skill_name, error)
