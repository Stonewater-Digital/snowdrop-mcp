"""Calculate revenue shares owed to partners."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TIER_DEFAULTS = {"referral": 0.05, "integration": 0.10}

TOOL_META: dict[str, Any] = {
    "name": "partner_revenue_share_calculator",
    "description": "Computes revenue share payouts per partner tier.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "partners": {"type": "array", "items": {"type": "object"}},
            "period": {"type": "string"},
        },
        "required": ["partners", "period"],
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


def partner_revenue_share_calculator(partners: list[dict[str, Any]], period: str, **_: Any) -> dict[str, Any]:
    """Return share schedules per partner."""
    try:
        shares = []
        total_shared = total_retained = 0.0
        for partner in partners:
            tier = partner.get("tier", "referral")
            revenue = float(partner.get("revenue_attributed", 0.0))
            rate = float(partner.get("share_rate_pct") or (TIER_DEFAULTS.get(tier, 0.15) * 100)) / 100
            owed = revenue * rate
            retained = revenue - owed
            total_shared += owed
            total_retained += retained
            shares.append(
                {
                    "partner_id": partner.get("partner_id"),
                    "tier": tier,
                    "revenue": round(revenue, 2),
                    "share_rate_pct": round(rate * 100, 2),
                    "share_owed": round(owed, 2),
                    "payment_schedule": [
                        {"due_date": period, "amount": round(owed, 2)},
                    ],
                }
            )
        retention_rate = (total_retained / (total_retained + total_shared)) * 100 if (total_retained + total_shared) else 0.0
        data = {
            "shares": shares,
            "total_shared": round(total_shared, 2),
            "total_retained": round(total_retained, 2),
            "retention_rate_pct": round(retention_rate, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("partner_revenue_share_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
