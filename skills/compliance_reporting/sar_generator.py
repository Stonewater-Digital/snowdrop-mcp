"""Construct Suspicious Activity Report envelopes for Thunder review."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "sar_generator",
    "description": "Drafts FinCEN SAR payloads without auto-filing.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "subject_id": {"type": "string"},
            "account": {"type": "object"},
            "activity_type": {"type": "string"},
            "suspicious_activity": {
                "type": "object",
                "description": "Details about the suspicious activity including description and amount.",
            },
            "filing_entity": {
                "type": "string",
                "default": "Stonewater Solutions LLC",
            },
        },
        "required": ["subject_id", "account", "activity_type", "suspicious_activity"],
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


def sar_generator(
    subject_id: str,
    account: dict[str, Any],
    activity_type: str,
    suspicious_activity: dict[str, Any],
    filing_entity: str = "Stonewater Solutions LLC",
    **_: Any,
) -> dict[str, Any]:
    """Compose a SAR data structure ready for Thunder approval."""
    try:
        if not subject_id:
            raise ValueError("subject_id is required")
        if not isinstance(account, dict):
            raise ValueError("account must be a dict")
        if not isinstance(suspicious_activity, dict):
            raise ValueError("suspicious_activity must be a dict")

        amount = float(suspicious_activity.get("amount", 0.0) or 0.0)
        pattern = str(suspicious_activity.get("pattern", "unspecified"))
        requires_filing = amount >= 5000 or pattern.lower() in {
            "structuring",
            "rapid_inflow_outflow",
            "smurfing",
        }

        sar_data = {
            "filing_entity": filing_entity,
            "subject": {
                "id": subject_id,
                "account": account,
            },
            "activity_type": activity_type,
            "suspicious_activity": suspicious_activity,
            "recommended_action": "pending_thunder_approval",
            "prepared_at": datetime.now(timezone.utc).isoformat(),
        }
        payload = {
            "sar_data": sar_data,
            "execution": "pending_thunder_approval",
            "requires_filing": requires_filing,
        }
        return {
            "status": "success",
            "data": payload,
            "timestamp": sar_data["prepared_at"],
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("sar_generator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
