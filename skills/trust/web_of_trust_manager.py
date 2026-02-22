"""Manage the community web-of-trust graph."""
from __future__ import annotations

import json
import os
import json
from collections import deque
from datetime import datetime, timezone
from typing import Any

LOG_PATH = "logs/trust_graph.jsonl"
ROOT_AGENT = "snowdrop-core"

TOOL_META: dict[str, Any] = {
    "name": "web_of_trust_manager",
    "description": "Records vouches between agents and exposes trust graph stats.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["vouch", "revoke", "get_vouchers", "get_vouched_for"],
            },
            "from_agent": {"type": "string"},
            "to_agent": {"type": ["string", "null"], "default": None},
            "vouch_context": {"type": ["string", "null"], "default": None},
        },
        "required": ["operation", "from_agent"],
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


MAX_VOUCHES = 10
VALID_CONTEXT = {"reliable_payer", "quality_work", "good_actor", "technical_skill"}


def web_of_trust_manager(
    operation: str,
    from_agent: str,
    to_agent: str | None = None,
    vouch_context: str | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Run the requested trust-graph mutation or query."""
    try:
        graph = _hydrate_graph()
        data: dict[str, Any]
        if operation == "vouch":
            if not to_agent:
                raise ValueError("to_agent required for vouch")
            if vouch_context and vouch_context not in VALID_CONTEXT:
                raise ValueError("Invalid vouch_context")
            if len(graph.get(from_agent, [])) >= MAX_VOUCHES:
                raise ValueError("Vouch quota exceeded")
            graph.setdefault(from_agent, set()).add(to_agent)
            _append_log({
                "action": "vouch",
                "from": from_agent,
                "to": to_agent,
                "context": vouch_context,
            })
            data = _graph_response(graph, from_agent, to_agent)
        elif operation == "revoke":
            if not to_agent:
                raise ValueError("to_agent required for revoke")
            graph.setdefault(from_agent, set()).discard(to_agent)
            _append_log({"action": "revoke", "from": from_agent, "to": to_agent})
            data = _graph_response(graph, from_agent, to_agent)
        elif operation == "get_vouchers":
            if not to_agent:
                raise ValueError("to_agent required for get_vouchers")
            vouchers = [agent for agent, targets in graph.items() if to_agent in targets]
            data = {
                "vouches_given": len(graph.get(from_agent, [])),
                "vouches_received": len(vouchers),
                "vouchers": vouchers,
                "trust_depth": _trust_depth(graph, to_agent),
            }
        elif operation == "get_vouched_for":
            targets = list(graph.get(from_agent, []))
            data = {
                "vouches_given": len(targets),
                "vouches_received": len(
                    [agent for agent, recipients in graph.items() if from_agent in recipients]
                ),
                "vouchers": targets,
                "trust_depth": _trust_depth(graph, from_agent),
            }
        else:
            raise ValueError("Unsupported operation")

        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("web_of_trust_manager", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _graph_response(graph: dict[str, set[str]], from_agent: str, to_agent: str | None) -> dict[str, Any]:
    vouchers = [agent for agent, targets in graph.items() if agent != from_agent and from_agent in targets]
    return {
        "vouches_given": len(graph.get(from_agent, [])),
        "vouches_received": len(vouchers),
        "vouchers": vouchers,
        "trust_depth": _trust_depth(graph, to_agent or from_agent),
    }


def _trust_depth(graph: dict[str, set[str]], target: str) -> int:
    if target == ROOT_AGENT:
        return 0
    visited = {ROOT_AGENT}
    queue: deque[tuple[str, int]] = deque([(ROOT_AGENT, 0)])
    while queue:
        current, depth = queue.popleft()
        for neighbor in graph.get(current, []):
            if neighbor == target:
                return depth + 1
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, depth + 1))
    return -1


def _hydrate_graph() -> dict[str, set[str]]:
    graph: dict[str, set[str]] = {}
    if not os.path.exists(LOG_PATH):
        return graph
    with open(LOG_PATH, "r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            payload = json.loads(line)
            action = payload.get("action")
            source = payload.get("from")
            target = payload.get("to")
            if not source or not target:
                continue
            graph.setdefault(source, set())
            if action == "vouch":
                graph[source].add(target)
            elif action == "revoke":
                graph[source].discard(target)
    return graph


def _append_log(entry: dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    entry["logged_at"] = datetime.now(timezone.utc).isoformat()
    with open(LOG_PATH, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry) + "\n")


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
