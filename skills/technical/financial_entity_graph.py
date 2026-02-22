"""
Executive Summary: PE/VC/RE asset link visualization — builds an adjacency graph, scores centrality, and surfaces hub entities.
Inputs: entities (list of dicts: name str, type str, id str),
        relationships (list of dicts: source_id str, target_id str, relationship_type str)
Outputs: graph_summary (dict), hub_entities (list), connected_components (int), entity_centrality (list of dicts)
MCP Tool Name: financial_entity_graph
"""
import os
import logging
import math
from typing import Any
from datetime import datetime, timezone
from collections import defaultdict, deque

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "financial_entity_graph",
    "description": (
        "Constructs an in-memory adjacency graph of financial entities "
        "(funds, companies, LPs, GPs, properties) and their ownership / investment "
        "relationships. Computes degree centrality for each node, finds connected "
        "components via BFS, and identifies hub entities whose centrality exceeds "
        "median + 1 standard deviation."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "entities": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "type": {"type": "string", "enum": ["fund", "company", "lp", "gp", "property"]},
                        "id":   {"type": "string"},
                    },
                    "required": ["name", "type", "id"],
                },
            },
            "relationships": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "source_id":         {"type": "string"},
                        "target_id":         {"type": "string"},
                        "relationship_type": {
                            "type": "string",
                            "enum": ["invested_in", "manages", "owns", "lp_of"],
                        },
                    },
                    "required": ["source_id", "target_id", "relationship_type"],
                },
            },
        },
        "required": ["entities", "relationships"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "graph_summary":        {"type": "object"},
            "hub_entities":         {"type": "array"},
            "connected_components": {"type": "integer"},
            "entity_centrality":    {"type": "array"},
            "status":               {"type": "string"},
            "timestamp":            {"type": "string"},
        },
        "required": ["graph_summary", "hub_entities", "connected_components", "entity_centrality", "status", "timestamp"],
    },
}


def financial_entity_graph(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build and analyse a directed graph of financial entities and relationships.

    Args:
        entities: List of node descriptors. Each dict must contain:
            - id (str): Unique node identifier.
            - name (str): Human-readable entity name.
            - type (str): One of "fund", "company", "lp", "gp", "property".
        relationships: List of directed edge descriptors. Each dict must contain:
            - source_id (str): ID of the originating entity.
            - target_id (str): ID of the receiving entity.
            - relationship_type (str): One of "invested_in", "manages", "owns", "lp_of".

    Returns:
        dict with keys:
            - status (str): "success" or "error".
            - graph_summary (dict): Node count, edge count, entity type distribution.
            - hub_entities (list[dict]): Entities with centrality > median + 1 stddev.
            - connected_components (int): Number of weakly-connected subgraphs.
            - entity_centrality (list[dict]): All entities with their centrality score,
              sorted descending.
            - timestamp (str): ISO 8601 UTC execution timestamp.
    """
    try:
        now_utc: datetime = datetime.now(timezone.utc)

        # Build entity lookup
        entity_map: dict[str, dict[str, Any]] = {e["id"]: e for e in entities}
        all_ids: set[str] = set(entity_map.keys())

        # Directed adjacency list (source → list of targets)
        adj_out: dict[str, list[str]] = defaultdict(list)
        # Undirected adjacency for component detection
        adj_undirected: dict[str, set[str]] = defaultdict(set)

        for rel in relationships:
            src: str = rel.get("source_id", "")
            tgt: str = rel.get("target_id", "")
            rel_type: str = rel.get("relationship_type", "")
            adj_out[src].append(tgt)
            adj_undirected[src].add(tgt)
            adj_undirected[tgt].add(src)
            # Track unknown IDs referenced in relationships
            all_ids.update([src, tgt])

        # Degree centrality: (in-degree + out-degree) / (N - 1), or raw count if N <= 1
        n: int = len(all_ids)
        degree: dict[str, int] = defaultdict(int)
        for src, targets in adj_out.items():
            degree[src] += len(targets)
            for tgt in targets:
                degree[tgt] += 1

        normaliser: float = max(n - 1, 1)
        centrality_scores: dict[str, float] = {
            node_id: round(degree[node_id] / normaliser, 6)
            for node_id in all_ids
        }

        # Statistics for hub detection
        scores: list[float] = list(centrality_scores.values())
        mean_score: float = sum(scores) / len(scores) if scores else 0.0
        variance: float = (
            sum((s - mean_score) ** 2 for s in scores) / len(scores) if scores else 0.0
        )
        stddev: float = math.sqrt(variance)
        sorted_scores: list[float] = sorted(scores)
        mid: int = len(sorted_scores) // 2
        median_score: float = (
            sorted_scores[mid]
            if len(sorted_scores) % 2 == 1
            else (sorted_scores[mid - 1] + sorted_scores[mid]) / 2.0
        )
        hub_threshold: float = median_score + stddev

        # Build entity_centrality output list
        entity_centrality: list[dict[str, Any]] = []
        hub_entities: list[dict[str, Any]] = []
        for node_id in all_ids:
            info: dict[str, Any] = entity_map.get(node_id, {"id": node_id, "name": node_id, "type": "unknown"})
            score: float = centrality_scores[node_id]
            entry: dict[str, Any] = {
                "entity":           info.get("name", node_id),
                "id":               node_id,
                "type":             info.get("type", "unknown"),
                "centrality_score": score,
                "degree":           degree[node_id],
                "is_hub":           score > hub_threshold,
            }
            entity_centrality.append(entry)
            if score > hub_threshold:
                hub_entities.append(entry)

        entity_centrality.sort(key=lambda x: x["centrality_score"], reverse=True)
        hub_entities.sort(key=lambda x: x["centrality_score"], reverse=True)

        # Connected components via BFS on undirected adjacency
        visited: set[str] = set()
        connected_components: int = 0
        for start_id in all_ids:
            if start_id not in visited:
                connected_components += 1
                queue: deque[str] = deque([start_id])
                while queue:
                    node: str = queue.popleft()
                    if node in visited:
                        continue
                    visited.add(node)
                    for neighbour in adj_undirected.get(node, set()):
                        if neighbour not in visited:
                            queue.append(neighbour)

        # Entity type distribution
        type_distribution: dict[str, int] = defaultdict(int)
        for e in entities:
            type_distribution[e.get("type", "unknown")] += 1

        graph_summary: dict[str, Any] = {
            "node_count":          len(all_ids),
            "edge_count":          len(relationships),
            "entity_type_dist":    dict(type_distribution),
            "hub_threshold":       round(hub_threshold, 6),
            "median_centrality":   round(median_score, 6),
            "stddev_centrality":   round(stddev, 6),
        }

        return {
            "status":               "success",
            "graph_summary":        graph_summary,
            "hub_entities":         hub_entities,
            "connected_components": connected_components,
            "entity_centrality":    entity_centrality,
            "timestamp":            now_utc.isoformat(),
        }

    except Exception as e:
        logger.error(f"financial_entity_graph failed: {e}")
        _log_lesson(f"financial_entity_graph: {e}")
        return {"status": "error", "error": str(e), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    """Append a failure lesson to the shared lessons log.

    Args:
        message: Human-readable description of the failure.
    """
    with open("logs/lessons.md", "a") as f:
        f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
