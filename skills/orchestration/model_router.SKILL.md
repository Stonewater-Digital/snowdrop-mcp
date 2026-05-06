---
skill: model_router
category: orchestration
description: Reads config/config.yaml and maps a task category to the correct model entry.
tier: free
inputs: task_category
---

# Model Router

## Description
Reads config/config.yaml and maps a task category to the correct model entry.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `task_category` | `string` | Yes |  |
| `urgency` | `string` | No |  |
| `fallback_allowed` | `boolean` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "model_router",
  "arguments": {
    "task_category": "<task_category>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "model_router"`.
