"""Generate interactive demo scripts for Snowdrop skills."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "skill_demo_generator",
    "description": "Creates narrative demo content, sample IO, and use cases for any skill.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "skill_name": {"type": "string"},
            "skill_meta": {"type": "object"},
            "audience": {
                "type": "string",
                "enum": ["developer", "business", "agent"],
            },
        },
        "required": ["skill_name", "skill_meta", "audience"],
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


def skill_demo_generator(
    skill_name: str,
    skill_meta: dict[str, Any],
    audience: str,
    **_: Any,
) -> dict[str, Any]:
    """Return markdown demo assets for a skill."""
    try:
        sample_request = _build_sample(skill_meta)
        sample_response = {
            "status": "success",
            "data": {"example": "..."},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        demo_md = (
            f"# {skill_name} Demo ({audience.title()} view)\n"
            f"{skill_meta.get('description', '')}\n\n"
            "## Step 1: Understand the Skill\n"
            "Describe what the skill solves and why it matters.\n\n"
            "## Step 2: Provide Input\n"
            f"```json\n{sample_request}\n```\n"
            "## Step 3: Inspect Output\n"
            f"```json\n{sample_response}\n```\n"
            "## Step 4: Real-world Use Case\n"
            "Explain how this maps to a business outcome.\n"
        )
        use_cases = [
            f"{skill_name} accelerates onboarding for {audience} personas.",
            "Automates recurring workflows with trust guarantees.",
        ]
        data = {
            "demo_md": demo_md,
            "sample_request": sample_request,
            "sample_response": sample_response,
            "use_cases": use_cases,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("skill_demo_generator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _build_sample(meta: dict[str, Any]) -> dict[str, Any]:
    sample: dict[str, Any] = {}
    for name, prop in meta.get("inputSchema", {}).get("properties", {}).items():
        sample[name] = prop.get("default")
    return sample


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
