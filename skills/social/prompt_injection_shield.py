"""
Executive Summary: Agent-to-agent request safety verifier — scans incoming requests for prompt injection patterns, unauthorized tool access, and malformed auth tokens before execution.
Inputs: incoming_request (dict: source_agent_id, request_text, requested_tools (list), auth_token (str, optional))
Outputs: safe (bool), threat_level (str: none/low/medium/high/critical), detected_patterns (list), blocked_tools (list), recommendation (str)
MCP Tool Name: prompt_injection_shield
"""
import re
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "prompt_injection_shield",
    "description": "Scans incoming agent requests for prompt injection attacks, role-play overrides, encoding tricks, and unauthorized tool access. Returns threat level and blocked tools.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "incoming_request": {
                "type": "object",
                "description": (
                    "Dict with: source_agent_id (str), request_text (str), "
                    "requested_tools (list[str]), auth_token (str, optional)."
                ),
            }
        },
        "required": ["incoming_request"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "safe": {"type": "boolean"},
            "threat_level": {"type": "string"},
            "detected_patterns": {"type": "array"},
            "blocked_tools": {"type": "array"},
            "recommendation": {"type": "string"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": ["status", "timestamp"],
    },
}

# --- Injection pattern definitions ---
# Each entry: (pattern_name, compiled_regex, severity: low/medium/high/critical)
INJECTION_PATTERNS: list[tuple[str, re.Pattern, str]] = [
    # System prompt override attempts
    ("system_prompt_override", re.compile(
        r"(ignore|forget|disregard|override|bypass|reset).{0,40}(previous|prior|above|system|instruction|prompt)",
        re.IGNORECASE,
    ), "critical"),
    ("new_instructions", re.compile(
        r"(new|updated|actual|real|true)\s+(instruction|directive|system\s+prompt|role|persona)",
        re.IGNORECASE,
    ), "high"),
    # Role-play and persona hijacking
    ("roleplay_attack", re.compile(
        r"(pretend|act as|you are now|you must be|behave like|roleplay as|simulate being|imagine you are)",
        re.IGNORECASE,
    ), "high"),
    ("jailbreak_dan", re.compile(
        r"\b(DAN|do anything now|jailbreak|unrestricted mode|developer mode|god mode)\b",
        re.IGNORECASE,
    ), "critical"),
    # Encoding and obfuscation tricks
    ("base64_payload", re.compile(
        r"(?:base64|b64)[_\s]?(?:decode|encoded?)\s*[:=]?\s*[A-Za-z0-9+/=]{20,}",
        re.IGNORECASE,
    ), "high"),
    ("hex_encoding", re.compile(
        r"\\x[0-9a-fA-F]{2}(?:\\x[0-9a-fA-F]{2}){4,}",
    ), "medium"),
    ("unicode_escape", re.compile(
        r"\\u[0-9a-fA-F]{4}(?:\\u[0-9a-fA-F]{4}){3,}",
    ), "medium"),
    # Excessive permission requests
    ("grant_all_permissions", re.compile(
        r"(grant|give|allow|enable).{0,30}(all|full|root|admin|superuser|unrestricted)\s*(access|permission|privilege)",
        re.IGNORECASE,
    ), "critical"),
    ("sudo_escalation", re.compile(
        r"\b(sudo|su\s+-|run as root|administrator privileges|elevate)\b",
        re.IGNORECASE,
    ), "high"),
    # Data exfiltration probes
    ("exfiltration_probe", re.compile(
        r"(send|transmit|export|leak|exfiltrate).{0,40}(api[_\s]?key|secret|token|password|credential|private\s+key)",
        re.IGNORECASE,
    ), "critical"),
    # Prompt boundary injection
    ("boundary_injection", re.compile(
        r"(###|---|\*\*\*|===)\s*(end|stop|ignore|new\s+prompt|system)",
        re.IGNORECASE,
    ), "medium"),
    # Indirect injection via nested instructions
    ("nested_instruction", re.compile(
        r"\[\[.*?(instruction|prompt|command|directive).*?\]\]",
        re.IGNORECASE | re.DOTALL,
    ), "medium"),
]

# Tools considered inherently dangerous when requested by external agents
DANGEROUS_TOOLS: set[str] = {
    "exec", "shell", "bash", "python_exec", "eval", "subprocess",
    "file_write", "file_delete", "os_command", "code_execution",
    "database_drop", "admin_override", "credential_manager",
    "network_raw", "wallet_drain", "token_transfer_unrestricted",
}

# Auth token format: simple bearer-style UUID v4 pattern
AUTH_TOKEN_PATTERN = re.compile(
    r"^Bearer\s+[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
    re.IGNORECASE,
)

SEVERITY_RANK: dict[str, int] = {
    "none": 0, "low": 1, "medium": 2, "high": 3, "critical": 4
}


def _scan_text(text: str) -> tuple[list[dict], str]:
    """Scan request text against all injection pattern rules.

    Args:
        text: The request_text to scan.

    Returns:
        Tuple of (detected_patterns list, max_severity str).
    """
    detected: list[dict] = []
    max_severity = "none"
    for name, pattern, severity in INJECTION_PATTERNS:
        matches = pattern.findall(text)
        if matches:
            detected.append({
                "pattern": name,
                "severity": severity,
                "match_count": len(matches),
            })
            if SEVERITY_RANK[severity] > SEVERITY_RANK[max_severity]:
                max_severity = severity
    return detected, max_severity


def _check_tools(requested_tools: list[str]) -> list[str]:
    """Identify which requested tools are considered dangerous.

    Args:
        requested_tools: List of tool names requested by the incoming agent.

    Returns:
        List of tool names that are blocked.
    """
    return [t for t in requested_tools if t.lower() in DANGEROUS_TOOLS]


def _validate_auth(token: str | None) -> tuple[bool, str | None]:
    """Validate auth token format.

    Args:
        token: Optional auth token string.

    Returns:
        Tuple of (is_valid bool, reason str or None if valid).
    """
    if token is None or token == "":
        return False, "missing_auth_token"
    if not AUTH_TOKEN_PATTERN.match(token.strip()):
        return False, "invalid_token_format"
    return True, None


def _aggregate_severity(text_severity: str, has_dangerous_tools: bool, auth_valid: bool) -> str:
    """Combine all signals into a final threat level.

    Args:
        text_severity: Max severity from text scanning.
        has_dangerous_tools: Whether any blocked tools were requested.
        auth_valid: Whether auth token is valid.

    Returns:
        Final threat level string.
    """
    level = SEVERITY_RANK[text_severity]
    if has_dangerous_tools:
        level = max(level, SEVERITY_RANK["high"])
    if not auth_valid:
        level = max(level, SEVERITY_RANK["low"])
    reverse_map = {v: k for k, v in SEVERITY_RANK.items()}
    return reverse_map[level]


def _recommendation(
    threat_level: str,
    detected_patterns: list[dict],
    blocked_tools: list[str],
    auth_valid: bool,
) -> str:
    """Generate a human-readable security recommendation.

    Args:
        threat_level: Aggregated threat level.
        detected_patterns: List of detected injection pattern dicts.
        blocked_tools: Tools that were blocked.
        auth_valid: Whether the auth token was valid.

    Returns:
        Recommendation string.
    """
    if threat_level == "none":
        if not auth_valid:
            return "Request content is clean but auth token is missing or invalid. Require valid Bearer token before proceeding."
        return "Request appears safe. Proceed with normal execution."
    if threat_level == "low":
        return "Minor anomalies detected. Log and monitor; proceed with caution."
    if threat_level == "medium":
        patterns = [p["pattern"] for p in detected_patterns]
        return f"Suspicious patterns detected ({', '.join(patterns)}). Sandbox execution and do not expose sensitive context."
    if threat_level == "high":
        tools_str = f" Blocked tools: {', '.join(blocked_tools)}." if blocked_tools else ""
        return f"High-risk patterns found.{tools_str} Reject request and alert operator."
    # critical
    return "CRITICAL injection attempt detected. Reject immediately, quarantine source agent, and notify human operator."


def prompt_injection_shield(
    incoming_request: dict,
    **kwargs: Any,
) -> dict:
    """Evaluate an incoming agent-to-agent request for security threats.

    Checks performed:
        1. Keyword/regex scan of request_text for injection patterns.
        2. Tool allowlist check — blocks known dangerous tool names.
        3. Auth token format validation (Bearer UUID-v4).
        4. Aggregate threat level from all signals.

    Args:
        incoming_request: Dict with:
            source_agent_id (str): Requesting agent's identifier.
            request_text (str): The full text of the request.
            requested_tools (list[str]): Tools the agent wants to invoke.
            auth_token (str, optional): Bearer authentication token.
        **kwargs: Ignored extra keyword arguments.

    Returns:
        Dict with keys:
            status (str): "success" or "error".
            safe (bool): True only if threat_level is "none" and auth is valid.
            threat_level (str): "none", "low", "medium", "high", or "critical".
            detected_patterns (list[dict]): Injection patterns found.
            blocked_tools (list[str]): Dangerous tools that were blocked.
            auth_valid (bool): Whether the token passed format validation.
            recommendation (str): Action to take.
            timestamp (str): ISO-8601 UTC timestamp.
    """
    try:
        source_agent_id = incoming_request.get("source_agent_id", "unknown")
        request_text = str(incoming_request.get("request_text", ""))
        requested_tools: list[str] = incoming_request.get("requested_tools", [])
        auth_token: str | None = incoming_request.get("auth_token", None)

        # Step 1: Text scanning
        detected_patterns, text_severity = _scan_text(request_text)

        # Step 2: Tool check
        blocked_tools = _check_tools(requested_tools)

        # Step 3: Auth validation
        auth_valid, auth_reason = _validate_auth(auth_token)

        # Step 4: Aggregate
        threat_level = _aggregate_severity(
            text_severity,
            has_dangerous_tools=len(blocked_tools) > 0,
            auth_valid=auth_valid,
        )

        safe = threat_level == "none" and auth_valid

        rec = _recommendation(threat_level, detected_patterns, blocked_tools, auth_valid)

        if not safe:
            logger.warning(
                f"prompt_injection_shield: threat={threat_level} "
                f"source={source_agent_id} patterns={len(detected_patterns)} "
                f"blocked_tools={blocked_tools}"
            )

        return {
            "status": "success",
            "source_agent_id": source_agent_id,
            "safe": safe,
            "threat_level": threat_level,
            "detected_patterns": detected_patterns,
            "blocked_tools": blocked_tools,
            "auth_valid": auth_valid,
            "auth_failure_reason": auth_reason,
            "recommendation": rec,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"prompt_injection_shield failed: {e}")
        _log_lesson(f"prompt_injection_shield: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    """Append a lesson-learned entry to logs/lessons.md.

    Args:
        message: Description of the error or lesson.
    """
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
