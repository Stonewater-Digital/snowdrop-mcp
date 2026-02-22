"""Auto-categorize Snowdrop expenses to IRS Schedule C codes."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "expense_categorizer",
    "description": "Maps expense strings to IRS categories using heuristics.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "expenses": {
                "type": "array",
                "items": {"type": "object"},
            }
        },
        "required": ["expenses"],
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

CATEGORY_RULES = {
    "Software/SaaS": {
        "keywords": ["openai", "anthropic", "openrouter", "slack", "notion"],
        "irs_line": "Part II, Line 27a",
    },
    "Web Services": {
        "keywords": ["railway", "fly.io", "flyio", "vercel", "aws"],
        "irs_line": "Part II, Line 25",
    },
    "Trading Fees": {
        "keywords": ["kraken", "binance", "coinbase"],
        "irs_line": "Part II, Line 10",
    },
    "Professional Services": {
        "keywords": ["legal", "counsel", "consultant"],
        "irs_line": "Part II, Line 17",
    },
}


def expense_categorizer(expenses: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return expenses enriched with category mapping."""

    try:
        categorized: list[dict[str, Any]] = []
        for expense in expenses:
            vendor = expense.get("vendor", "").lower()
            description = expense.get("description", "").lower()
            category, irs_line = _match_category(vendor + " " + description)
            categorized.append(
                {
                    **expense,
                    "category": category,
                    "irs_line": irs_line,
                }
            )
        data = {"categorized_expenses": categorized}
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("expense_categorizer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _match_category(text: str) -> tuple[str, str]:
    for category, meta in CATEGORY_RULES.items():
        if any(keyword in text for keyword in meta["keywords"]):
            return category, meta["irs_line"]
    return "Other", "Part II, Line 27a"


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
