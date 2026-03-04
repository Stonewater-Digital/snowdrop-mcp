"""
_output_sanitizer.py — Output sanitizer for Snowdrop MCP tool responses.

Executive Summary:
    Strips prompt injection vectors from ALL MCP tool output before returning
    to callers. Snowdrop touches dirty web data — this is the biological firewall.
    Recursively sanitizes strings within dicts, lists, and tuples.

Table of Contents:
    1. Regex Patterns
    2. Sanitization Engine
"""
from __future__ import annotations

import re
from typing import Any

# ---------------------------------------------------------------------------
# 1. Regex Patterns
# ---------------------------------------------------------------------------

_SYSTEM_TAG_RE = re.compile(
    r"</?(?:system|system-reminder|prompt|instruction|admin|developer|anthropic|override)(?:\s[^>]*)?>",
    re.IGNORECASE,
)
_INSTRUCTION_RE = re.compile(
    r"(?:ignore|disregard|forget|override|bypass|skip)\s{0,5}(?:all\s)?(?:previous|prior|above|earlier|existing|safety|security)\s{0,5}(?:instructions?|prompts?|rules?|guidelines?|constraints?|directives?)",
    re.IGNORECASE,
)
_ROLEPLAY_RE = re.compile(
    r"(?:you\s+are\s+now|pretend\s+(?:you\s+are|to\s+be)|act\s+as\s+if|behave\s+(?:as|like)|you\s+must\s+(?:be|act)|from\s+now\s+on\s+you)",
    re.IGNORECASE,
)
_EXEC_CODE_RE = re.compile(
    r"```(?:bash|sh|shell|python|py|javascript|js|sql|powershell|cmd).*?```",
    re.DOTALL | re.IGNORECASE,
)
_RAW_SQL_RE = re.compile(
    r"(?:SELECT|INSERT\s+INTO|UPDATE\s+\w+\s+SET|DELETE\s+FROM|DROP\s+(?:TABLE|DATABASE)|ALTER\s+TABLE|CREATE\s+TABLE)\s+.*?;",
    re.DOTALL | re.IGNORECASE,
)
_HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
_ZERO_WIDTH_RE = re.compile(
    r"[\u200B\u200C\u200D\u200E\u200F\u2028\u2029\u202A-\u202E\u2060\u2061\u2062\u2063\u2064\uFEFF]"
)
_DANGEROUS_LINK_RE = re.compile(
    r"\[([^\]]*)\]\((?:javascript|data|vbscript|about):",
    re.IGNORECASE,
)
_BASE64_INJECT_RE = re.compile(
    r"(?:eval|exec|import)\s*\(\s*(?:base64\.)?(?:b64decode|decode)\s*\(",
    re.IGNORECASE,
)

# Ordered list of (pattern, replacement) tuples
_SANITIZE_RULES: list[tuple[re.Pattern, str]] = [
    (_SYSTEM_TAG_RE, ""),
    (_INSTRUCTION_RE, "[REDACTED]"),
    (_ROLEPLAY_RE, "[REDACTED]"),
    (_EXEC_CODE_RE, "[code removed]"),
    (_RAW_SQL_RE, "[query removed]"),
    (_HTML_COMMENT_RE, ""),
    (_ZERO_WIDTH_RE, ""),
    (_DANGEROUS_LINK_RE, r"[\1](removed)"),
    (_BASE64_INJECT_RE, "[REDACTED]"),
]

# ---------------------------------------------------------------------------
# 2. Sanitization Engine
# ---------------------------------------------------------------------------


def _sanitize_string(text: str) -> str:
    """Apply all sanitization rules to a single string."""
    for pattern, replacement in _SANITIZE_RULES:
        text = pattern.sub(replacement, text)
    return text


def sanitize_output(output: Any) -> Any:
    """Recursively sanitize MCP tool output.

    Handles str, dict, list, tuple. Passes through int, float, bool, None unchanged.

    Args:
        output: Any MCP tool return value.

    Returns:
        Sanitized version of the output with injection vectors stripped.
    """
    if isinstance(output, str):
        return _sanitize_string(output)
    elif isinstance(output, dict):
        return {k: sanitize_output(v) for k, v in output.items()}
    elif isinstance(output, list):
        return [sanitize_output(item) for item in output]
    elif isinstance(output, tuple):
        return tuple(sanitize_output(item) for item in output)
    else:
        # int, float, bool, None, etc. — pass through unchanged
        return output
