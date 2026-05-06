---
skill: financial_entity_graph
category: technical
description: Constructs an in-memory adjacency graph of financial entities (funds, companies, LPs, GPs, properties) and their ownership / investment relationships. Computes degree centrality for each node, finds connected components via BFS, and identifies hub entities whose centrality exceeds median + 1 standard deviation.
tier: free
inputs: entities, relationships
---

# Financial Entity Graph

## Description
Constructs an in-memory adjacency graph of financial entities (funds, companies, LPs, GPs, properties) and their ownership / investment relationships. Computes degree centrality for each node, finds connected components via BFS, and identifies hub entities whose centrality exceeds median + 1 standard deviation.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `entities` | `array` | Yes |  |
| `relationships` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "financial_entity_graph",
  "arguments": {
    "entities": [],
    "relationships": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "financial_entity_graph"`.
