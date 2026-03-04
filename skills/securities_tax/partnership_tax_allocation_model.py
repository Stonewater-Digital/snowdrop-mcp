"""Partnership tax allocation model.
Distributes taxable income to partners using ownership and hurdle preferences.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "partnership_tax_allocation_model",
    "description": "Allocates partnership income among partners with preferred returns.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "partners": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "ownership_pct": {"type": "number"},
                        "preferred_return_pct": {"type": "number", "default": 0.0},
                    },
                    "required": ["name", "ownership_pct"],
                },
            },
            "taxable_income": {"type": "number"},
        },
        "required": ["partners", "taxable_income"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def partnership_tax_allocation_model(partners: Sequence[dict[str, Any]], taxable_income: float, **_: Any) -> dict[str, Any]:
    """Return allocation schedule after preferred returns."""
    try:
        preferred_paid = []
        remaining_income = taxable_income
        for partner in partners:
            pref = taxable_income * partner.get("preferred_return_pct", 0.0) / 100
            preferred_paid.append(pref)
            remaining_income -= pref
        allocations = []
        for partner, pref_amount in zip(partners, preferred_paid):
            share = remaining_income * partner["ownership_pct"] / 100 if taxable_income else 0.0
            total_alloc = pref_amount + share
            allocations.append(
                {
                    "name": partner["name"],
                    "allocation": round(total_alloc, 2),
                    "preferred_component": round(pref_amount, 2),
                }
            )
        data = {
            "allocations": allocations,
            "remaining_income": round(remaining_income, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("partnership_tax_allocation_model failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
