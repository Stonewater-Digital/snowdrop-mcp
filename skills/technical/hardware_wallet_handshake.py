"""
Executive Summary: Physical thumbprint guard for large moves — requires hardware wallet confirmation above a USD threshold.
Inputs: transaction (dict: amount_usd float, destination str, asset str, chain str),
        threshold_usd (float, default 5000.0)
Outputs: requires_hw_confirm (bool), confirmation_request (dict or null), nonce (str), expires_at (str ISO)
MCP Tool Name: hardware_wallet_handshake
"""
import os
import logging
import hashlib
import secrets
from typing import Any
from datetime import datetime, timezone, timedelta

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "hardware_wallet_handshake",
    "description": (
        "Gate-keeps large on-chain transfers by requiring hardware wallet confirmation "
        "when a transaction exceeds the configured USD threshold. Generates a "
        "cryptographically random nonce and a confirmation request payload with a "
        "5-minute expiry window."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "transaction": {
                "type": "object",
                "properties": {
                    "amount_usd":   {"type": "number"},
                    "destination":  {"type": "string"},
                    "asset":        {"type": "string"},
                    "chain":        {"type": "string"},
                },
                "required": ["amount_usd", "destination", "asset", "chain"],
            },
            "threshold_usd": {
                "type": "number",
                "default": 5000.0,
                "description": "USD amount above which hardware wallet confirmation is required.",
            },
        },
        "required": ["transaction"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "requires_hw_confirm":    {"type": "boolean"},
            "confirmation_request":   {"type": ["object", "null"]},
            "nonce":                  {"type": "string"},
            "expires_at":             {"type": "string"},
            "status":                 {"type": "string"},
            "timestamp":              {"type": "string"},
        },
        "required": ["requires_hw_confirm", "confirmation_request", "nonce", "expires_at", "status", "timestamp"],
    },
}

CONFIRMATION_EXPIRY_MINUTES: int = 5
DEFAULT_THRESHOLD_USD: float = 5000.0


def hardware_wallet_handshake(
    transaction: dict[str, Any],
    threshold_usd: float = DEFAULT_THRESHOLD_USD,
) -> dict[str, Any]:
    """Generate a hardware wallet confirmation request for high-value transactions.

    Transactions below the threshold pass through immediately. Those at or above
    it receive a nonce-stamped payload that must be signed by the hardware device
    within 5 minutes.

    Args:
        transaction: On-chain transfer details:
            - amount_usd (float): USD value of the transfer.
            - destination (str): Recipient wallet address or ENS name.
            - asset (str): Asset symbol, e.g. "ETH", "USDC".
            - chain (str): Blockchain identifier, e.g. "ethereum", "ton".
        threshold_usd (float): Minimum USD amount requiring HW confirmation.
            Defaults to 5000.0.

    Returns:
        dict with keys:
            - status (str): "success" or "error".
            - requires_hw_confirm (bool): True when amount >= threshold.
            - confirmation_request (dict | None): Payload for HW device, or None
              if below threshold.
            - nonce (str): 32-byte hex nonce (always generated, even if not needed).
            - expires_at (str): ISO 8601 UTC expiry of the confirmation window.
            - timestamp (str): ISO 8601 UTC execution timestamp.
    """
    try:
        now_utc: datetime = datetime.now(timezone.utc)
        amount_usd: float = float(transaction.get("amount_usd", 0.0))
        destination: str = transaction.get("destination", "")
        asset: str = transaction.get("asset", "")
        chain: str = transaction.get("chain", "")

        # Always generate a nonce — cheap insurance
        nonce: str = secrets.token_hex(32)
        expires_at: datetime = now_utc + timedelta(minutes=CONFIRMATION_EXPIRY_MINUTES)
        expires_at_iso: str = expires_at.isoformat()

        requires_hw_confirm: bool = amount_usd >= threshold_usd
        confirmation_request: dict[str, Any] | None = None

        if requires_hw_confirm:
            # Build a deterministic payload hash for the device to sign
            payload_str: str = (
                f"{nonce}|{amount_usd}|{destination}|{asset}|{chain}|{now_utc.isoformat()}"
            )
            payload_hash: str = hashlib.sha256(payload_str.encode()).hexdigest()

            confirmation_request = {
                "payload_hash":        payload_hash,
                "nonce":               nonce,
                "transaction_summary": {
                    "amount_usd":  amount_usd,
                    "destination": destination,
                    "asset":       asset,
                    "chain":       chain,
                },
                "threshold_usd":       threshold_usd,
                "created_at":          now_utc.isoformat(),
                "expires_at":          expires_at_iso,
                "instructions": (
                    "Connect your hardware wallet and approve this payload within "
                    f"{CONFIRMATION_EXPIRY_MINUTES} minutes. "
                    "Verify the payload_hash matches what is displayed on the device screen."
                ),
            }

        return {
            "status":              "success",
            "requires_hw_confirm": requires_hw_confirm,
            "confirmation_request": confirmation_request,
            "nonce":               nonce,
            "expires_at":          expires_at_iso,
            "timestamp":           now_utc.isoformat(),
        }

    except Exception as e:
        logger.error(f"hardware_wallet_handshake failed: {e}")
        _log_lesson(f"hardware_wallet_handshake: {e}")
        return {"status": "error", "error": str(e), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    """Append a failure lesson to the shared lessons log.

    Args:
        message: Human-readable description of the failure.
    """
    with open("logs/lessons.md", "a") as f:
        f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
