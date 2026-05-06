---
skill: consensus_protocol
category: swarm
description: Evaluates votes for quorum and flags potential Byzantine behavior.
tier: free
inputs: votes
---

# Consensus Protocol

## Description
Evaluates votes for quorum and flags potential Byzantine behavior.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `votes` | `array` | Yes |  |
| `quorum_threshold` | `number` | No |  |
| `min_voters` | `integer` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "consensus_protocol",
  "arguments": {
    "votes": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "consensus_protocol"`.
