---
skill: workflow_engine
category: workflow
description: Evaluates workflow dependencies and surfaces next executable steps.
tier: free
inputs: workflow
---

# Workflow Engine

## Description
Evaluates workflow dependencies and surfaces next executable steps.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `workflow` | `object` | Yes |  |
| `completed_steps` | `array` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "workflow_engine",
  "arguments": {
    "workflow": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "workflow_engine"`.
