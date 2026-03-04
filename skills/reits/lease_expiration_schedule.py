"""Bucket lease expirations by year to highlight rollover risk."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "lease_expiration_schedule",
    "description": "Creates lease expiration ladder showing annual rollover percentages.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "leases": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "tenant": {"type": "string"},
                        "annual_rent": {"type": "number"},
                        "expires_in_year": {"type": "integer"},
                    },
                    "required": ["tenant", "annual_rent", "expires_in_year"],
                },
            }
        },
        "required": ["leases"],
    },
    "outputSchema": {"type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def lease_expiration_schedule(leases: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return expiration buckets and concentration metrics."""
    try:
        total_rent = sum(item.get("annual_rent", 0.0) for item in leases)
        buckets: dict[str, float] = defaultdict(float)
        for lease in leases:
            year = lease.get("expires_in_year", 0)
            if year <= 1:
                bucket = "year_1"
            elif year == 2:
                bucket = "year_2"
            elif year == 3:
                bucket = "year_3"
            elif year == 4:
                bucket = "year_4"
            elif year == 5:
                bucket = "year_5"
            else:
                bucket = "year_5_plus"
            buckets[bucket] += lease.get("annual_rent", 0.0)
        bucket_pct = {
            bucket: round((amount / total_rent * 100) if total_rent else 0.0, 2)
            for bucket, amount in buckets.items()
        }
        largest_bucket = max(bucket_pct.items(), key=lambda item: item[1])[0] if bucket_pct else "none"
        data = {
            "bucket_percentages": bucket_pct,
            "largest_bucket": largest_bucket,
            "rollover_warning": bucket_pct.get("year_1", 0.0) > 15,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("lease_expiration_schedule", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
