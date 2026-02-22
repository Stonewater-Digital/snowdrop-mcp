"""Test agent compatibility with Snowdrop APIs."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "agent_compatibility_tester",
    "description": "Runs handshake, discovery, and error-handling tests for third-party agents.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "agent_id": {"type": "string"},
            "test_suite": {
                "type": "string",
                "enum": ["basic", "standard", "full"],
            },
            "agent_capabilities": {"type": "object"},
        },
        "required": ["agent_id", "test_suite", "agent_capabilities"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
    },
}


TESTS = [
    ("auth_handshake", lambda caps: caps.get("auth_method") in {"oauth", "token"}),
    ("skill_discovery", lambda caps: caps.get("supports_mcp")),
    ("sample_call", lambda caps: caps.get("supports_a2a")),
    ("error_handling", lambda caps: caps.get("error_handling", True)),
    ("rate_limit", lambda caps: caps.get("respects_rate_limits", True)),
]


def agent_compatibility_tester(
    agent_id: str,
    test_suite: str,
    agent_capabilities: dict[str, Any],
    **_: Any,
) -> dict[str, Any]:
    """Return compatibility score and level."""
    try:
        results = []
        passed = 0
        for name, predicate in TESTS:
            outcome = bool(predicate(agent_capabilities))
            results.append({"test": name, "passed": outcome})
            passed += int(outcome)
        suite_multiplier = {"basic": 0.8, "standard": 1.0, "full": 1.1}[test_suite]
        score = min(100.0, passed / len(TESTS) * 100 * suite_multiplier)
        level = "basic"
        if score >= 90:
            level = "premium"
        elif score >= 75:
            level = "standard"
        certification_eligible = score >= 60
        data = {
            "passed": score >= 80,
            "score": round(score, 2),
            "test_results": results,
            "compatibility_level": level,
            "issues": [r["test"] for r in results if not r["passed"]],
            "certification_eligible": certification_eligible,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("agent_compatibility_tester", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
