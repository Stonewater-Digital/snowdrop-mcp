"""Determine next executable steps in a workflow."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "workflow_engine",
    "description": "Evaluates workflow dependencies and surfaces next executable steps.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "workflow": {"type": "object"},
            "completed_steps": {
                "type": "array",
                "items": {"type": "string"},
                "default": [],
            },
        },
        "required": ["workflow"],
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


def workflow_engine(
    workflow: dict[str, Any],
    completed_steps: list[str] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Resolve dependency-aware execution order for a workflow."""
    try:
        steps = workflow.get("steps", [])
        if not steps:
            raise ValueError("workflow.steps cannot be empty")
        completed = set(completed_steps or [])
        step_ids = {step["step_id"] for step in steps}
        if missing := completed - step_ids:
            raise ValueError(f"completed_steps contain unknown IDs: {missing}")

        graph = {step["step_id"]: set(step.get("depends_on", [])) for step in steps}
        ready_steps = _resolve_ready_steps(steps, completed, graph)
        blocked = _resolve_blocked_steps(steps, completed, graph, ready_steps)
        completed_list = [step_id for step_id in completed if step_id in step_ids]
        progress_pct = round(len(completed_list) / len(steps) * 100, 2)
        workflow_complete = len(completed_list) == len(steps)

        data = {
            "next_steps": ready_steps,
            "blocked_steps": blocked,
            "completed": completed_list,
            "progress_pct": progress_pct,
            "workflow_complete": workflow_complete,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("workflow_engine", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _resolve_ready_steps(
    steps: list[dict[str, Any]],
    completed: set[str],
    graph: dict[str, set[str]],
) -> list[dict[str, Any]]:
    ready = []
    for step in steps:
        step_id = step["step_id"]
        if step_id in completed:
            continue
        deps = graph.get(step_id, set())
        if deps.issubset(completed):
            ready.append({
                "step_id": step_id,
                "skill_name": step.get("skill_name"),
                "params": step.get("params", {}),
            })
    return ready


def _resolve_blocked_steps(
    steps: list[dict[str, Any]],
    completed: set[str],
    graph: dict[str, set[str]],
    ready_steps: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    ready_ids = {step["step_id"] for step in ready_steps}
    blocked = []
    for step in steps:
        step_id = step["step_id"]
        if step_id in completed or step_id in ready_ids:
            continue
        deps = graph.get(step_id, set())
        unmet = [dep for dep in deps if dep not in completed]
        blocked.append({"step_id": step_id, "waiting_on": unmet})
    return blocked


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
