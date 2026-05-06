---
skill: cron_scheduler
category: integrations
description: Checks which scheduled tasks are due and when the next run occurs.
tier: free
inputs: current_time, schedule
---

# Cron Scheduler

## Description
Checks which scheduled tasks are due and when the next run occurs.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `current_time` | `string` | Yes |  |
| `schedule` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cron_scheduler",
  "arguments": {
    "current_time": "<current_time>",
    "schedule": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cron_scheduler"`.
