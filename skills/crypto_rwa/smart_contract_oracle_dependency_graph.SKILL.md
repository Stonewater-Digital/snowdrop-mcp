---
skill: smart_contract_oracle_dependency_graph
category: crypto_rwa
description: Constructs dependency graphs of oracle feeds to find single points of failure.
tier: free
inputs: payload
---

# Smart Contract Oracle Dependency Graph

## Description
Constructs dependency graphs of oracle feeds to find single points of failure.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `payload` | `any` | Yes |  |
| `context` | `any` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "smart_contract_oracle_dependency_graph",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_oracle_dependency_graph"`.
