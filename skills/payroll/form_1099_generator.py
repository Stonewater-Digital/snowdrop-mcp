"""Generate 1099-NEC data packets."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "form_1099_generator",
    "description": "Produces Snowdrop's 1099-NEC structure for Thunder review.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "payee": {"type": "object"},
            "total_paid": {"type": "number"},
            "tax_year": {"type": "integer"},
        },
        "required": ["payee", "total_paid", "tax_year"],
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


def form_1099_generator(
    payee: dict[str, Any],
    total_paid: float,
    tax_year: int,
    **_: Any,
) -> dict[str, Any]:
    """Return 1099-NEC payload (no filing)."""

    try:
        if total_paid < 600:
            raise ValueError("1099-NEC applicable only for payments >= $600")
        form = {
            "tax_year": tax_year,
            "payee": payee,
            "box_1_nonemployee_comp": round(total_paid, 2),
            "status": "pending_thunder_approval",
        }
        return {
            "status": "success",
            "data": {"form": form},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("form_1099_generator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
