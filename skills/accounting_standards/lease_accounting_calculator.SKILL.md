---
skill: lease_accounting_calculator
category: accounting_standards
description: Computes lease liability, ROU asset, and income statement impact for ASC 842.
tier: free
inputs: lease_payments, lease_term_years, discount_rate, lease_type
---

# Lease Accounting Calculator

## Description
Computes lease liability, ROU asset, and income statement impact for ASC 842.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `lease_payments` | `array` | Yes |  |
| `lease_term_years` | `integer` | Yes |  |
| `discount_rate` | `number` | Yes |  |
| `lease_type` | `string` | Yes |  |
| `residual_guarantee` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "lease_accounting_calculator",
  "arguments": {
    "lease_payments": [],
    "lease_term_years": 0,
    "discount_rate": 0,
    "lease_type": "<lease_type>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "lease_accounting_calculator"`.
