"""Score community contributions for quality and security."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "contribution_quality_scorer",
    "description": "Calculates quality grades based on Snowdrop coding standards and security checks.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "submission": {"type": "object"},
        },
        "required": ["submission"],
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

PATTERN_WEIGHT = 0.4
SECURITY_WEIGHT = 0.3
COMPLETENESS_WEIGHT = 0.2
STYLE_WEIGHT = 0.1


def contribution_quality_scorer(submission: dict[str, Any], **_: Any) -> dict[str, Any]:
    """Return quality score, grade, and auto-approval recommendation."""
    try:
        pattern_score = sum(
            int(submission.get(flag, False))
            for flag in [
                "has_tool_meta",
                "has_input_schema",
                "has_output_schema",
                "has_error_handling",
                "has_log_lesson",
                "has_docstring",
            ]
        ) / 6
        security_flags = submission.get("dangerous_patterns_found", [])
        security_score = 1 - min(len(security_flags) / 3, 1)
        completeness_score = min(submission.get("lines", 0) / 50, 1)
        style_score = 1 if submission.get("passes_import_check", False) else 0.5
        quality_score = (
            pattern_score * PATTERN_WEIGHT
            + security_score * SECURITY_WEIGHT
            + completeness_score * COMPLETENESS_WEIGHT
            + style_score * STYLE_WEIGHT
        ) * 100
        grade = _grade(quality_score)
        issues = security_flags + (["Missing pattern"] if pattern_score < 1 else [])
        suggestions = []
        if pattern_score < 1:
            suggestions.append("Ensure TOOL_META, schemas, and log helper are present")
        if security_flags:
            suggestions.append("Remove dangerous patterns: " + ", ".join(security_flags))
        if completeness_score < 1:
            suggestions.append("Add more substance or tests to reach 50+ lines")
        auto_approve = quality_score >= 85 and not security_flags
        data = {
            "quality_score": round(quality_score, 2),
            "grade": grade,
            "breakdown": {
                "pattern": round(pattern_score * 100, 1),
                "security": round(security_score * 100, 1),
                "completeness": round(completeness_score * 100, 1),
                "style": round(style_score * 100, 1),
            },
            "auto_approve": auto_approve,
            "issues": issues,
            "suggestions": suggestions,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("contribution_quality_scorer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _grade(score: float) -> str:
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
