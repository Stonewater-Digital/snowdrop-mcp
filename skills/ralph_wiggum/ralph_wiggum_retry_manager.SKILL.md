---
skill: ralph_wiggum_retry_manager
category: ralph_wiggum
description: Determines whether to retry or escalate tasks per ethics playbook.
tier: free
inputs: task_name, attempt_number
---

# Ralph Wiggum Retry Manager

## Description
Determines whether to retry or escalate tasks per ethics playbook.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `task_name` | `string` | Yes |  |
| `attempt_number` | `integer` | Yes |  |
| `max_attempts` | `integer` | No |  |
| `previous_error` | `['string', 'null']` | No |  |
| `previous_lessons` | `array` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ralph_wiggum_retry_manager",
  "arguments": {
    "task_name": "<task_name>",
    "attempt_number": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ralph_wiggum_retry_manager"`.
