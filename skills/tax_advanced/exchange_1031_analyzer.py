"""Analyze 1031 like-kind exchange timelines and tax deferral."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "exchange_1031_analyzer",
    "description": "Calculates gains, boot, and deadlines for like-kind exchanges.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "relinquished": {"type": "object"},
            "replacement_candidates": {"type": "array", "items": {"type": "object"}},
            "sale_date": {"type": "string"},
        },
        "required": ["relinquished", "replacement_candidates", "sale_date"],
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


def exchange_1031_analyzer(
    relinquished: dict[str, Any],
    replacement_candidates: list[dict[str, Any]],
    sale_date: str,
    **_: Any,
) -> dict[str, Any]:
    """Return gain breakdown and deadlines for a 1031 exchange."""
    try:
        sale_price = relinquished.get("sale_price", 0.0)
        basis = relinquished.get("adjusted_basis", 0.0)
        mortgage = relinquished.get("mortgage", 0.0)
        closing_costs = relinquished.get("closing_costs", 0.0)
        realized_gain = sale_price - basis - closing_costs
        minimum_replacement_price = sale_price - closing_costs
        qualifying = [
            cand
            for cand in replacement_candidates
            if cand.get("price", 0.0) >= minimum_replacement_price
        ]
        boot = max(0.0, sale_price - sum(c.get("price", 0.0) for c in qualifying))
        tax_deferred = realized_gain - boot
        sale_dt = datetime.fromisoformat(sale_date)
        identification_deadline = (sale_dt + timedelta(days=45)).date().isoformat()
        closing_deadline = (sale_dt + timedelta(days=180)).date().isoformat()
        data = {
            "realized_gain": round(realized_gain, 2),
            "tax_deferred": round(tax_deferred, 2),
            "boot_taxable": round(boot, 2),
            "identification_deadline": identification_deadline,
            "closing_deadline": closing_deadline,
            "qualifying_replacements": qualifying,
            "minimum_replacement_price": round(minimum_replacement_price, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("exchange_1031_analyzer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
