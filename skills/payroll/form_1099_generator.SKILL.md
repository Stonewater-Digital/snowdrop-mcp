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
| `payee` | `object` | Yes | Payee info object with keys: `name` (string), `tin` (string), `address` (string). |
| `total_paid` | `number` | Yes | Total USD amount paid to the payee in the tax year. Must be >= $600 to trigger 1099-NEC. |
| `tax_year` | `integer` | Yes | Four-digit tax year for the form (e.g. 2024). |

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
    "payee": {"name": "Jane Contractor", "tin": "123-45-6789", "address": "123 Main St, Austin TX 78701"},
    "total_paid": 8500.00,
    "tax_year": 2024
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "form_1099_generator"`.
