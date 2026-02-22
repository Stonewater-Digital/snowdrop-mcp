"""Generate IRS Schedule D / Form 8949-ready data."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "schedule_d_8949_generator",
    "description": "Classifies transactions into short- and long-term gains for tax filing.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "transactions": {
                "type": "array",
                "items": {"type": "object"},
                "description": "List with buy_date, sell_date, proceeds, cost_basis, asset.",
            }
        },
        "required": ["transactions"],
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


def schedule_d_8949_generator(transactions: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return Schedule D friendly aggregates.

    Args:
        transactions: Capital gain/loss entries with buy/sell dates and amounts.

    Returns:
        Envelope with line items plus aggregated short- and long-term totals.
    """

    try:
        line_items = []
        totals = {
            "short_term": {"proceeds": 0.0, "cost_basis": 0.0, "gain": 0.0},
            "long_term": {"proceeds": 0.0, "cost_basis": 0.0, "gain": 0.0},
        }

        for tx in transactions:
            buy_date = _parse_date(tx.get("buy_date"))
            sell_date = _parse_date(tx.get("sell_date"))
            proceeds = float(tx.get("proceeds", 0) or 0)
            cost_basis = float(tx.get("cost_basis", 0) or 0)
            gain = round(proceeds - cost_basis, 4)
            holding_days = (sell_date - buy_date).days
            term = "long_term" if holding_days >= 365 else "short_term"

            totals[term]["proceeds"] += proceeds
            totals[term]["cost_basis"] += cost_basis
            totals[term]["gain"] += gain

            line_items.append(
                {
                    "asset": tx.get("asset"),
                    "buy_date": buy_date.date().isoformat(),
                    "sell_date": sell_date.date().isoformat(),
                    "proceeds": round(proceeds, 4),
                    "cost_basis": round(cost_basis, 4),
                    "gain": gain,
                    "term": term,
                }
            )

        summary = {
            bucket: {
                "proceeds": round(values["proceeds"], 2),
                "cost_basis": round(values["cost_basis"], 2),
                "gain": round(values["gain"], 2),
            }
            for bucket, values in totals.items()
        }

        return {
            "status": "success",
            "data": {"line_items": line_items, "totals": summary},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("schedule_d_8949_generator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _parse_date(raw: str | None) -> datetime:
    if not raw:
        raise ValueError("Missing date value in transaction")
    normalized = raw.strip()
    if "T" not in normalized:
        normalized += "T00:00:00+00:00"
    normalized = normalized.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized)


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
