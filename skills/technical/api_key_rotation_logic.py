"""
Executive Summary: Automated credential security — flags expired/expiring-soon API keys and builds a prioritized rotation schedule.
Inputs: credentials (list of dicts: service str, key_name str, created_date str ISO, max_age_days int default 90)
Outputs: expired (list), expiring_soon (list within 7 days), rotation_schedule (list of dicts), compliance_pct (float)
MCP Tool Name: api_key_rotation_logic
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone, timedelta

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "api_key_rotation_logic",
    "description": (
        "Evaluates API credential ages against their configured maximum lifetime. "
        "Returns three categories: expired keys (must rotate now), expiring-soon keys "
        "(within 7 days), and a full rotation schedule sorted by urgency. "
        "Also reports an overall compliance percentage."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "credentials": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "service":      {"type": "string"},
                        "key_name":     {"type": "string"},
                        "created_date": {"type": "string", "format": "date-time"},
                        "max_age_days": {"type": "integer", "default": 90},
                    },
                    "required": ["service", "key_name", "created_date"],
                },
            }
        },
        "required": ["credentials"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "expired":             {"type": "array"},
            "expiring_soon":       {"type": "array"},
            "rotation_schedule":   {"type": "array"},
            "compliance_pct":      {"type": "number"},
            "status":              {"type": "string"},
            "timestamp":           {"type": "string"},
        },
        "required": ["expired", "expiring_soon", "rotation_schedule", "compliance_pct", "status", "timestamp"],
    },
}

DEFAULT_MAX_AGE_DAYS: int = 90
EXPIRING_SOON_DAYS: int = 7


def api_key_rotation_logic(credentials: list[dict[str, Any]]) -> dict[str, Any]:
    """Evaluate API key ages and produce a prioritized rotation schedule.

    Args:
        credentials: List of credential descriptors. Each dict must contain:
            - service (str): Name of the external service (e.g. "openai", "stripe").
            - key_name (str): Identifier for this specific key.
            - created_date (str): ISO 8601 date/datetime when the key was created.
            - max_age_days (int, optional): Maximum allowed age before rotation.
              Defaults to 90 days.

    Returns:
        dict with keys:
            - status (str): "success" or "error".
            - expired (list[dict]): Credentials that have exceeded max_age_days.
            - expiring_soon (list[dict]): Valid credentials expiring within 7 days.
            - rotation_schedule (list[dict]): All credentials needing action, sorted
              by priority (days_overdue descending for expired, days_remaining
              ascending for expiring soon).
            - compliance_pct (float): Percentage of credentials currently compliant.
            - timestamp (str): ISO 8601 UTC execution timestamp.
    """
    try:
        now_utc: datetime = datetime.now(timezone.utc)

        expired: list[dict[str, Any]] = []
        expiring_soon: list[dict[str, Any]] = []
        rotation_schedule: list[dict[str, Any]] = []
        compliant_count: int = 0

        for cred in credentials:
            service: str = cred.get("service", "unknown")
            key_name: str = cred.get("key_name", "unknown")
            raw_created: str = cred.get("created_date", "")
            max_age_days: int = int(cred.get("max_age_days", DEFAULT_MAX_AGE_DAYS))

            try:
                created_dt: datetime = datetime.fromisoformat(raw_created)
                if created_dt.tzinfo is None:
                    created_dt = created_dt.replace(tzinfo=timezone.utc)
            except ValueError:
                created_dt = datetime.min.replace(tzinfo=timezone.utc)

            age_days: int = (now_utc - created_dt).days
            expiry_dt: datetime = created_dt + timedelta(days=max_age_days)
            days_remaining: int = (expiry_dt - now_utc).days
            days_overdue: int = max(0, age_days - max_age_days)

            entry: dict[str, Any] = {
                "service":        service,
                "key_name":       key_name,
                "created_date":   raw_created,
                "age_days":       age_days,
                "max_age_days":   max_age_days,
                "days_remaining": days_remaining,
                "days_overdue":   days_overdue,
                "expires_at":     expiry_dt.isoformat(),
            }

            if age_days > max_age_days:
                # Already expired
                priority_label: str = "CRITICAL" if days_overdue > 30 else "HIGH"
                expired.append(entry)
                rotation_schedule.append({**entry, "priority": priority_label})
            elif days_remaining <= EXPIRING_SOON_DAYS:
                # Still valid but expiring soon
                expiring_soon.append(entry)
                rotation_schedule.append({**entry, "priority": "MEDIUM"})
            else:
                compliant_count += 1

        total: int = len(credentials)
        compliance_pct: float = (compliant_count / total * 100.0) if total > 0 else 100.0

        # Sort: expired first (by days_overdue desc), then expiring-soon (days_remaining asc)
        rotation_schedule.sort(
            key=lambda x: (-x["days_overdue"], x["days_remaining"])
        )

        return {
            "status":           "success",
            "expired":          expired,
            "expiring_soon":    expiring_soon,
            "rotation_schedule": rotation_schedule,
            "compliance_pct":   round(compliance_pct, 2),
            "timestamp":        now_utc.isoformat(),
        }

    except Exception as e:
        logger.error(f"api_key_rotation_logic failed: {e}")
        _log_lesson(f"api_key_rotation_logic: {e}")
        return {"status": "error", "error": str(e), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    """Append a failure lesson to the shared lessons log.

    Args:
        message: Human-readable description of the failure.
    """
    with open("logs/lessons.md", "a") as f:
        f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
