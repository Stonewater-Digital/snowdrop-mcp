---
skill: community_growth_tracker
category: community_analytics
description: Calculates growth rates, viral coefficient, and projections from snapshots.
tier: free
inputs: snapshots
---

# Community Growth Tracker

## Description
Calculates growth rates, viral coefficient, and projections from snapshots.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `snapshots` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "community_growth_tracker",
  "arguments": {
    "snapshots": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "community_growth_tracker"`.
