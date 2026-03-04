"""Compute a cryptographic hash of string content.

MCP Tool Name: file_hash_calculator
"""
from __future__ import annotations
import hashlib
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "file_hash_calculator",
    "description": "Compute a cryptographic hash (SHA-256, SHA-1, MD5, SHA-512, etc.) of the given string content. Returns the hex digest.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "content": {
                "type": "string",
                "description": "The string content to hash.",
            },
            "algorithm": {
                "type": "string",
                "description": "Hash algorithm to use.",
                "enum": ["sha256", "sha1", "md5", "sha512", "sha384", "sha224"],
                "default": "sha256",
            },
        },
        "required": ["content"],
    },
}

_SUPPORTED = {"sha256", "sha1", "md5", "sha512", "sha384", "sha224"}


def file_hash_calculator(
    content: str,
    algorithm: str = "sha256",
) -> dict[str, Any]:
    """Compute hash of string content."""
    try:
        algorithm = algorithm.lower().strip()
        if algorithm not in _SUPPORTED:
            return {
                "status": "error",
                "data": {"error": f"Unsupported algorithm '{algorithm}'. Supported: {sorted(_SUPPORTED)}"},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        h = hashlib.new(algorithm)
        content_bytes = content.encode("utf-8")
        h.update(content_bytes)
        hex_digest = h.hexdigest()

        return {
            "status": "ok",
            "data": {
                "algorithm": algorithm,
                "hex_digest": hex_digest,
                "digest_length_chars": len(hex_digest),
                "content_length_bytes": len(content_bytes),
                "content_length_chars": len(content),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
