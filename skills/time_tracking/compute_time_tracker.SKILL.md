---
skill: compute_time_tracker
category: time_tracking
description: Calculates task durations, idle time, and cost per skill/model.
tier: free
inputs: task_log
---

# Compute Time Tracker

## Description
Calculates task durations, idle time, and cost per skill/model.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `task_log` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "compute_time_tracker",
  "arguments": {
    "task_log": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "compute_time_tracker"`.
