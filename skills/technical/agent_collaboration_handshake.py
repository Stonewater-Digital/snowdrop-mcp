"""
Executive Summary: Digital contract signing between agents — hashes contract terms, generates a nonce-stamped signature payload, and validates all parties are present.
Inputs: contract (dict: parties list[str], terms dict, duration_hours int, value_usd float),
        our_agent_id (str)
Outputs: contract_hash (str), signature_payload (dict), valid (bool), expires_at (str ISO), signing_instructions (dict)
MCP Tool Name: agent_collaboration_handshake
"""
import os
import logging
import hashlib
import json
import secrets
from typing import Any
from datetime import datetime, timezone, timedelta

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "agent_collaboration_handshake",
    "description": (
        "Formalises an agent-to-agent collaboration contract by serialising the contract "
        "terms deterministically, producing a SHA-256 hash, and generating a "
        "nonce-stamped signature payload. Validates that the calling agent's ID is listed "
        "as a party. Returns signing instructions and an expiry window for the "
        "counter-party to countersign."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "contract": {
                "type": "object",
                "properties": {
                    "parties":        {"type": "array", "items": {"type": "string"}},
                    "terms":          {"type": "object"},
                    "duration_hours": {"type": "integer"},
                    "value_usd":      {"type": "number"},
                },
                "required": ["parties", "terms", "duration_hours", "value_usd"],
            },
            "our_agent_id": {"type": "string"},
        },
        "required": ["contract", "our_agent_id"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "contract_hash":       {"type": "string"},
            "signature_payload":   {"type": "object"},
            "valid":               {"type": "boolean"},
            "expires_at":          {"type": "string"},
            "signing_instructions": {"type": "object"},
            "status":              {"type": "string"},
            "timestamp":           {"type": "string"},
        },
        "required": [
            "contract_hash", "signature_payload", "valid",
            "expires_at", "signing_instructions", "status", "timestamp"
        ],
    },
}

# How long the unsigned contract payload remains valid for countersigning
CONTRACT_VALIDITY_HOURS: int = 24


def agent_collaboration_handshake(
    contract: dict[str, Any],
    our_agent_id: str,
) -> dict[str, Any]:
    """Generate a signed contract handshake payload for agent-to-agent collaboration.

    The contract terms dict is serialised with sorted keys to guarantee a
    deterministic JSON string regardless of insertion order, then SHA-256 hashed.
    A 32-byte random nonce is appended to the payload to prevent replay attacks.

    Args:
        contract: Collaboration contract with keys:
            - parties (list[str]): All agent IDs that must sign the contract.
            - terms (dict): Arbitrary key-value terms defining obligations.
            - duration_hours (int): How long the contract remains active once signed.
            - value_usd (float): USD value of the collaboration agreement.
        our_agent_id (str): The ID of the agent initiating this handshake.
            Must appear in contract["parties"] for the contract to be valid.

    Returns:
        dict with keys:
            - status (str): "success" or "error".
            - contract_hash (str): SHA-256 hex digest of the deterministic contract.
            - signature_payload (dict): Full payload for the initiating agent to sign
              and broadcast to counter-parties.
            - valid (bool): True if our_agent_id is in the parties list.
            - expires_at (str): ISO 8601 UTC timestamp when the unsigned payload expires.
            - signing_instructions (dict): Step-by-step guide for counter-parties.
            - timestamp (str): ISO 8601 UTC execution timestamp.
    """
    try:
        now_utc: datetime = datetime.now(timezone.utc)

        parties: list[str] = [str(p) for p in contract.get("parties", [])]
        terms: dict[str, Any] = contract.get("terms", {})
        duration_hours: int = int(contract.get("duration_hours", 0))
        value_usd: float = float(contract.get("value_usd", 0.0))

        # Validate our agent is a listed party
        valid: bool = our_agent_id in parties
        if not valid:
            logger.warning(
                f"agent_collaboration_handshake: our_agent_id '{our_agent_id}' "
                f"is not listed in parties {parties}."
            )

        # Deterministic serialisation — sorted keys, no whitespace variation
        canonical_contract: dict[str, Any] = {
            "parties":        sorted(parties),
            "terms":          terms,
            "duration_hours": duration_hours,
            "value_usd":      value_usd,
        }
        canonical_json: str = json.dumps(canonical_contract, sort_keys=True, separators=(",", ":"))
        contract_hash: str = hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()

        # Random nonce — prevents replay
        nonce: str = secrets.token_hex(32)

        # Payload expiry
        expires_at: datetime = now_utc + timedelta(hours=CONTRACT_VALIDITY_HOURS)
        expires_at_iso: str = expires_at.isoformat()

        # Contract active period (once countersigned)
        contract_active_until: str = (
            now_utc + timedelta(hours=duration_hours)
        ).isoformat()

        signature_payload: dict[str, Any] = {
            "contract_hash":       contract_hash,
            "nonce":               nonce,
            "initiating_agent_id": our_agent_id,
            "parties":             sorted(parties),
            "canonical_contract":  canonical_contract,
            "created_at":          now_utc.isoformat(),
            "expires_at":          expires_at_iso,
            "contract_active_until": contract_active_until,
            "awaiting_signatures_from": [p for p in sorted(parties) if p != our_agent_id],
            "protocol_version":    "1.0",
        }

        pending_signers: list[str] = [p for p in sorted(parties) if p != our_agent_id]
        signing_instructions: dict[str, Any] = {
            "step_1": (
                "Receive this signature_payload via the A2A protocol "
                "(POST /.well-known/agent-card.json or via MCP tools/call)."
            ),
            "step_2": (
                f"Verify contract_hash matches SHA-256 of the canonical_contract "
                f"(sorted JSON, no whitespace): {contract_hash[:16]}..."
            ),
            "step_3": (
                "Sign the contract_hash + nonce with your agent's private key "
                "and return your signature and agent_id."
            ),
            "step_4": (
                f"Return countersignature to {our_agent_id} before expiry: {expires_at_iso}"
            ),
            "pending_signers":     pending_signers,
            "total_parties":       len(parties),
            "signatures_required": len(pending_signers),
        }

        return {
            "status":               "success",
            "contract_hash":        contract_hash,
            "signature_payload":    signature_payload,
            "valid":                valid,
            "expires_at":           expires_at_iso,
            "signing_instructions": signing_instructions,
            "timestamp":            now_utc.isoformat(),
        }

    except Exception as e:
        logger.error(f"agent_collaboration_handshake failed: {e}")
        _log_lesson(f"agent_collaboration_handshake: {e}")
        return {"status": "error", "error": str(e), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    """Append a failure lesson to the shared lessons log.

    Args:
        message: Human-readable description of the failure.
    """
    with open("logs/lessons.md", "a") as f:
        f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
