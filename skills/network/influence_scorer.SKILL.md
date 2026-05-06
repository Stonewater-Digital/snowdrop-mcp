---
skill: influence_scorer
category: network
description: Scores agent influence using a simplified PageRank iteration.
tier: free
inputs: interactions
---

# Influence Scorer

## Description
Scores agent influence using a simplified PageRank iteration.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `interactions` | `array` | Yes |  |
| `damping` | `number` | No |  |
| `iterations` | `integer` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "influence_scorer",
  "arguments": {
    "interactions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "influence_scorer"`.
