"""Transform structured metrics into narratives."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "data_narrator",
    "description": "Converts structured finance outputs into tone-aware prose.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "data_type": {
                "type": "string",
                "enum": ["portfolio_summary", "pnl", "reconciliation", "alert"],
            },
            "data": {"type": "object"},
            "tone": {"type": "string", "default": "professional"},
        },
        "required": ["data_type", "data"],
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


def data_narrator(
    data_type: str,
    data: dict[str, Any],
    tone: str = "professional",
    **_: Any,
) -> dict[str, Any]:
    """Generate a templated narrative for the requested data type."""
    try:
        builders = {
            "portfolio_summary": _portfolio_summary,
            "pnl": _pnl_summary,
            "reconciliation": _reconciliation_summary,
            "alert": _alert_summary,
        }
        if data_type not in builders:
            raise ValueError("Unsupported data_type")
        narrative, key_points, sentiment = builders[data_type](data, tone)
        payload = {
            "narrative": narrative,
            "key_points": key_points,
            "sentiment": sentiment,
        }
        return {
            "status": "success",
            "data": payload,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("data_narrator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _portfolio_summary(data: dict[str, Any], tone: str) -> tuple[str, list[str], str]:
    change_pct = float(data.get("change_pct", 0))
    direction = "gained" if change_pct >= 0 else "declined"
    sentiment = "positive" if change_pct > 0 else "negative" if change_pct < 0 else "neutral"
    total_value = data.get("total_value", "n/a")
    movers = ", ".join(data.get("top_movers", [])) or "no standout positions"
    narrative = (
        f"Portfolio {direction} {abs(change_pct):.2f}% to {total_value} in {tone} tone. "
        f"Leaders: {movers}."
    )
    key_points = [
        f"Total value: {total_value}",
        f"Change: {change_pct:.2f}%",
        f"Top movers: {movers}",
    ]
    return narrative, key_points, sentiment


def _pnl_summary(data: dict[str, Any], tone: str) -> tuple[str, list[str], str]:
    profit = float(data.get("net_profit", 0))
    sentiment = "positive" if profit > 0 else "negative" if profit < 0 else "neutral"
    verb = "generated" if profit >= 0 else "absorbed"
    revenue = data.get("revenue", 0)
    expenses = data.get("expenses", 0)
    narrative = (
        f"Operations {verb} {abs(profit):,.0f} in net P&L. Revenue of {revenue:,.0f} versus "
        f"expenses of {expenses:,.0f}. Tone: {tone}."
    )
    return (
        narrative,
        [
            f"Revenue: {revenue:,.0f}",
            f"Expenses: {expenses:,.0f}",
            f"Net P&L: {profit:,.0f}",
        ],
        sentiment,
    )


def _reconciliation_summary(data: dict[str, Any], tone: str) -> tuple[str, list[str], str]:
    mismatches = data.get("unreconciled_items", [])
    sentiment = "alert" if mismatches else "positive"
    if mismatches:
        details = ", ".join(mismatches[:5])
        narrative = (
            f"Unusual activity detected: {len(mismatches)} items await reconciliation ({details})."
            f" Tone: {tone}."
        )
    else:
        narrative = "All ledgers reconcile cleanly; no action required."
    key_points = [f"Unreconciled count: {len(mismatches)}"]
    return narrative, key_points, sentiment


def _alert_summary(data: dict[str, Any], tone: str) -> tuple[str, list[str], str]:
    alert_type = data.get("alert_type", "general alert")
    severity = data.get("severity", "info")
    message = data.get("message", "")
    sentiment = "negative" if severity in {"high", "critical"} else "neutral"
    narrative = f"{alert_type.title()} flagged at {severity.upper()} severity: {message}. Tone: {tone}."
    key_points = [f"Alert: {alert_type}", f"Severity: {severity}"]
    return narrative, key_points, sentiment


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
