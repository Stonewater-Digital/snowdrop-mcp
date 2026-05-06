---
skill: envelope_budget_allocator
category: budgeting
description: Allocates a total budget across categories by percentage using the envelope budgeting method. Validates percentages sum to 100.
tier: free
inputs: total_budget, categories
---

# Envelope Budget Allocator

## Description
Allocates a total budget across categories by percentage using the envelope budgeting method. Validates percentages sum to 100.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `total_budget` | `number` | Yes | Total monthly budget to allocate in dollars. |
| `categories` | `array` | Yes | List of categories with name and percentage allocation. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "envelope_budget_allocator",
  "arguments": {
    "total_budget": 0,
    "categories": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "envelope_budget_allocator"`.
