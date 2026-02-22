"""Match inbound payments to outstanding invoices."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

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
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("payment_reconciler", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
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


def _log_lesson(skill_name: str, error: str) -> None:
    """Append a Ralph Wiggum lesson entry."""

    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
