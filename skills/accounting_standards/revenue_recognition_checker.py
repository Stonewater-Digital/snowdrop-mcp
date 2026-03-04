"""Check ASC 606 revenue recognition compliance."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "revenue_recognition_checker",
    "description": "Applies the ASC 606 five-step model to contracts and allocates revenue to obligations.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "contract": {"type": "object"},
        },
        "required": ["contract"],
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


def revenue_recognition_checker(contract: dict[str, Any], **_: Any) -> dict[str, Any]:
    """Return recognized vs deferred revenue and notes."""
    try:
        obligations = contract.get("performance_obligations", [])
        total_standalone = sum(po.get("standalone_price", 0) for po in obligations)
        if total_standalone == 0:
            raise ValueError("Standalone selling prices required")
        allocation = []
        recognized = deferred = 0.0
        notes = []
        for po in obligations:
            relative_pct = po.get("standalone_price", 0) / total_standalone
            allocated_price = contract.get("total_value", 0) * relative_pct
            method = po.get("delivery_type", "point_in_time")
            satisfied = po.get("delivered", False)
            if method == "over_time":
                recognized_amount = allocated_price * (po.get("pct_complete", 0) / 100)
            else:
                recognized_amount = allocated_price if satisfied else 0
            deferred_amount = allocated_price - recognized_amount
            recognized += recognized_amount
            deferred += deferred_amount
            allocation.append(
                {
                    "obligation": po.get("description"),
                    "allocated": round(allocated_price, 2),
                    "recognized": round(recognized_amount, 2),
                    "deferred": round(deferred_amount, 2),
                }
            )
            notes.append(
                f"PO '{po.get('description')}' recognized via {method} with satisfaction={'yes' if satisfied else 'no'}"
            )
        data = {
            "recognized_revenue": round(recognized, 2),
            "deferred_revenue": round(deferred, 2),
            "allocation": allocation,
            "recognition_method_by_po": [
                {"description": po.get("description"), "method": po.get("delivery_type")}
                for po in obligations
            ],
            "compliance_notes": notes,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("revenue_recognition_checker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
