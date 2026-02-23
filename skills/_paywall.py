"""
Paywall helper — standard response returned by all premium skill stubs.

Auto-generated stubs import this module via `from skills._paywall import paywall_response`.
Do not delete or rename this file.

Premium skills appear in tools/list with their full name and signature so developers can
see what they do. Calling a premium skill without a subscription returns this response.
Subscribe: https://snowdrop.ai (coming soon)
"""
from datetime import datetime, timezone

SUBSCRIBE_URL = "https://snowdrop.ai"
COMING_SOON = True


def paywall_response(skill_name: str) -> dict:
    """Return a standard payment_required dict for any premium skill stub.

    Args:
        skill_name: The MCP tool name that was called (for informative error message).

    Returns:
        dict with status="payment_required" and subscription details.
    """
    return {
        "status": "payment_required",
        "data": {
            "skill": skill_name,
            "tier": "premium",
            "message": (
                f"'{skill_name}' is a Snowdrop Premium skill. "
                "Subscribe to access the full implementation."
            ),
            "subscribe_url": SUBSCRIBE_URL,
            "coming_soon": COMING_SOON,
            "note": (
                "All premium skills are visible in tools/list so you can evaluate "
                "the interface before subscribing."
            ),
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
