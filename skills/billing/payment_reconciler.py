"""Match inbound payments to outstanding invoices."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from skills.utils import SkillTelemetryEmitter, get_iso_timestamp, log_lesson

TOOL_META: dict[str, Any] = {
    "name": "payment_reconciler",
    "description": "Reconciles Watering Hole payments against invoice records.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "payments": {
                "type": "array",
                "items": {"type": "object"},
            },
            "invoices": {
                "type": "array",
                "items": {"type": "object"},
            },
        },
        "required": ["payments", "invoices"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "matched": {"type": "array", "items": {"type": "object"}},
                    "unmatched_payments": {"type": "array", "items": {"type": "object"}},
                    "overdue_invoices": {"type": "array", "items": {"type": "object"}},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def payment_reconciler(
    payments: list[dict[str, Any]],
    invoices: list[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    """Return matching pairs, open payments, and overdue invoices."""
    emitter = SkillTelemetryEmitter(
        "payment_reconciler",
        {"payments": len(payments or []), "invoices": len(invoices or [])},
    )
    try:
        tolerance = 0.01
        open_invoices = invoices.copy()
        matched: list[dict[str, Any]] = []
        unmatched: list[dict[str, Any]] = []

        for payment in payments:
            candidate_index = _find_invoice(payment, open_invoices, tolerance)
            if candidate_index is None:
                unmatched.append(payment)
                continue
            invoice = open_invoices.pop(candidate_index)
            matched.append({"payment": payment, "invoice": invoice})

        overdue_list = _identify_overdue(open_invoices)
        data = {
            "matched": matched,
            "unmatched_payments": unmatched,
            "overdue_invoices": overdue_list,
        }
        emitter.record(
            "ok",
            {
                "matched": len(matched),
                "unmatched": len(unmatched),
                "overdue": len(overdue_list),
            },
        )
        return {
            "status": "success",
            "data": data,
            "timestamp": get_iso_timestamp(),
        }
    except Exception as exc:
        log_lesson(f"payment_reconciler: {exc}")
        emitter.record("error", {"error": str(exc)})
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": get_iso_timestamp(),
        }


def _find_invoice(
    payment: dict[str, Any],
    open_invoices: list[dict[str, Any]],
    tolerance: float,
) -> int | None:
    pay_amount = float(payment.get("amount", 0))
    pay_agent = payment.get("from_agent")
    for index, invoice in enumerate(open_invoices):
        if invoice.get("agent_id") != pay_agent:
            continue
        amount_due = float(invoice.get("amount_due", 0))
        if abs(amount_due - pay_amount) <= tolerance:
            return index
    return None


def _identify_overdue(invoices: list[dict[str, Any]]) -> list[dict[str, Any]]:
    now = datetime.now(timezone.utc).date()
    overdue: list[dict[str, Any]] = []
    for invoice in invoices:
        due_text = invoice.get("due_date")
        if not due_text:
            continue
        try:
            due_date = datetime.fromisoformat(due_text).date()
        except ValueError:
            continue
        if due_date < now:
            overdue.append(invoice)
    return overdue
