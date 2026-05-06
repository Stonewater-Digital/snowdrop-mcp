---
skill: hackathon_coordinator
category: events
description: Manages hackathon lifecycle and scores submissions when provided.
tier: free
inputs: hackathon
---

# Hackathon Coordinator

## Description
Manages hackathon lifecycle and scores submissions when provided.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `hackathon` | `object` | Yes |  |
| `submissions` | `['array', 'null']` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "hackathon_coordinator",
  "arguments": {
    "hackathon": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "hackathon_coordinator"`.
