---
skill: franchise_analytics_reporter
category: franchise
description: Summarizes revenue, royalties, and operational health per franchise operator.
tier: free
inputs: operator_id, period, requests, agent_count
---

# Franchise Analytics Reporter

## Description
Summarizes revenue, royalties, and operational health per franchise operator.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operator_id` | `string` | Yes |  |
| `period` | `string` | Yes |  |
| `requests` | `array` | Yes |  |
| `agent_count` | `integer` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "franchise_analytics_reporter",
  "arguments": {
    "operator_id": "<operator_id>",
    "period": "<period>",
    "requests": [],
    "agent_count": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "franchise_analytics_reporter"`.
