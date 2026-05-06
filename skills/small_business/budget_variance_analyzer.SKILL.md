---
skill: budget_variance_analyzer
category: small_business
description: Summarizes budgeted versus actual spend by category with variance breakdowns, flagging overruns and savings opportunities.
tier: free
inputs: budget_items
---

# Budget Variance Analyzer

## Description
Summarizes budgeted versus actual spend by category with variance breakdowns, flagging overruns and savings opportunities.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `budget_items` | `array` | Yes | List of items {category, budgeted, actual}. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "budget_variance_analyzer",
  "arguments": {
    "budget_items": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "budget_variance_analyzer"`.
