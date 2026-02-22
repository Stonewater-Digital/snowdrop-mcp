"""Pre-flight deployment readiness check."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "deployment_readiness_checker",
    "description": "Aggregates deployment checklist results and surfaces blockers/warnings.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "checks": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["checks"],
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


def deployment_readiness_checker(checks: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Summarize readiness across deployment categories."""
    try:
        passed = failed = skipped = 0
        blockers: list[str] = []
        warnings: list[str] = []
        for check in checks:
            status = (check.get("status") or "").lower()
            name = check.get("name", "unknown")
            if status == "pass":
                passed += 1
            elif status == "fail":
                failed += 1
                blockers.append(f"{name} ({check.get('category')})")
            else:
                skipped += 1
                warnings.append(f"Skipped: {name}")
        ready = failed == 0
        data = {
            "ready": ready,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "blockers": blockers,
            "warnings": warnings,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("deployment_readiness_checker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
