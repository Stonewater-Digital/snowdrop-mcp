"""Reconcile billed vs. actual compute usage."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "billing_reconciler",
    "description": "Compares invoiced amounts against measured compute usage to surface deltas.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "invoiced": {"type": "array", "items": {"type": "object"}},
            "actual_usage": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["invoiced", "actual_usage"],
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


def billing_reconciler(
    invoiced: list[dict[str, Any]],
    actual_usage: list[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    """Identify over/under-billing conditions per agent-period."""
    try:
        actual_lookup = {
            (str(entry.get("agent_id")), str(entry.get("period"))): float(entry.get("computed_cost", 0.0))
            for entry in actual_usage
        }
        discrepancies = []
        overbilled_total = 0.0
        underbilled_total = 0.0
        affected_agents: set[str] = set()
        invoiced_keys: set[tuple[str, str]] = set()

        for invoice in invoiced:
            if not isinstance(invoice, dict):
                raise ValueError("each invoiced entry must be a dict")
            agent_id = str(invoice.get("agent_id"))
            period = str(invoice.get("period"))
            billed = float(invoice.get("amount_billed", 0.0))
            actual = actual_lookup.get((agent_id, period), 0.0)
            invoiced_keys.add((agent_id, period))
            diff = round(billed - actual, 4)
            if diff == 0:
                continue
            affected_agents.add(agent_id)
            discrepancy_type = "overbilled" if diff > 0 else "underbilled"
            if diff > 0:
                overbilled_total += diff
            else:
                underbilled_total += abs(diff)
            discrepancies.append(
                {
                    "agent_id": agent_id,
                    "period": period,
                    "amount_billed": billed,
                    "actual_cost": actual,
                    "difference": diff,
                    "type": discrepancy_type,
                }
            )

        for (agent_id, period), actual in actual_lookup.items():
            if (agent_id, period) in invoiced_keys:
                continue
            diff = round(0.0 - actual, 4)
            underbilled_total += abs(diff)
            affected_agents.add(agent_id)
            discrepancies.append(
                {
                    "agent_id": agent_id,
                    "period": period,
                    "amount_billed": 0.0,
                    "actual_cost": actual,
                    "difference": diff,
                    "type": "underbilled",
                }
            )

        data = {
            "discrepancies": discrepancies,
            "total_overbilled": round(overbilled_total, 4),
            "total_underbilled": round(underbilled_total, 4),
            "agents_affected": len(affected_agents),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("billing_reconciler", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
