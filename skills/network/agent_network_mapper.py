"""Map interactions between Snowdrop agents."""
from __future__ import annotations

from collections import deque
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "agent_network_mapper",
    "description": "Builds adjacency insights, clusters, and bridge agents from interactions.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "interactions": {
                "type": "array",
                "items": {"type": "object"},
            }
        },
        "required": ["interactions"],
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


def agent_network_mapper(interactions: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Build adjacency, clusters, and key agent roles."""
    try:
        adjacency: dict[str, set[str]] = {}
        edge_set: set[tuple[str, str]] = set()
        for interaction in interactions:
            if not isinstance(interaction, dict):
                raise ValueError("each interaction must be a dict")
            source = str(interaction.get("from_agent"))
            target = str(interaction.get("to_agent"))
            if not source or not target:
                continue
            adjacency.setdefault(source, set()).add(target)
            adjacency.setdefault(target, set()).add(source)
            edge = tuple(sorted((source, target)))
            edge_set.add(edge)

        nodes = list(adjacency.keys())
        clusters = _connected_components(adjacency)
        isolated = [node for node in nodes if not adjacency[node]]
        hub_agents = sorted(nodes, key=lambda node: len(adjacency[node]), reverse=True)[:5]
        bridge_agents = _bridge_agents(adjacency)

        data = {
            "nodes": len(nodes),
            "edges": len(edge_set),
            "clusters": clusters,
            "hub_agents": hub_agents,
            "bridge_agents": bridge_agents,
            "isolated_agents": isolated,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("agent_network_mapper", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _connected_components(graph: dict[str, set[str]]) -> list[dict[str, Any]]:
    visited: set[str] = set()
    components: list[dict[str, Any]] = []
    for node in graph:
        if node in visited:
            continue
        queue: deque[str] = deque([node])
        component = []
        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            component.append(current)
            for neighbor in graph.get(current, set()):
                if neighbor not in visited:
                    queue.append(neighbor)
        components.append({"members": component, "size": len(component)})
    return components


def _bridge_agents(graph: dict[str, set[str]]) -> list[str]:
    bridges = []
    for node, neighbors in graph.items():
        if len(neighbors) < 2:
            continue
        components = 0
        visited: set[str] = set()
        for neighbor in neighbors:
            if neighbor in visited:
                continue
            components += 1
            visited.update(_dfs_without(graph, neighbor, node))
        if components > 1:
            bridges.append(node)
    return bridges


def _dfs_without(graph: dict[str, set[str]], start: str, excluded: str) -> set[str]:
    stack = [start]
    visited: set[str] = set()
    while stack:
        node = stack.pop()
        if node in visited or node == excluded:
            continue
        visited.add(node)
        for neighbor in graph.get(node, set()):
            if neighbor not in visited and neighbor != excluded:
                stack.append(neighbor)
    return visited


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
