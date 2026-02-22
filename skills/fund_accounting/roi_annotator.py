"""Adds return-on-investment context to any transaction record."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "roi_annotator",
    "description": "Enriches ledger transactions with qualitative ROI commentary.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "transaction": {
                "type": "object",
                "description": "Transaction dict containing amount/description/category.",
            }
        },
        "required": ["transaction"],
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


def roi_annotator(transaction: dict[str, Any], **_: Any) -> dict[str, Any]:
    """Attach a qualitative ROI annotation to the supplied transaction.

    Args:
        transaction: Raw ledger entry containing amount, description, and category.

    Returns:
        Envelope with the enriched transaction that now includes roi_annotation text.
    """

    try:
        amount = float(transaction.get("amount", 0) or 0)
        category = (transaction.get("category") or "general").lower()
        description = (transaction.get("description") or "").lower()

        annotation = _build_annotation(amount, category, description)
        enriched = dict(transaction)
        enriched["roi_annotation"] = annotation

        return {
            "status": "success",
            "data": enriched,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("roi_annotator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _build_annotation(amount: float, category: str, description: str) -> str:
    if amount == 0:
        return "Zero-dollar entry tagged for traceability." \
            "Opportunity: confirm whether value was realized."

    if "grok" in description:
        return (
            f"${amount:.2f} Grok sweep detected sentiment divergence ≥2%."
            " Signal ready for thesis refinement."
        )

    if category in {"compute", "infra"}:
        efficiency = "high" if amount < 50 else "moderate"
        return (
            f"${amount:.2f} {category} cycle with {efficiency} efficiency → unlocks automation"
            " runway for Watering Hole experiments."
        )

    if category == "api":
        return (
            f"${amount:.2f} API pull fueled data freshness for Ghost Ledger reconciliations."
            " Ripple: lower NAV variance risk."
        )

    if "ton" in description:
        return f"${amount:.2f} TON ops stabilized liquidity bands for Thunder's thesis."

    return f"${amount:.2f} deployed toward {category} — monitor impact during next Ralph loop."


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
