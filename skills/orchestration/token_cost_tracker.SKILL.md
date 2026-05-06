---
skill: token_cost_tracker
category: orchestration
description: Logs model API usage and enforces the $50/day spend cap.
tier: free
inputs: entries
---

# Token Cost Tracker

## Description
Logs model API usage and enforces the $50/day spend cap.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `entries` | `array` | Yes | Usage entries to append and track. |
| `log_path` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "token_cost_tracker",
  "arguments": {
    "entries": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_cost_tracker"`.
