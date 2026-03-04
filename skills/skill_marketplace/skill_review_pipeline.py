"""Evaluate community skill submissions for quality and security."""
from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "skill_review_pipeline",
    "description": "Runs static review checks on submitted community skill code.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "submission_id": {"type": "string"},
            "skill_code": {"type": "string"},
            "checklist": {"type": ["object", "null"], "default": None},
        },
        "required": ["submission_id", "skill_code"],
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

DEFAULT_CHECKS = {
    "has_tool_meta": lambda code: "TOOL_META" in code,
    "has_main_function": lambda code: bool(re.search(r"def\s+\w+\(", code)),
    "has_error_handling": lambda code: "except" in code,
    "dangerous_imports": lambda code: not re.search(r"(os\.system|subprocess|eval\(|exec\()", code),
    "return_envelope": lambda code: '"status"' in code or "'status'" in code,
}


def skill_review_pipeline(
    submission_id: str,
    skill_code: str,
    checklist: dict[str, Any] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Run automated review checks."""
    try:
        checks_to_run = checklist or {key: True for key in DEFAULT_CHECKS}
        results = []
        passed_total = 0
        for check, enabled in checks_to_run.items():
            if not enabled:
                continue
            rule = DEFAULT_CHECKS.get(check)
            outcome = bool(rule(skill_code)) if rule else False
            passed_total += int(outcome)
            results.append({"check": check, "passed": outcome})
        score = passed_total / max(len(results), 1) * 100
        security_flags = [
            "dangerous_imports" for item in results if not item["passed"] and item["check"] == "dangerous_imports"
        ]
        recommendation = "approve" if score >= 80 else "revise" if score >= 50 else "reject"
        data = {
            "passed": score == 100,
            "score": round(score, 2),
            "checks": results,
            "security_flags": security_flags,
            "recommendation": recommendation,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("skill_review_pipeline", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
