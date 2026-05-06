---
skill: assembly_line_cost_calculator
category: orchestration
description: Compares Assembly Line run-rate against a pure-Opus baseline.
tier: free
inputs: task_count, avg_tokens_per_task
---

# Assembly Line Cost Calculator

## Description
Compares Assembly Line run-rate against a pure-Opus baseline.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `task_count` | `integer` | Yes |  |
| `avg_tokens_per_task` | `integer` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "assembly_line_cost_calculator",
  "arguments": {
    "task_count": 0,
    "avg_tokens_per_task": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "assembly_line_cost_calculator"`.
