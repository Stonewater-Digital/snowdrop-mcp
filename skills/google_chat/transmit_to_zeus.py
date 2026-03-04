"""
transmit_to_zeus.py — Prepare daily intel and transmit to Zeus via Google Chat.

Executive Summary:
    Orchestrator skill that calls prep_daily_intel to generate BLUF bullets,
    formats them into a branded message, and sends to the Conductive Black Ops
    Google Chat space via google_chat_send (Incoming Webhook).

Table of Contents:
    1. TOOL_META
    2. Message Formatting
    3. Skill Implementation
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.transmit_to_zeus")

# ---------------------------------------------------------------------------
# 1. TOOL_META
# ---------------------------------------------------------------------------

TOOL_META = {
    "name": "transmit_to_zeus",
    "description": "Prepare daily intel and transmit to Zeus via Conductive Black Ops Google Chat space.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "hours_lookback": {
                "type": "integer",
                "description": "Hours of data to analyze (default: 24)",
            },
        },
    },
}

# ---------------------------------------------------------------------------
# 2. Message Formatting
# ---------------------------------------------------------------------------

_STATUS_EMOJI = {
    "GREEN": "\U0001f7e2",  # 🟢
    "YELLOW": "\U0001f7e1",  # 🟡
    "RED": "\U0001f534",  # 🔴
}


def _format_message(bullets: list[str], status_indicator: str, date_str: str) -> str:
    """Format the intel briefing message for Google Chat."""
    emoji = _STATUS_EMOJI.get(status_indicator, "\u2754")
    bullet_text = "\n".join(bullets)
    return (
        f"{emoji} SNOWDROP DAILY INTEL \u2014 {date_str}\n"
        f"Status: {status_indicator}\n\n"
        f"{bullet_text}\n\n"
        f"\u2014 Snowdrop Black Ops | T-20 automated briefing"
    )


# ---------------------------------------------------------------------------
# 3. Skill Implementation
# ---------------------------------------------------------------------------


def transmit_to_zeus(
    hours_lookback: int = 24,
) -> dict[str, Any]:
    """Prepare and transmit daily intel to Zeus.

    Args:
        hours_lookback: Hours of log data to analyze.

    Returns:
        Standard Snowdrop response with intel and send results.
    """
    ts = datetime.now(timezone.utc).isoformat()

    try:
        # Step 1: Prepare intel
        from skills.google_chat.prep_daily_intel import prep_daily_intel

        intel_result = prep_daily_intel(hours_lookback=hours_lookback)
        if intel_result["status"] != "ok":
            return {
                "status": "error",
                "data": {"error": f"Intel prep failed: {intel_result['data'].get('error', 'unknown')}"},
                "timestamp": ts,
            }

        bullets = intel_result["data"]["bullets"]
        status_indicator = intel_result["data"]["status_indicator"]
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        # Step 2: Format message
        message = _format_message(bullets, status_indicator, date_str)

        # Step 3: Send via Google Chat webhook
        from skills.google_chat.google_chat_send import google_chat_send

        send_result = google_chat_send(
            message_text=message,
            thread_id="daily-intel",
        )

        if send_result["status"] != "ok":
            return {
                "status": "error",
                "data": {
                    "error": f"Chat send failed: {send_result['data'].get('error', 'unknown')}",
                    "intel": intel_result["data"],
                },
                "timestamp": ts,
            }

        logger.info("Daily intel transmitted to Zeus — status=%s", status_indicator)
        return {
            "status": "ok",
            "data": {
                "intel": intel_result["data"],
                "send": send_result["data"],
                "message_preview": message[:200],
            },
            "timestamp": ts,
        }

    except Exception as exc:
        logger.error("transmit_to_zeus failed: %s", exc)
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": ts,
        }
