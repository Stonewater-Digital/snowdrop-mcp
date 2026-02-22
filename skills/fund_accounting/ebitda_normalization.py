"""
Executive Summary: Scrubs and normalizes reported EBITDA by categorizing and summing add-back adjustments for M&A due diligence.

Inputs: reported_ebitda (float), adjustments (list[dict]: item, amount, category)
Outputs: dict with normalized_ebitda (float), adjustment_summary (dict of category totals), total_adjustments (float)
MCP Tool Name: ebitda_normalization
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "ebitda_normalization",
    "description": "Scrubs and normalizes reported EBITDA by categorizing and summing add-back adjustments for M&A due diligence.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "reported_ebitda": {
                "type": "number",
                "description": "As-reported EBITDA in dollars",
            },
            "adjustments": {
                "type": "array",
                "description": "List of EBITDA add-back adjustments",
                "items": {
                    "type": "object",
                    "properties": {
                        "item": {"type": "string", "description": "Description of the adjustment"},
                        "amount": {
                            "type": "number",
                            "description": "Adjustment amount (positive = add-back, negative = deduction)",
                        },
                        "category": {
                            "type": "string",
                            "enum": ["one_time", "owner_comp", "non_recurring", "rent_adjustment"],
                            "description": "Adjustment category",
                        },
                    },
                    "required": ["item", "amount", "category"],
                },
            },
        },
        "required": ["reported_ebitda", "adjustments"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "normalized_ebitda": {"type": "number"},
            "adjustment_summary": {"type": "object"},
            "total_adjustments": {"type": "number"},
            "adjustment_detail": {"type": "array"},
            "normalization_multiple_impact": {"type": "object"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": [
            "normalized_ebitda", "adjustment_summary", "total_adjustments",
            "status", "timestamp",
        ],
    },
}

_VALID_CATEGORIES = {"one_time", "owner_comp", "non_recurring", "rent_adjustment"}

_CATEGORY_LABELS: dict[str, str] = {
    "one_time": "One-Time Items",
    "owner_comp": "Owner Compensation Normalization",
    "non_recurring": "Non-Recurring Items",
    "rent_adjustment": "Rent / Real Estate Adjustment",
}

# Typical M&A EBITDA multiples for quick sanity-check output
_REFERENCE_MULTIPLES = [4.0, 5.0, 6.0, 7.0, 8.0, 10.0, 12.0]


def ebitda_normalization(
    reported_ebitda: float,
    adjustments: list[dict[str, Any]],
    **kwargs: Any,
) -> dict:
    """Normalizes EBITDA by applying categorized add-back adjustments.

    Iterates through each adjustment, validates its category, and accumulates
    totals by category. Normalized EBITDA = reported_ebitda + total_adjustments.
    Also generates an implied valuation range table using reference multiples.

    Categories:
    - one_time: Non-repeating events (litigation, insurance proceeds, etc.)
    - owner_comp: Delta between owner compensation and market-rate replacement
    - non_recurring: Items unlikely to repeat (restructuring, one-off consulting)
    - rent_adjustment: Difference between actual rent and market rent (related party)

    Args:
        reported_ebitda: As-reported EBITDA in dollars.
        adjustments: List of dicts with keys: item (str), amount (float),
            category (str in valid set above).
        **kwargs: Ignored extra keyword arguments.

    Returns:
        dict: Contains normalized_ebitda (float), adjustment_summary (dict of
              category -> total), total_adjustments (float), adjustment_detail
              (list with per-item breakdown), normalization_multiple_impact
              (implied EV at reference multiples), status, timestamp.
    """
    try:
        category_totals: dict[str, float] = {cat: 0.0 for cat in _VALID_CATEGORIES}
        adjustment_detail: list[dict] = []

        for adj in adjustments:
            item = adj.get("item", "")
            amount = float(adj.get("amount", 0.0))
            category = adj.get("category", "")

            if category not in _VALID_CATEGORIES:
                raise ValueError(
                    f"Invalid category '{category}' for item '{item}'. "
                    f"Must be one of: {sorted(_VALID_CATEGORIES)}"
                )

            category_totals[category] += amount
            adjustment_detail.append({
                "item": item,
                "amount": round(amount, 2),
                "category": category,
                "category_label": _CATEGORY_LABELS[category],
            })

        total_adjustments = sum(category_totals.values())
        normalized_ebitda = reported_ebitda + total_adjustments

        adjustment_summary: dict[str, Any] = {}
        for cat, total in category_totals.items():
            adjustment_summary[cat] = {
                "label": _CATEGORY_LABELS[cat],
                "total": round(total, 2),
                "item_count": sum(1 for a in adjustments if a.get("category") == cat),
                "pct_of_reported": round(total / reported_ebitda, 6) if reported_ebitda != 0 else 0.0,
            }

        # Implied EV table at reference multiples
        normalization_multiple_impact: dict[str, dict] = {}
        for multiple in _REFERENCE_MULTIPLES:
            normalization_multiple_impact[f"{multiple}x"] = {
                "reported_ev": round(reported_ebitda * multiple, 2),
                "normalized_ev": round(normalized_ebitda * multiple, 2),
                "ev_uplift": round(total_adjustments * multiple, 2),
            }

        result = {
            "reported_ebitda": round(reported_ebitda, 2),
            "total_adjustments": round(total_adjustments, 2),
            "normalized_ebitda": round(normalized_ebitda, 2),
            "normalization_pct": round(total_adjustments / reported_ebitda, 6) if reported_ebitda != 0 else 0.0,
            "adjustment_summary": adjustment_summary,
            "adjustment_detail": adjustment_detail,
            "normalization_multiple_impact": normalization_multiple_impact,
            "adjustment_count": len(adjustments),
        }
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as e:
        logger.error(f"ebitda_normalization failed: {e}")
        _log_lesson(f"ebitda_normalization: {e}")
        return {"status": "error", "error": str(e), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    """Appends an error lesson to the lessons log.

    Args:
        message: The lesson message to log.
    """
    os.makedirs("logs", exist_ok=True)
    with open("logs/lessons.md", "a") as f:
        f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
