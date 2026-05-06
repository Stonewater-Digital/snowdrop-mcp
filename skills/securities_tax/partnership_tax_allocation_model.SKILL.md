---
skill: partnership_tax_allocation_model
category: securities_tax
description: Allocates partnership income among partners with preferred returns.
tier: free
inputs: partners, taxable_income
---

# Partnership Tax Allocation Model

## Description
Allocates partnership income among partners with preferred returns.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `partners` | `array` | Yes |  |
| `taxable_income` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "partnership_tax_allocation_model",
  "arguments": {
    "partners": [],
    "taxable_income": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "partnership_tax_allocation_model"`.
