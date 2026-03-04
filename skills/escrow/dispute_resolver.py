"""Guide structured resolutions for escrow disputes."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "dispute_resolver",
    "description": "Determines auto, manual, or split dispute resolutions for escrow issues.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "dispute": {"type": "object"},
            "resolution_type": {
                "type": "string",
                "enum": ["auto", "manual", "split"],
            },
        },
        "required": ["dispute", "resolution_type"],
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


def dispute_resolver(
    dispute: dict[str, Any],
    resolution_type: str,
    **_: Any,
) -> dict[str, Any]:
    """Resolve a dispute using configurable heuristics."""
    try:
        amount = float(dispute.get("amount", 0))
        if amount <= 0:
            raise ValueError("dispute amount must be positive")
        resolution_type = resolution_type.lower()
        handlers = {
            "auto": _resolve_auto,
            "manual": _resolve_manual,
            "split": _resolve_split,
        }
        if resolution_type not in handlers:
            raise ValueError("Unsupported resolution_type")
        outcome = handlers[resolution_type](dispute, amount)
        return {
            "status": "success",
            "data": outcome,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("dispute_resolver", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _resolve_auto(dispute: dict[str, Any], amount: float) -> dict[str, Any]:
    reason = (dispute.get("reason") or "").lower()
    evidence = dispute.get("evidence", []) or []
    if "not delivered" in reason or "no show" in reason:
        refund = amount
        resolution = "full_refund"
        reasoning = "Service flagged as undelivered"
    elif "partial" in reason or len(evidence) < 1:
        refund = amount * 0.5
        resolution = "partial_refund"
        reasoning = "Insufficient evidence for full refund"
    else:
        refund = amount * 0.25
        resolution = "goodwill_refund"
        reasoning = "Evidence favors respondent"
    return {
        "resolution": resolution,
        "refund_amount": round(refund, 2),
        "escalated": False,
        "reasoning": reasoning,
    }


def _resolve_manual(dispute: dict[str, Any], amount: float) -> dict[str, Any]:
    return {
        "resolution": "escalated_to_thunder",
        "refund_amount": 0.0,
        "escalated": True,
        "reasoning": "Manual review requested for dispute",
    }


def _resolve_split(dispute: dict[str, Any], amount: float) -> dict[str, Any]:
    split_refund = amount * 0.5
    return {
        "resolution": "split_refund",
        "refund_amount": round(split_refund, 2),
        "escalated": False,
        "reasoning": "Parties share responsibility; issuing 50/50 split",
    }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
