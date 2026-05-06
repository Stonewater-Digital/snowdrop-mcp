---
skill: community_leverage_dashboard
category: crowd_economics
description: Summarizes how community contributions amplify internal capacity.
tier: free
inputs: period, internal_stats, community_stats
---

# Community Leverage Dashboard

## Description
Summarizes how community contributions amplify internal capacity.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `period` | `string` | Yes |  |
| `internal_stats` | `object` | Yes |  |
| `community_stats` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "community_leverage_dashboard",
  "arguments": {
    "period": "<period>",
    "internal_stats": {},
    "community_stats": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "community_leverage_dashboard"`.
