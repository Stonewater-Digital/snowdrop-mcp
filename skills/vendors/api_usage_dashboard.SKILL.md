---
skill: api_usage_dashboard
category: vendors
description: Summarizes token usage, costs, and trends across providers/models/purposes.
tier: free
inputs: usage_logs
---

# Api Usage Dashboard

## Description
Summarizes token usage, costs, and trends across providers/models/purposes.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `usage_logs` | `array` | Yes |  |
| `budget_limit` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "api_usage_dashboard",
  "arguments": {
    "usage_logs": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "api_usage_dashboard"`.
