"""
Executive Summary: MPC-style key shard management using Shamir's Secret Sharing concept for split, reconstruct, and verify operations.
Inputs: action (str), key_data (str), shards (list of str), threshold (int), total_shards (int)
Outputs: action_result (dict), threshold (int), total (int)
MCP Tool Name: private_key_shard_manager
"""
import os
import hashlib
import hmac
import logging
import secrets
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "private_key_shard_manager",
    "description": "MPC key shard management using Shamir's Secret Sharing: split a key into N shards (K-of-N required to reconstruct), reconstruct from K shards, or verify shard validity.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["split", "reconstruct", "verify"],
                "description": "Operation to perform: 'split', 'reconstruct', or 'verify'."
            },
            "key_data": {
                "type": "string",
                "description": "The key or secret to split (required for 'split' action)."
            },
            "shards": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of shard strings (required for 'reconstruct' and 'verify' actions)."
            },
            "threshold": {
                "type": "integer",
                "description": "Minimum number of shards required to reconstruct (K)."
            },
            "total_shards": {
                "type": "integer",
                "description": "Total number of shards to generate (N)."
            }
        },
        "required": ["action", "threshold", "total_shards"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "action_result": {"type": "object"},
            "threshold": {"type": "integer"},
            "total": {"type": "integer"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"}
        },
        "required": ["action_result", "threshold", "total", "status", "timestamp"]
    }
}

# GF(2^8) prime polynomial for Galois Field arithmetic (AES uses this)
_GF_PRIME = 0x11B
_GF_SIZE = 256


def _gf_multiply(a: int, b: int) -> int:
    """Multiply two elements in GF(2^8).

    Args:
        a: First GF(2^8) element.
        b: Second GF(2^8) element.

    Returns:
        Product in GF(2^8).
    """
    result = 0
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        if a & 0x100:
            a ^= _GF_PRIME
        b >>= 1
    return result & 0xFF


def _gf_pow(base: int, exp: int) -> int:
    """Compute base^exp in GF(2^8).

    Args:
        base: Base element.
        exp: Exponent.

    Returns:
        Result in GF(2^8).
    """
    result = 1
    for _ in range(exp):
        result = _gf_multiply(result, base)
    return result


def _gf_div(a: int, b: int) -> int:
    """Divide a by b in GF(2^8).

    Args:
        a: Dividend.
        b: Divisor (must be non-zero).

    Returns:
        Quotient in GF(2^8).

    Raises:
        ZeroDivisionError: If divisor is zero.
    """
    if b == 0:
        raise ZeroDivisionError("Division by zero in GF(2^8).")
    if a == 0:
        return 0
    return _gf_pow(b, _GF_SIZE - 2) and _gf_multiply(a, _gf_pow(b, _GF_SIZE - 2))


def _split_secret_byte(secret_byte: int, threshold: int, total_shards: int) -> list[tuple[int, int]]:
    """Split a single byte using Shamir's Secret Sharing over GF(2^8).

    Constructs a random polynomial of degree (threshold-1) with the secret
    as the constant term, then evaluates it at x=1..total_shards.

    Args:
        secret_byte: The byte value (0-255) to split.
        threshold: Minimum shares needed to reconstruct (K).
        total_shards: Total shares to generate (N).

    Returns:
        List of (x, y) share tuples where x is 1-indexed shard number.
    """
    # Generate random polynomial coefficients [secret, a1, a2, ..., a_{k-1}]
    coefficients = [secret_byte] + [secrets.randbelow(256) for _ in range(threshold - 1)]

    shares = []
    for x in range(1, total_shards + 1):
        y = 0
        for i, coeff in enumerate(coefficients):
            y ^= _gf_multiply(coeff, _gf_pow(x, i))
        shares.append((x, y))
    return shares


def _reconstruct_secret_byte(shares: list[tuple[int, int]]) -> int:
    """Reconstruct a single byte using Lagrange interpolation over GF(2^8).

    Args:
        shares: List of (x, y) share tuples (at least threshold shares).

    Returns:
        Reconstructed secret byte value.
    """
    secret = 0
    for i, (xi, yi) in enumerate(shares):
        numerator = yi
        denominator = 1
        for j, (xj, _) in enumerate(shares):
            if i != j:
                numerator = _gf_multiply(numerator, xj)
                denominator = _gf_multiply(denominator, xi ^ xj)
        secret ^= _gf_multiply(numerator, _gf_pow(denominator, _GF_SIZE - 2))
    return secret


def _encode_shard(shard_index: int, byte_shares: list[tuple[int, int]]) -> str:
    """Encode a shard as a hex string with index prefix.

    Format: "<index_hex2><byte0_y_hex2><byte1_y_hex2>..."

    Args:
        shard_index: The 1-indexed shard number.
        byte_shares: List of (x, y) pairs — one per secret byte.

    Returns:
        Hex-encoded shard string.
    """
    y_values = bytes([y for (_, y) in byte_shares])
    return f"{shard_index:02x}" + y_values.hex()


def _decode_shard(shard_hex: str) -> tuple[int, bytes]:
    """Decode a hex shard string back to index and y-values.

    Args:
        shard_hex: The hex-encoded shard string.

    Returns:
        Tuple of (shard_index, y_values_bytes).

    Raises:
        ValueError: If the shard format is invalid.
    """
    if len(shard_hex) < 4:
        raise ValueError(f"Shard too short to be valid: '{shard_hex}'.")
    try:
        index = int(shard_hex[:2], 16)
        y_bytes = bytes.fromhex(shard_hex[2:])
    except ValueError as exc:
        raise ValueError(f"Invalid shard hex encoding: {exc}") from exc
    return index, y_bytes


def _split_key(key_data: str, threshold: int, total_shards: int) -> dict:
    """Split a key string into N shards with K-of-N reconstruction.

    Args:
        key_data: The secret key string to split.
        threshold: Minimum shares required to reconstruct (K).
        total_shards: Total number of shards (N).

    Returns:
        Dict containing shards list, threshold, total, and key_hash for verification.
    """
    secret_bytes = key_data.encode("utf-8")
    n_bytes = len(secret_bytes)

    # Split each byte independently
    all_shard_bytes: list[list[tuple[int, int]]] = []
    for byte_val in secret_bytes:
        byte_shares = _split_secret_byte(byte_val, threshold, total_shards)
        all_shard_bytes.append(byte_shares)

    # Reorganize: all_shard_bytes[byte_i][shard_j] → shards[shard_j][byte_i]
    shards = []
    for shard_j in range(total_shards):
        shard_byte_shares = [(all_shard_bytes[byte_i][shard_j]) for byte_i in range(n_bytes)]
        shards.append(_encode_shard(shard_j + 1, shard_byte_shares))

    key_hash = hashlib.sha256(secret_bytes).hexdigest()

    return {
        "shards": shards,
        "threshold": threshold,
        "total_shards": total_shards,
        "key_hash": key_hash,
        "secret_length_bytes": n_bytes,
        "algorithm": "Shamir-GF256",
    }


def _reconstruct_key(shards: list[str], threshold: int) -> dict:
    """Reconstruct the secret from K or more shards.

    Args:
        shards: List of hex-encoded shard strings.
        threshold: Minimum K value used during splitting.

    Returns:
        Dict containing reconstructed key and verification hash.

    Raises:
        ValueError: If fewer than threshold shards are provided or shards are inconsistent.
    """
    if len(shards) < threshold:
        raise ValueError(
            f"Need at least {threshold} shards, got {len(shards)}."
        )

    decoded = [_decode_shard(s) for s in shards[:threshold]]
    n_bytes = len(decoded[0][1])

    # Verify all shards have the same byte length
    for idx, (_, y_bytes) in enumerate(decoded):
        if len(y_bytes) != n_bytes:
            raise ValueError(
                f"Shard {idx} has {len(y_bytes)} bytes, expected {n_bytes}."
            )

    # Reconstruct each byte
    reconstructed = bytearray()
    for byte_i in range(n_bytes):
        shares_for_byte = [(decoded[j][0], decoded[j][1][byte_i]) for j in range(threshold)]
        reconstructed.append(_reconstruct_secret_byte(shares_for_byte))

    secret = reconstructed.decode("utf-8")
    key_hash = hashlib.sha256(reconstructed).hexdigest()

    return {
        "reconstructed_key": secret,
        "key_hash": key_hash,
        "shards_used": threshold,
        "algorithm": "Shamir-GF256",
    }


def _verify_shards(shards: list[str], threshold: int, total_shards: int) -> dict:
    """Verify shard format validity and basic consistency.

    Args:
        shards: List of hex-encoded shard strings to verify.
        threshold: Expected K threshold.
        total_shards: Expected N total shards.

    Returns:
        Dict containing validity status and per-shard details.
    """
    results = []
    valid_count = 0
    expected_length: int | None = None

    for i, shard in enumerate(shards):
        try:
            index, y_bytes = _decode_shard(shard)
            length = len(y_bytes)

            if expected_length is None:
                expected_length = length

            length_consistent = (length == expected_length)
            index_in_range = 1 <= index <= total_shards

            valid = length_consistent and index_in_range and length > 0
            if valid:
                valid_count += 1

            results.append({
                "shard_index": i,
                "encoded_index": index,
                "byte_length": length,
                "length_consistent": length_consistent,
                "index_in_range": index_in_range,
                "valid": valid,
            })
        except ValueError as exc:
            results.append({
                "shard_index": i,
                "valid": False,
                "error": str(exc),
            })

    enough_for_threshold = valid_count >= threshold

    return {
        "valid": enough_for_threshold,
        "valid_shard_count": valid_count,
        "total_shards_checked": len(shards),
        "threshold_met": enough_for_threshold,
        "per_shard": results,
    }


def private_key_shard_manager(
    action: str,
    threshold: int,
    total_shards: int,
    key_data: str = "",
    shards: list[str] | None = None,
) -> dict:
    """Perform MPC key shard operations: split, reconstruct, or verify.

    Uses Shamir's Secret Sharing over GF(2^8) for cryptographically secure
    key splitting. A K-of-N scheme means any K shards can reconstruct the
    secret, but fewer than K shards reveal zero information.

    Args:
        action: Operation to perform — "split", "reconstruct", or "verify".
        threshold: Minimum number of shards required to reconstruct (K).
        total_shards: Total number of shards to generate (N).
        key_data: The secret key string to split (required for "split").
        shards: List of hex-encoded shard strings (required for "reconstruct"/"verify").

    Returns:
        A dict with keys:
            - action_result (dict): Shards list (split), key (reconstruct), valid bool (verify).
            - threshold (int): The K value used.
            - total (int): The N value used.
            - status (str): "success" or "error".
            - timestamp (str): ISO 8601 UTC timestamp.
    """
    try:
        action = action.strip().lower()
        if action not in ("split", "reconstruct", "verify"):
            raise ValueError(f"action must be 'split', 'reconstruct', or 'verify', got '{action}'.")
        if threshold < 2:
            raise ValueError(f"threshold must be >= 2, got {threshold}.")
        if total_shards < threshold:
            raise ValueError(
                f"total_shards ({total_shards}) must be >= threshold ({threshold})."
            )
        if total_shards > 254:
            raise ValueError("total_shards cannot exceed 254 (GF(2^8) constraint).")

        if action == "split":
            if not key_data:
                raise ValueError("key_data is required for 'split' action.")
            result = _split_key(key_data, threshold, total_shards)

        elif action == "reconstruct":
            if not shards:
                raise ValueError("shards list is required for 'reconstruct' action.")
            result = _reconstruct_key(shards, threshold)

        elif action == "verify":
            if not shards:
                raise ValueError("shards list is required for 'verify' action.")
            result = _verify_shards(shards, threshold, total_shards)

        return {
            "status": "success",
            "action": action,
            "action_result": result,
            "threshold": threshold,
            "total": total_shards,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"private_key_shard_manager failed: {e}")
        _log_lesson(f"private_key_shard_manager: {e}")
        return {
            "status": "error",
            "error": str(e),
            "action_result": {},
            "threshold": threshold,
            "total": total_shards,
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
