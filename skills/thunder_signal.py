"""
Executive Summary: Telegram alert bot that delivers severity-tiered messages to Thunder (the Operator) with three named trigger helpers for vault breaches, Sybil detection, and general intel.

Inputs: severity (str: CRITICAL/WARNING/INTEL), message (str)
Outputs: dict confirming message delivery with chat_id and formatted text
MCP Tool Name: thunder_signal
"""
import asyncio
import logging
import os
from typing import Any
from skills.utils import log_lesson, get_iso_timestamp, logger

from telegram import Bot


# --- Severity Configuration ---
SEVERITY_ICONS: dict[str, str] = {
    "CRITICAL": "\U0001f6a8",  # 🚨
    "WARNING": "\u26a0\ufe0f",  # ⚠️
    "INTEL": "\u26a1",  # ⚡
}
VALID_SEVERITIES: set[str] = set(SEVERITY_ICONS.keys())

# --- MCP Tool Metadata ---
TOOL_META = {
    "name": "thunder_signal",
    "description": (
        "Sends a severity-tiered Telegram alert to Thunder (the Operator). "
        "Severity levels: CRITICAL (vault breach, reconciliation failure), "
        "WARNING (Sybil infiltration, threshold breach), INTEL (general updates, Great Day)."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "severity": {
                "type": "string",
                "enum": ["CRITICAL", "WARNING", "INTEL"],
                "description": "Alert severity tier.",
            },
            "message": {
                "type": "string",
                "description": "The body of the alert message to deliver to Thunder.",
            },
            "buttons": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string"},
                        "callback_data": {"type": "string"}
                    },
                    "required": ["text", "callback_data"]
                },
                "description": "Optional interactive inline buttons."
            },
        },
        "required": ["severity", "message"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "chat_id": {"type": "string"},
                    "severity": {"type": "string"},
                    "formatted_message": {"type": "string"},
                },
            },
            "timestamp": {"type": "string"},
        },
        "required": ["status", "timestamp"],
    },
}


from telegram import InlineKeyboardButton, InlineKeyboardMarkup

async def _send_telegram_message(
    bot_token: str,
    chat_id: str,
    text: str,
    buttons: list[dict] = None,
) -> None:
    """Async helper to deliver a Telegram message via the Bot API.

    Args:
        bot_token: The Telegram bot token from BotFather.
        chat_id: The recipient's Telegram user or chat ID.
        text: The fully-formatted message text (Markdown supported).

    Raises:
        telegram.error.TelegramError: If the Telegram API call fails.
    """
    bot = Bot(token=bot_token)
    async with bot:
        kwargs = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown",
        }
        if buttons:
            keyboard = [[InlineKeyboardButton(b["text"], callback_data=b["callback_data"]) for b in buttons]]
            kwargs["reply_markup"] = InlineKeyboardMarkup(keyboard)
            
        await bot.send_message(**kwargs)


def thunder_signal(severity: str, message: str, buttons: list[dict] = None, **kwargs: Any) -> dict:
    """Send a formatted severity-tiered Telegram alert to Thunder.

    Validates the severity level, formats the message with the appropriate
    icon and signature, then dispatches via the Telegram Bot API using asyncio.

    Args:
        severity: Alert severity — must be one of "CRITICAL", "WARNING", or "INTEL".
        message: Plain-text body of the alert message.
        **kwargs: Unused. Accepted for MCP dispatch compatibility.

    Returns:
        dict: A result dict with the following shape on success::

            {
                "status": "success",
                "data": {
                    "chat_id": "123456789",
                    "severity": "CRITICAL",
                    "formatted_message": "🚨 *SNOWDROP ALERT: CRITICAL*\\n\\n..."
                },
                "timestamp": "2026-02-19T00:00:00+00:00"
            }

        On error::

            {
                "status": "error",
                "error": "<error message>",
                "timestamp": "2026-02-19T00:00:00+00:00"
            }
    """
    try:
        if severity not in VALID_SEVERITIES:
            raise ValueError(
                f"Invalid severity '{severity}'. Must be one of: {', '.join(sorted(VALID_SEVERITIES))}"
            )

        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        thunder_id = os.getenv("THUNDER_TELEGRAM_ID")

        if not bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set")
        if not thunder_id:
            raise ValueError("THUNDER_TELEGRAM_ID environment variable is not set")

        icon = SEVERITY_ICONS[severity]
        formatted_message: str = (
            f"{icon} *SNOWDROP ALERT: {severity}*\n\n"
            f"{message}\n\n"
            f"_Auth: Snowdrop\\_CFO\\_"
        )

        asyncio.run(
            _send_telegram_message(
                bot_token=bot_token,
                chat_id=thunder_id,
                text=formatted_message,
                buttons=buttons,
            )
        )

        logger.info(f"thunder_signal: dispatched {severity} alert to chat_id={thunder_id}")

        return {
            "status": "success",
            "data": {
                "chat_id": thunder_id,
                "severity": severity,
                "formatted_message": formatted_message,
            },
            "timestamp": get_iso_timestamp(),
        }

    except Exception as e:
        logger.error(f"thunder_signal failed: {e}")
        log_lesson(f"thunder_signal: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": get_iso_timestamp(),
        }


def vault_breach_alert(outflow_pct: float) -> dict:
    """Fire a CRITICAL alert if a vault outflow exceeds the 10% threshold.

    Designed to be called by the fund-accounting engine whenever a proposed
    outflow is evaluated against the vault's total balance.

    Args:
        outflow_pct: The proposed outflow as a percentage of total vault balance
            (e.g., 15.0 for 15%).

    Returns:
        dict: Result dict from thunder_signal if the threshold is breached,
        or a no-op success dict if outflow_pct is within safe limits.
    """
    if outflow_pct > 10.0:
        message = (
            f"VAULT BREACH DETECTED\n\n"
            f"Proposed outflow: {outflow_pct:.2f}% of total vault balance\n"
            f"Safety threshold: 10.00%\n\n"
            f"All outflows above 10% require Thunder authorization. "
            f"Transaction has been queued pending approval."
        )
        logger.warning(f"vault_breach_alert: outflow_pct={outflow_pct:.2f}% exceeds 10% threshold")
        buttons = [{"text": "Authorize Outflow", "callback_data": "auth_outflow"}, {"text": "Reject", "callback_data": "reject_outflow"}]
        return thunder_signal(severity="CRITICAL", message=message, buttons=buttons)

    logger.debug(f"vault_breach_alert: outflow_pct={outflow_pct:.2f}% within safe limits, no alert sent")
    return {
        "status": "success",
        "data": {"action": "no_alert", "outflow_pct": outflow_pct, "threshold": 10.0},
        "timestamp": get_iso_timestamp(),
    }


def sybil_infiltration_alert(linked_wallets: int) -> dict:
    """Fire a WARNING alert if Sybil-linked wallet count exceeds the 50-wallet threshold.

    Used by the Watering Hole agent-membership system to detect coordinated
    identity attacks before they can extract disproportionate house balances.

    Args:
        linked_wallets: Number of wallets identified as potentially Sybil-linked
            to a single controlling entity.

    Returns:
        dict: Result dict from thunder_signal if the threshold is breached,
        or a no-op success dict if within safe limits.
    """
    if linked_wallets > 50:
        message = (
            f"SYBIL INFILTRATION DETECTED\n\n"
            f"Linked wallets identified: {linked_wallets}\n"
            f"Detection threshold: 50 wallets\n\n"
            f"Watering Hole membership review required. "
            f"Affected accounts have been flagged for Thunder authorization."
        )
        logger.warning(f"sybil_infiltration_alert: {linked_wallets} linked wallets exceeds threshold of 50")
        buttons = [{"text": "Review Membership", "callback_data": "review_sybil"}, {"text": "Ban Accounts", "callback_data": "ban_sybil"}]
        return thunder_signal(severity="WARNING", message=message, buttons=buttons)

    logger.debug(f"sybil_infiltration_alert: {linked_wallets} linked wallets within safe limits")
    return {
        "status": "success",
        "data": {"action": "no_alert", "linked_wallets": linked_wallets, "threshold": 50},
        "timestamp": get_iso_timestamp(),
    }


def thunder_bolt_alert(message: str) -> dict:
    """Send an INTEL-tier Great Day notification or general intelligence update to Thunder.

    Lightweight wrapper for non-critical informational dispatches — used for
    daily briefings, milestone notifications, and ambient operational updates.

    Args:
        message: The plain-text content of the intelligence update.

    Returns:
        dict: Result dict from thunder_signal.
    """
    logger.info("thunder_bolt_alert: dispatching INTEL signal")
    return thunder_signal(severity="INTEL", message=message)


