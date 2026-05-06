---
skill: form_1099_generator
category: payroll
description: Produces Snowdrop's 1099-NEC structure for Thunder review.
tier: free
inputs: payee, total_paid, tax_year
---

# Form 1099 Generator

## Description
Produces Snowdrop's 1099-NEC structure for Thunder review.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `payee` | `object` | Yes |  |
| `total_paid` | `number` | Yes |  |
| `tax_year` | `integer` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "form_1099_generator",
  "arguments": {
    "payee": {},
    "total_paid": 0,
    "tax_year": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "form_1099_generator"`.
