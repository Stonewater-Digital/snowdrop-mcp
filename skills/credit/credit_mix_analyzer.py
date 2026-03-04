"""Analyze credit mix diversity, average age, and provide recommendations.

MCP Tool Name: credit_mix_analyzer
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "credit_mix_analyzer",
    "description": "Analyze credit account mix by type, count diversity score, compute average account age, and provide recommendations for a healthier credit profile.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "accounts": {
                "type": "array",
                "description": "List of credit accounts.",
                "items": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string", "description": "Account type (e.g., credit_card, mortgage, auto_loan, student_loan, personal_loan)."},
                        "balance": {"type": "number", "description": "Current balance."},
                        "age_months": {"type": "integer", "description": "Account age in months."},
                    },
                    "required": ["type", "balance", "age_months"],
                },
            },
        },
        "required": ["accounts"],
    },
}

_IDEAL_TYPES = {"credit_card", "mortgage", "auto_loan", "student_loan", "personal_loan"}


def credit_mix_analyzer(accounts: list[dict[str, Any]]) -> dict[str, Any]:
    """Analyze credit mix diversity and average age."""
    try:
        if not accounts:
            return {
                "status": "error",
                "data": {"error": "accounts list must not be empty."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        type_counts: dict[str, int] = {}
        total_age = 0
        for acct in accounts:
            t = acct["type"].lower().replace(" ", "_")
            type_counts[t] = type_counts.get(t, 0) + 1
            total_age += acct["age_months"]

        unique_types = set(type_counts.keys())
        avg_age_months = total_age / len(accounts)
        avg_age_years = avg_age_months / 12

        # Diversity score: how many of the ideal types are present (0-100)
        diversity_score = round(len(unique_types & _IDEAL_TYPES) / len(_IDEAL_TYPES) * 100, 1)

        missing = _IDEAL_TYPES - unique_types
        recommendations = []
        if missing:
            recommendations.append(f"Consider adding: {', '.join(sorted(missing))} for better mix.")
        if avg_age_years < 3:
            recommendations.append("Average account age is low; avoid opening new accounts unnecessarily.")
        if diversity_score >= 80:
            recommendations.append("Excellent credit mix diversity.")

        return {
            "status": "ok",
            "data": {
                "total_accounts": len(accounts),
                "type_counts": type_counts,
                "unique_types": len(unique_types),
                "diversity_score": diversity_score,
                "avg_age_months": round(avg_age_months, 1),
                "avg_age_years": round(avg_age_years, 1),
                "recommendations": recommendations,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
