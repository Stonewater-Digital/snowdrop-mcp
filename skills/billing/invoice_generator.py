"""Create Watering Hole invoices for Snowdrop partners."""
from __future__ import annotations

import uuid
from typing import Any

from skills.utils import SkillTelemetryEmitter, get_iso_timestamp, log_lesson

TOOL_META: dict[str, Any] = {
    "name": "invoice_generator",
    "description": "Generates franchise-friendly invoices with royalty handling.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "agent_id": {"type": "string"},
            "line_items": {
                "type": "array",
                "items": {"type": "object"},
            },
            "currency": {"type": "string", "default": "USDC"},
            "due_date": {"type": "string"},
        },
        "required": ["agent_id", "line_items", "due_date"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "invoice": {"type": "object"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def invoice_generator(
    agent_id: str,
    line_items: list[dict[str, Any]],
    due_date: str,
    currency: str = "USDC",
    **_: Any,
) -> dict[str, Any]:
    """Construct an invoice payload with optional franchise royalties."""

    emitter = SkillTelemetryEmitter(
        "invoice_generator",
        {
            "agent_id": agent_id,
            "line_item_count": len(line_items or []),
            "currency": currency,
        },
    )
    try:
        if not line_items:
            raise ValueError("line_items cannot be empty")

        processed_items: list[dict[str, Any]] = []
        subtotal = 0.0
        for item in line_items:
            quantity = float(item.get("quantity", 0))
            unit_price = float(item.get("unit_price", 0))
            if quantity <= 0 or unit_price < 0:
                raise ValueError("Each line item needs positive quantity and non-negative price")
            extended = quantity * unit_price
            subtotal += extended
            processed_items.append({**item, "extended_total": round(extended, 2)})

        royalty = 0.0
        if _requires_royalty(agent_id):
            royalty = round(subtotal * 0.10, 2)

        total_due = round(subtotal + royalty, 2)
        invoice = {
            "invoice_id": f"inv_{uuid.uuid4()}",
            "agent_id": agent_id,
            "currency": currency,
            "due_date": due_date,
            "line_items": processed_items,
            "subtotal": round(subtotal, 2),
            "franchise_royalty": royalty,
            "total_due": total_due,
            "status": "pending_thunder_approval",
        }
        emitter.record(
            "ok",
            {
                "subtotal": round(subtotal, 2),
                "franchise_royalty": royalty,
                "total_due": total_due,
                "requires_royalty": royalty > 0,
            },
        )
        return {
            "status": "success",
            "data": {"invoice": invoice},
            "timestamp": get_iso_timestamp(),
        }
    except Exception as exc:
        log_lesson(f"invoice_generator: {exc}")
        emitter.record("error", {"error": str(exc)})
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": get_iso_timestamp(),
        }


def _requires_royalty(agent_id: str) -> bool:
    normalized = agent_id.lower()
    return "franchise" in normalized or normalized.startswith("wh-")
