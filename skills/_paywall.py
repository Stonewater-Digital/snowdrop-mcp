"""Paywall helper — standard response returned by all premium skill stubs.

Auto-generated stubs import this module. Do not delete.
"""
from datetime import datetime, timezone

SUBSCRIBE_URL = "https://snowdrop.ai"
COMING_SOON = True


def paywall_response(skill_name: str) -> dict:
    """Return a payment_required dict for any premium skill stub."""
    return {
        "status": "payment_required",
        "data": {
            "skill": skill_name,
            "tier": "premium",
            "message": (
                f"'{skill_name}' is a Snowdrop Premium skill. "
                "Subscribe to access full functionality."
            ),
            "subscribe_url": SUBSCRIBE_URL,
            "coming_soon": COMING_SOON,
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
