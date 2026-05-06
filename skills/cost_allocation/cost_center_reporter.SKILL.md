---
skill: cost_center_reporter
category: cost_allocation
description: Aggregates expenses by center with mix and budget deltas.
tier: free
inputs: expenses, period
---

# Cost Center Reporter

## Description
Aggregates expenses by center with mix and budget deltas.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `expenses` | `array` | Yes |  |
| `period` | `string` | Yes |  |
| `budget` | `['object', 'null']` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cost_center_reporter",
  "arguments": {
    "expenses": [],
    "period": "<period>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cost_center_reporter"`.
