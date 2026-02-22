"""Post-action self-audit that compares planned work versus executed outcomes."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "elegance_loop",
    "description": (
        "Compares planned actions against executed results, quantifies drift, and flags when"
        " discrepancies breach the 1% tolerance."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "planned_actions": {
                "type": "array",
                "items": {"type": "object"},
                "description": "Actions Snowdrop intended to execute.",
            },
            "executed_results": {
                "type": "array",
                "items": {"type": "object"},
                "description": "Observed execution logs or API receipts.",
            },
        },
        "required": ["planned_actions", "executed_results"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string", "format": "date-time"},
        },
    },
}


def elegance_loop(
    planned_actions: list[dict[str, Any]],
    executed_results: list[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    """Measure execution drift after Snowdrop takes an action.

    Args:
        planned_actions: Sequence of intended actions and their metadata/amounts.
        executed_results: Observed results pulled from APIs, ledgers, or brokers.

    Returns:
        Envelope with discrepancy percentage, running totals, and escalation flag.
    """

    try:
        def _key(item: dict[str, Any], fallback_index: int) -> str:
            return str(
                item.get("id")
                or item.get("action")
                or item.get("reference")
                or fallback_index
            )

        planned_index = {_key(item, idx): item for idx, item in enumerate(planned_actions)}
        executed_index = {_key(item, idx): item for idx, item in enumerate(executed_results)}

        discrepancies: list[dict[str, Any]] = []
        planned_total = 0.0
        executed_total = 0.0

        for key, planned in planned_index.items():
            planned_amount = float(planned.get("amount", 0) or 0)
            planned_total += planned_amount
            executed_amount = float(executed_index.get(key, {}).get("amount", 0) or 0)
            executed_total += executed_amount
            if abs(planned_amount - executed_amount) > 0:
                discrepancies.append(
                    {
                        "key": key,
                        "planned_amount": planned_amount,
                        "executed_amount": executed_amount,
                        "delta": round(executed_amount - planned_amount, 6),
                    }
                )

        for key, executed in executed_index.items():
            if key in planned_index:
                continue
            executed_amount = float(executed.get("amount", 0) or 0)
            executed_total += executed_amount
            discrepancies.append(
                {
                    "key": key,
                    "planned_amount": 0.0,
                    "executed_amount": executed_amount,
                    "delta": round(executed_amount, 6),
                }
            )

        total_delta = executed_total - planned_total
        discrepancy_pct = (
            abs(total_delta) / planned_total * 100 if planned_total else (100.0 if total_delta else 0.0)
        )
        escalate = discrepancy_pct > 1

        if discrepancies:
            log_summary = (
                f"discrepancies={len(discrepancies)} delta={round(total_delta, 4)}"
                f" pct={round(discrepancy_pct, 2)}"
            )
            _log_lesson("elegance_loop", log_summary)

        data = {
            "planned_total": round(planned_total, 4),
            "executed_total": round(executed_total, 4),
            "total_delta": round(total_delta, 4),
            "discrepancy_pct": round(discrepancy_pct, 4),
            "escalate": escalate,
            "discrepancies": discrepancies,
        }

        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("elegance_loop", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    """Append discrepancy notes to lessons.md."""
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
