"""Resolve execution order and parallel task groups."""
from __future__ import annotations

from collections import defaultdict, deque
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "task_dependency_resolver",
    "description": "Performs topological sorting and surfaces parallelizable groups.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "tasks": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["tasks"],
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


def task_dependency_resolver(tasks: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return a dependency-aware plan or error on cycle detection."""
    try:
        if not tasks:
            raise ValueError("tasks cannot be empty")
        graph: dict[str, list[str]] = defaultdict(list)
        indegree: dict[str, int] = {}
        nodes = set()
        for task in tasks:
            task_id = task.get("task_id")
            if not task_id:
                raise ValueError("task_id is required for every task")
            nodes.add(task_id)
            depends = task.get("depends_on", []) or []
            indegree.setdefault(task_id, 0)
            for dep in depends:
                graph[dep].append(task_id)
                indegree[task_id] = indegree.get(task_id, 0) + 1
                nodes.add(dep)
                indegree.setdefault(dep, 0)

        zero_indegree = deque(sorted(node for node in nodes if indegree.get(node, 0) == 0))
        order: list[str] = []
        parallel_groups: list[list[str]] = []
        while zero_indegree:
            current_layer = sorted(set(zero_indegree))
            zero_indegree.clear()
            parallel_groups.append(current_layer)
            for node in current_layer:
                order.append(node)
                for neighbor in graph.get(node, []):
                    indegree[neighbor] -= 1
                    if indegree[neighbor] == 0:
                        zero_indegree.append(neighbor)

        if len(order) != len(nodes):
            message = "Circular dependency detected"
            _log_lesson("task_dependency_resolver", message)
            return {
                "status": "error",
                "data": {"error": message, "has_cycles": True},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        data = {
            "execution_order": order,
            "parallel_groups": parallel_groups,
            "has_cycles": False,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("task_dependency_resolver", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
