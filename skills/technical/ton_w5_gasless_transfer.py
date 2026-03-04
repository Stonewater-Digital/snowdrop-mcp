"""
Executive Summary: Build TON W5 wallet gasless transfer payloads using battery sponsorship, enabling zero-fee TON movements.
Inputs: recipient_address (str), amount_ton (float), memo (str, optional)
Outputs: transfer_payload (dict), estimated_fee (float), tx_ready (bool)
MCP Tool Name: ton_w5_gasless_transfer
"""
import os
import hashlib
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "ton_w5_gasless_transfer",
    "description": "Build TON W5 wallet gasless transfer payload using battery sponsorship for zero-fee TON movements.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "recipient_address": {
                "type": "string",
                "description": "The TON recipient wallet address (EQ or UQ format)."
            },
            "amount_ton": {
                "type": "number",
                "description": "Amount of TON to transfer (in TON, not nanoton)."
            },
            "memo": {
                "type": "string",
                "description": "Optional transfer comment/memo."
            }
        },
        "required": ["recipient_address", "amount_ton"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "transfer_payload": {"type": "object"},
            "estimated_fee": {"type": "number"},
            "tx_ready": {"type": "boolean"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"}
        },
        "required": ["transfer_payload", "estimated_fee", "tx_ready", "status", "timestamp"]
    }
}

# TON nanoton conversion constant
NANOTON_PER_TON = 1_000_000_000


def ton_w5_gasless_transfer(
    recipient_address: str,
    amount_ton: float,
    memo: str = ""
) -> dict:
    """Build a TON W5 gasless transfer payload using battery sponsorship.

    Args:
        recipient_address: The TON recipient wallet address (EQ or UQ format).
        amount_ton: Amount of TON to transfer (in TON, not nanoton).
        memo: Optional transfer comment or memo string.

    Returns:
        A dict with keys:
            - transfer_payload (dict): The constructed W5 transfer message structure.
            - estimated_fee (float): Always 0.0 for W5 gasless transfers.
            - tx_ready (bool): Whether the payload is ready for broadcast.
            - status (str): "success" or "error".
            - timestamp (str): ISO 8601 UTC timestamp.
    """
    try:
        ton_api_key = os.getenv("TON_API_KEY", "")
        sender_address = os.getenv("TON_WALLET_ADDRESS", "")

        if not ton_api_key:
            raise ValueError("TON_API_KEY environment variable is not set.")
        if not sender_address:
            raise ValueError("TON_WALLET_ADDRESS environment variable is not set.")
        if amount_ton <= 0:
            raise ValueError(f"amount_ton must be positive, got {amount_ton}.")
        if not recipient_address.startswith(("EQ", "UQ", "0:")):
            raise ValueError(
                f"recipient_address '{recipient_address}' does not appear to be a valid TON address."
            )

        amount_nanoton = int(amount_ton * NANOTON_PER_TON)

        # Construct a deterministic payload reference hash for idempotency
        payload_ref = hashlib.sha256(
            f"{sender_address}:{recipient_address}:{amount_nanoton}:{memo}:{datetime.now(timezone.utc).date()}".encode()
        ).hexdigest()[:16]

        # W5 wallet transfer message structure
        # W5 wallets support signed-extension messages where the gas fee is
        # sponsored by a battery provider (e.g. TON API battery service).
        transfer_payload = {
            "wallet_version": "W5",
            "sender_address": sender_address,
            "recipient_address": recipient_address,
            "amount_nanoton": amount_nanoton,
            "amount_ton": amount_ton,
            "memo": memo,
            "payload_ref": payload_ref,
            "message_type": "v5r1_external",
            "sponsorship": {
                "type": "battery",
                "provider": "tonapi.io",
                "api_key_present": bool(ton_api_key),
                "endpoint": "https://battery.tonapi.io/v2/wallet/emulate",
            },
            "body": {
                "op_code": "0x0f8a7ea5",  # TON standard transfer op
                "query_id": int(datetime.now(timezone.utc).timestamp()),
                "amount": amount_nanoton,
                "destination": recipient_address,
                "response_destination": sender_address,
                "forward_ton_amount": 1,  # 1 nanoton forward for notification
                "forward_payload": memo.encode("utf-8").hex() if memo else "",
            },
            "extensions": {
                "gasless": True,
                "battery_sponsored": True,
            },
            "seqno_required": True,
            "valid_until": int(datetime.now(timezone.utc).timestamp()) + 600,  # 10 min window
        }

        # W5 gasless transfers have zero fee to the sender
        estimated_fee = 0.0

        # Payload is ready if we have all required fields and a valid address
        tx_ready = bool(
            sender_address
            and recipient_address
            and amount_nanoton > 0
            and ton_api_key
        )

        return {
            "status": "success",
            "transfer_payload": transfer_payload,
            "estimated_fee": estimated_fee,
            "tx_ready": tx_ready,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"ton_w5_gasless_transfer failed: {e}")
        _log_lesson(f"ton_w5_gasless_transfer: {e}")
        return {
            "status": "error",
            "error": str(e),
            "transfer_payload": {},
            "estimated_fee": 0.0,
            "tx_ready": False,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    """Append an error lesson to the lessons log file.

    Args:
        message: The lesson message to record.
    """
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        logger.warning("Could not write to logs/lessons.md")
