---
skill: agent_session_tracker
category: agent_crm
description: Aggregates per-agent usage, spend, and churn risk from session logs.
tier: free
inputs: sessions
---

# Agent Session Tracker

## Description
Aggregates per-agent usage, spend, and churn risk from session logs.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `sessions` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "agent_session_tracker",
  "arguments": {
    "sessions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "agent_session_tracker"`.
