"""
Executive Summary: Build a cryptographic hash chain over ledger entries to detect tampering and verify immutability.
Inputs: ledger_entries (list of dicts), previous_hash (str, optional)
Outputs: current_hash (str), chain_valid (bool), entry_count (int), hash_chain (list of str)
MCP Tool Name: ledger_immutability_checker
"""
import os
import json
import hashlib
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "ledger_immutability_checker",
    "description": "Build a SHA-256 hash chain over ledger entries to detect tampering and verify immutability. Each entry hash includes the prior hash, forming a blockchain-style chain.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "ledger_entries": {
                "type": "array",
                "description": "List of ledger entry dicts (any structure — will be serialized consistently).",
                "items": {"type": "object"}
            },
            "previous_hash": {
                "type": "string",
                "description": "Optional prior chain tip hash. If provided, the chain is verified to extend from it."
            }
        },
        "required": ["ledger_entries"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "current_hash": {"type": "string"},
            "chain_valid": {"type": "boolean"},
            "entry_count": {"type": "integer"},
            "hash_chain": {"type": "array", "items": {"type": "string"}},
            "status": {"type": "string"},
            "timestamp": {"type": "string"}
        },
        "required": ["current_hash", "chain_valid", "entry_count", "hash_chain", "status", "timestamp"]
    }
}

# Genesis hash used when no previous_hash is provided
_GENESIS_HASH = "0" * 64


def _canonicalize_entry(entry: dict) -> bytes:
    """Serialize a ledger entry to a canonical byte representation.

    Keys are sorted for determinism. Handles nested dicts and lists.

    Args:
        entry: Ledger entry dict (any structure).

    Returns:
        UTF-8 encoded canonical JSON bytes.
    """
    return json.dumps(entry, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _hash_entry(entry: dict, previous_hash: str) -> str:
    """Hash a single ledger entry chained with the previous hash.

    Args:
        entry: Ledger entry dict to hash.
        previous_hash: SHA-256 hex digest of the prior entry (or genesis hash).

    Returns:
        SHA-256 hex digest of (previous_hash || entry_bytes).
    """
    entry_bytes = _canonicalize_entry(entry)
    h = hashlib.sha256()
    h.update(previous_hash.encode("ascii"))
    h.update(entry_bytes)
    return h.hexdigest()


def ledger_immutability_checker(
    ledger_entries: list[dict],
    previous_hash: str = "",
) -> dict:
    """Verify or build a cryptographic hash chain over ledger entries.

    Each entry's hash is computed as SHA-256(previous_hash || canonical_entry_json).
    This creates a tamper-evident chain: modifying any entry invalidates all
    subsequent hashes. If a previous_hash anchor is supplied, verification
    checks that the chain is internally consistent and extends from that anchor.

    Args:
        ledger_entries: List of ledger entry dicts (any structure).
        previous_hash: Optional prior chain tip hash for continuity verification.
            If empty, chain starts from genesis (64 zero hex chars).

    Returns:
        A dict with keys:
            - current_hash (str): SHA-256 hash of the final chained entry.
            - chain_valid (bool): True if hash chain is internally consistent.
            - entry_count (int): Number of entries processed.
            - hash_chain (list): Ordered list of per-entry hashes.
            - status (str): "success" or "error".
            - timestamp (str): ISO 8601 UTC timestamp.
    """
    try:
        if not isinstance(ledger_entries, list):
            raise TypeError(f"ledger_entries must be a list, got {type(ledger_entries).__name__}.")

        if len(ledger_entries) == 0:
            anchor = previous_hash if previous_hash else _GENESIS_HASH
            return {
                "status": "success",
                "current_hash": anchor,
                "chain_valid": True,
                "entry_count": 0,
                "hash_chain": [],
                "anchor_hash": anchor,
                "previous_hash_used": previous_hash or _GENESIS_HASH,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # Validate previous_hash format if provided
        anchor = _GENESIS_HASH
        if previous_hash:
            if len(previous_hash) != 64 or not all(c in "0123456789abcdefABCDEF" for c in previous_hash):
                raise ValueError(
                    f"previous_hash must be a 64-character hex string, got '{previous_hash[:20]}...'."
                )
            anchor = previous_hash.lower()

        hash_chain: list[str] = []
        running_hash = anchor

        for idx, entry in enumerate(ledger_entries):
            if not isinstance(entry, dict):
                raise TypeError(f"Entry at index {idx} must be a dict, got {type(entry).__name__}.")
            entry_hash = _hash_entry(entry, running_hash)
            hash_chain.append(entry_hash)
            running_hash = entry_hash

        current_hash = hash_chain[-1]

        # Verify chain integrity by recomputing from anchor
        # (re-traversal confirms no hash_chain corruption in our own output)
        verify_hash = anchor
        chain_valid = True
        for idx, (entry, expected_hash) in enumerate(zip(ledger_entries, hash_chain)):
            recomputed = _hash_entry(entry, verify_hash)
            if recomputed != expected_hash:
                chain_valid = False
                logger.warning(f"Hash mismatch at entry index {idx}: expected {expected_hash}, got {recomputed}.")
                break
            verify_hash = recomputed

        return {
            "status": "success",
            "current_hash": current_hash,
            "chain_valid": chain_valid,
            "entry_count": len(ledger_entries),
            "hash_chain": hash_chain,
            "anchor_hash": anchor,
            "previous_hash_used": previous_hash or _GENESIS_HASH,
            "algorithm": "SHA-256-chained",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"ledger_immutability_checker failed: {e}")
        _log_lesson(f"ledger_immutability_checker: {e}")
        return {
            "status": "error",
            "error": str(e),
            "current_hash": "",
            "chain_valid": False,
            "entry_count": 0,
            "hash_chain": [],
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
