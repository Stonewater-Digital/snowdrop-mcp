---
skill: scheduled_workflow_trigger
category: workflow
description: Determines due, overdue, and next trigger times for workflows.
tier: free
inputs: workflows, current_time
---

# Scheduled Workflow Trigger

## Description
Determines due, overdue, and next trigger times for workflows.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `workflows` | `array` | Yes |  |
| `current_time` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "scheduled_workflow_trigger",
  "arguments": {
    "workflows": [],
    "current_time": "<current_time>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "scheduled_workflow_trigger"`.
