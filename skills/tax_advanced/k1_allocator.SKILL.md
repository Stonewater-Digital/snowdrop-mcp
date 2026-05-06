---
skill: k1_allocator
category: tax_advanced
description: Allocates income, deductions, and distributions across partners with special allocations.
tier: free
inputs: partners, fund_income, fund_deductions, distributions
---

# K1 Allocator

## Description
Allocates income, deductions, and distributions across partners with special allocations.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `partners` | `array` | Yes |  |
| `fund_income` | `object` | Yes |  |
| `fund_deductions` | `object` | Yes |  |
| `distributions` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "k1_allocator",
  "arguments": {
    "partners": [],
    "fund_income": {},
    "fund_deductions": {},
    "distributions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "k1_allocator"`.
