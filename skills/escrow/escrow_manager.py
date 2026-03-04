"""Manage escrow lifecycle events between agents."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "escrow_manager",
    "description": "Creates, monitors, and adjudicates agent escrow records.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["create", "release", "dispute", "refund", "status"],
            },
            "escrow": {"type": "object"},
        },
        "required": ["operation", "escrow"],
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


def escrow_manager(
    operation: str,
    escrow: dict[str, Any],
    **_: Any,
) -> dict[str, Any]:
    """Change escrow state while keeping transfers pending Thunder approval."""
    try:
        operation = operation.lower()
        handlers = {
            "create": _handle_create,
            "release": _handle_release,
            "dispute": _handle_dispute,
            "refund": _handle_refund,
            "status": _handle_status,
        }
        if operation not in handlers:
            raise ValueError("Unsupported operation")

        updated = handlers[operation](escrow)
        return {
            "status": "success",
            "data": updated,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("escrow_manager", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _handle_create(escrow: dict[str, Any]) -> dict[str, Any]:
    amount = float(escrow.get("amount", 0))
    if amount <= 0:
        raise ValueError("amount must be positive")
    created = escrow.get("created_at") or datetime.now(timezone.utc).isoformat()
    escrow_state = {**escrow, "status": "held", "created_at": created}
    escrow_state["execution"] = "pending_thunder_approval"
    return escrow_state


def _handle_release(escrow: dict[str, Any]) -> dict[str, Any]:
    if escrow.get("status") == "disputed":
        raise ValueError("Cannot release funds while disputed")
    if escrow.get("skill_delivered") not in {"yes", True, "true"}:
        raise ValueError("Delivery confirmation required before release")
    escrow_state = {**escrow, "status": "released"}
    escrow_state["execution"] = "pending_thunder_approval"
    escrow_state["released_at"] = datetime.now(timezone.utc).isoformat()
    return escrow_state


def _handle_dispute(escrow: dict[str, Any]) -> dict[str, Any]:
    reason = escrow.get("dispute_reason") or "unspecified"
    escrow_state = {**escrow, "status": "disputed", "dispute_reason": reason}
    escrow_state["execution"] = "pending_thunder_approval"
    return escrow_state


def _handle_refund(escrow: dict[str, Any]) -> dict[str, Any]:
    escrow_state = {**escrow, "status": "refunded"}
    escrow_state["execution"] = "pending_thunder_approval"
    escrow_state["refunded_at"] = datetime.now(timezone.utc).isoformat()
    return escrow_state


def _handle_status(escrow: dict[str, Any]) -> dict[str, Any]:
    escrow_state = {**escrow}
    escrow_state.setdefault("status", "held")
    escrow_state["execution"] = "pending_thunder_approval"
    return escrow_state


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
