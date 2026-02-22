"""Flag unusual counterparty or behavioral transaction signals."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "transaction_anomaly_flagger",
    "description": "Scores transactions for amount, counterparty, category, and timing anomalies.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "transactions": {"type": "array", "items": {"type": "object"}},
            "history_stats": {"type": "object"},
        },
        "required": ["transactions", "history_stats"],
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


def transaction_anomaly_flagger(
    transactions: list[dict[str, Any]],
    history_stats: dict[str, Any],
    **_: Any,
) -> dict[str, Any]:
    """Flag transactions deviating from historical baselines."""
    try:
        avg = float(history_stats.get("avg_amount", 0) or 0)
        std = float(history_stats.get("std_amount", 0) or 0)
        known_counterparties = set(history_stats.get("known_counterparties", []))
        typical_categories = set(history_stats.get("typical_categories", []))
        if not transactions:
            raise ValueError("transactions cannot be empty")

        flagged: list[dict[str, Any]] = []
        for txn in transactions:
            txn_amount = float(txn.get("amount", 0))
            reasons: list[str] = []
            if std > 0 and abs(txn_amount - avg) > 3 * std:
                reasons.append("amount_outlier")
            elif std == 0 and txn_amount > avg * 2:
                reasons.append("amount_outlier")

            counterparty = str(txn.get("counterparty", "")).strip()
            if counterparty and counterparty not in known_counterparties:
                reasons.append("unknown_counterparty")

            category = str(txn.get("category", "")).lower()
            if category and typical_categories and category not in typical_categories:
                reasons.append("unusual_category")

            timestamp = txn.get("timestamp")
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                    if 2 <= dt.hour < 5:
                        reasons.append("odd_hours_activity")
                except ValueError:
                    reasons.append("invalid_timestamp")

            if reasons:
                flagged.append({"transaction": txn, "reasons": reasons})

        risk_summary = _summarize_risk(flagged)
        data = {
            "flagged": flagged,
            "flag_count": len(flagged),
            "risk_summary": risk_summary,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("transaction_anomaly_flagger", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _summarize_risk(flagged: list[dict[str, Any]]) -> str:
    if not flagged:
        return "No anomalies detected." 
    reason_counts: dict[str, int] = {}
    for entry in flagged:
        for reason in entry.get("reasons", []):
            reason_counts[reason] = reason_counts.get(reason, 0) + 1
    parts = [f"{reason}: {count}" for reason, count in sorted(reason_counts.items())]
    return ", ".join(parts)


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
