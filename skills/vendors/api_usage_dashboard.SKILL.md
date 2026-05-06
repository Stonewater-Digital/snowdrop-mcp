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
| `usage_logs` | `array` | Yes | List of usage log objects, each with `provider` (string), `model` (string), `tokens` (int), `cost_usd` (float), `purpose` (string), and `timestamp` (ISO8601 string). |
| `budget_limit` | `number` | No | Optional monthly budget cap in USD. If provided, the dashboard flags providers exceeding their share of the limit. |

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
    "usage_logs": [
      {
        "provider": "OpenRouter",
        "model": "claude-3-haiku",
        "tokens": 15000,
        "cost_usd": 0.075,
        "purpose": "reconciliation",
        "timestamp": "2026-05-06T00:00:00Z"
      }
    ],
    "budget_limit": 20.0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "api_usage_dashboard"`.
