---
skill: agent_network_mapper
category: network
description: Builds adjacency insights, clusters, and bridge agents from interactions.
tier: free
inputs: interactions
---

# Agent Network Mapper

## Description
Builds adjacency insights, clusters, and bridge agents from interactions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `interactions` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "agent_network_mapper",
  "arguments": {
    "interactions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "agent_network_mapper"`.
