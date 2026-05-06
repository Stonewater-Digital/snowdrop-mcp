---
skill: failure_diagnostic_generator
category: ralph_wiggum
description: Summarizes attempts, hypothesizes root causes, and prescribes human actions.
tier: free
inputs: task_name, attempts, system_state
---

# Failure Diagnostic Generator

## Description
Summarizes attempts, hypothesizes root causes, and prescribes human actions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `task_name` | `string` | Yes |  |
| `attempts` | `array` | Yes |  |
| `system_state` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "failure_diagnostic_generator",
  "arguments": {
    "task_name": "<task_name>",
    "attempts": [],
    "system_state": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "failure_diagnostic_generator"`.
